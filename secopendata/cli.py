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

from .client import NotSubscribedError, SECAPIError, SECClient, infer_key_scope
from .config import MissingKeyError
from .products import CATEGORIES, REGISTRY, FundDailyInfo, FundFactsheet


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


def _json_arg(raw: str | None, path: str | None) -> Any | None:
    if raw and path:
        raise SystemExit("Use either --json or --json-file, not both.")
    if path:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    if raw:
        return json.loads(raw)
    return None


def cmd_products(args: argparse.Namespace, client: SECClient) -> Any:
    return [
        {"name": p.name, "title": p.title, "description": p.description}
        for p in REGISTRY.values()
    ]


def cmd_categories(args: argparse.Namespace, client: SECClient) -> Any:
    return [
        {
            "key_scope": c.key_scope,
            "env_var": f"SEC_{c.key_scope.replace('-', '_').upper()}_KEY",
            "title": c.title,
            "description": c.description,
        }
        for c in CATEGORIES.values()
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


def cmd_request(args: argparse.Namespace, client: SECClient) -> Any:
    params = _kv_params(args.param)
    body = _json_arg(args.json, args.json_file)
    key_scope = args.key_scope or infer_key_scope(args.path)
    return client.request(
        args.method,
        args.path,
        key_scope=key_scope,
        params=params,
        json_body=body,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secopendata",
        description="Pull data from the Thai SEC OpenAPI (api.sec.or.th).",
    )
    parser.add_argument("--timeout", type=int, default=30)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("products", help="list legacy registered API products").set_defaults(func=cmd_products)
    sub.add_parser("categories", help="list SEC Open Data portal key scopes").set_defaults(func=cmd_categories)
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

    p_req = sub.add_parser("request", help="raw GET/POST against any api.sec.or.th path")
    p_req.add_argument("--method", choices=["GET", "POST"], default="GET")
    p_req.add_argument("--path", required=True, help="API path, e.g. /v1/one-report/...")
    p_req.add_argument("--key-scope", default="", help="subscription-key scope; inferred from path if omitted")
    p_req.add_argument("--param", action="append", help="repeatable key=value query param")
    p_req.add_argument("--json", default="", help="JSON request body for POST endpoints")
    p_req.add_argument("--json-file", dest="json_file", default="", help="file containing JSON request body")
    p_req.set_defaults(func=cmd_request)

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
