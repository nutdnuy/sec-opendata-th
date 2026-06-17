"""Command-line interface for the SEC OpenData client.

All subcommands print JSON to stdout so they compose with other tools and so the
plugin's slash commands can parse the result. Run ``python -m secopendata -h``.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from typing import Any

from .client import NotSubscribedError, SECAPIError, SECClient
from .config import MissingKeyError
from .products import REGISTRY, FundDailyInfo, FundFactsheet


def _emit(data: Any) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2, default=str)
    sys.stdout.write("\n")


def _kv_params(pairs: list[str] | None) -> dict[str, str]:
    params: dict[str, str] = {}
    for item in pairs or []:
        if "=" not in item:
            raise SystemExit(f"--param expects key=value, got: {item}")
        key, value = item.split("=", 1)
        params[key] = value
    return params


def cmd_products(args: argparse.Namespace, client: SECClient) -> Any:
    return [
        {"name": p.name, "title": p.title, "description": p.description}
        for p in REGISTRY.values()
    ]


def cmd_amcs(args: argparse.Namespace, client: SECClient) -> Any:
    return FundFactsheet(client).amc_list()


def cmd_funds(args: argparse.Namespace, client: SECClient) -> Any:
    ff = FundFactsheet(client)
    unique_id = args.amc
    if not unique_id.startswith("C"):  # treat as a name to resolve
        resolved = ff.resolve_amc_id(args.amc)
        if not resolved:
            raise SystemExit(f"No AMC matched '{args.amc}'. Try `amcs` to list ids.")
        unique_id = resolved
    return ff.funds_by_amc(unique_id)


def cmd_nav(args: argparse.Namespace, client: SECClient) -> Any:
    proj_id = args.proj_id
    if not proj_id and args.amc and args.abbr:
        ff = FundFactsheet(client)
        amc_id = args.amc if args.amc.startswith("C") else ff.resolve_amc_id(args.amc)
        for fund in ff.funds_by_amc(amc_id or ""):
            abbr = str(fund.get("abbr_name") or fund.get("fund_abbr_name") or "")
            if abbr.lower() == args.abbr.lower():
                proj_id = str(fund.get("proj_id") or fund.get("unique_id") or "")
                break
        if not proj_id:
            raise SystemExit(f"No fund '{args.abbr}' under AMC '{args.amc}'.")
    if not proj_id:
        raise SystemExit("Provide --proj-id, or both --amc and --abbr.")
    date = args.date or dt.date.today().isoformat()
    return {"proj_id": proj_id, "nav_date": date,
            "nav": FundDailyInfo(client).daily_nav(proj_id, date)}


def cmd_fund_info(args: argparse.Namespace, client: SECClient) -> Any:
    ff = FundFactsheet(client)
    info: dict[str, Any] = {
        "proj_id": args.proj_id,
        "policy": ff.policy(args.proj_id),
        "classes": ff.classes(args.proj_id),
    }
    if args.top5:
        info["top5"] = ff.top5(args.proj_id, args.top5)
    return info


def cmd_get(args: argparse.Namespace, client: SECClient) -> Any:
    params = _kv_params(args.param)
    if args.paginate:
        return list(
            client.get_paginated(
                args.product, args.path or "", params=params,
                page_param=args.page_param, size_param=args.size_param,
                page_size=args.page_size,
            )
        )
    return client.get(args.product, args.path or "", params=params)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secopendata",
        description="Pull data from the Thai SEC OpenAPI (api.sec.or.th).",
    )
    parser.add_argument("--timeout", type=int, default=30)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("products", help="list registered API products").set_defaults(func=cmd_products)
    sub.add_parser("amcs", help="list all asset management companies").set_defaults(func=cmd_amcs)

    p_funds = sub.add_parser("funds", help="list funds for an AMC (name or unique_id)")
    p_funds.add_argument("--amc", required=True)
    p_funds.set_defaults(func=cmd_funds)

    p_nav = sub.add_parser("nav", help="daily NAV for a fund on a date")
    p_nav.add_argument("--proj-id", dest="proj_id", default="")
    p_nav.add_argument("--amc", default="")
    p_nav.add_argument("--abbr", default="")
    p_nav.add_argument("--date", default="")
    p_nav.set_defaults(func=cmd_nav)

    p_info = sub.add_parser("fund-info", help="policy, share classes, optional top5")
    p_info.add_argument("--proj-id", dest="proj_id", required=True)
    p_info.add_argument("--top5", default="", help="period, e.g. a fiscal/quarter code")
    p_info.set_defaults(func=cmd_fund_info)

    p_get = sub.add_parser("get", help="raw GET against any product/path (escape hatch)")
    p_get.add_argument("--product", required=True)
    p_get.add_argument("--path", default="")
    p_get.add_argument("--param", action="append", help="repeatable key=value query param")
    p_get.add_argument("--paginate", action="store_true")
    p_get.add_argument("--page-param", dest="page_param", default="page")
    p_get.add_argument("--size-param", dest="size_param", default="limit")
    p_get.add_argument("--page-size", dest="page_size", type=int, default=100)
    p_get.set_defaults(func=cmd_get)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    client = SECClient(timeout=args.timeout)
    try:
        _emit(args.func(args, client))
        return 0
    except MissingKeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    except NotSubscribedError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 4
    except SECAPIError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
