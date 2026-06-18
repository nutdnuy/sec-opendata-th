# Fund API Mapping

เปรียบเทียบ API เดิม vs ใหม่ เพื่อ migrate ไป SEC Open Data

## ตารางความหมายของการเปลี่ยนแปลง

| ประเภทการเปลี่ยนแปลง | คำอธิบาย                                                      |
| :----------------- | :----------------------------------------------------------- |
| Under Development  | API ที่อยู่ระหว่างพัฒนา/ปรับปรุง                                     |
| Unchanged          | API เดิมยังคงมีในระบบใหม่                                        |
| Updated            | API เดิมมีการปรับโครงสร้าง endpoint หรือ parameter หรือ โครงสร้างของข้อมูล |
| Deprecated         | API เดิมถูกยกเลิก                                               |

ตารางด้านล่างแสดงการเปรียบเทียบระหว่าง
**Fund API ในระบบเดิม** ได้แก่ Fund Factsheet API และ Fund Daily Info กับ **Fund API ในระบบใหม่**

## Fund Factsheet API Mapping

| Fund API เดิม                                                 | Fund API ใหม่                                                 | Endpoint เดิม                                        | Endpoint ใหม่                                        | Change Type       | หมายเหตุ                                |
| ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------------------- | --------------------------------------------------- | ----------------- | -------------------------------------- |
| 01. รายชื่อ บลจ.                                               | 1. รายชื่อบริษัทจัดการกองทุนรวม                                    | /FundFactsheet/fund/amc                             | /v2/fund/general-info/amcs                          | Updated           | ปรับโครงสร้าง endpoint                   |
| 02. กองทุนภายใต้การบริหารจัดการของบลจ.                           | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | /FundFactsheet/fund/amc/{unique_id}                 | /v2/fund/general-info/profiles                      | Updated           | รวมข้อมูลทั่วไปทั้งหมด และเพิ่มข้อมูลชนิดหน่วยลงทุน |
| 03. ค้นหาชื่อกองทุนด้วยชื่อย่อหรือชื่อกองทุนบางส่วน                       | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | POST /FundFactsheet/fund                            | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 04. URL ของ Fact Sheet และรายงานประจำปีของกองทุน               | 6. URL และ ไฟล์ pdf ของ Fund Fact Sheet                       | /FundFactsheet/fund/{proj_id}/URLs                  | /v2/fund/factsheet/urls                             | Updated           | ปรับโครงสร้าง endpoint                   |
| 05. การเสนอขาย                                               | 7. การเสนอขายกองทุนรวม                                        | /FundFactsheet/fund/{proj_id}/IPO                   | /v2/fund/factsheet/ipos                             | Updated           | ปรับโครงสร้าง endpoint                   |
| 06. มูลค่าหน่วยลงทุน/จำนวนหน่วยลงทุนในการสั่งซื้อขาย/คงเหลือ            | 9. มูลค่าและจำนวนหน่วยลงทุนขั้นต่ำในการสั่งซื้อ สั่งขายคืน หรือคงเหลือของกองทุนรวม | /FundFactsheet/fund/{proj_id}/investment            | /v2/fund/factsheet/subscription-redemption-minimums | Updated           | ปรับโครงสร้าง endpoint                   |
| 07. ลักษณะและอายุโครงการ                                       | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | /FundFactsheet/fund/{proj_id}/project_type          | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 08. ประเภทกองทุนตามนโยบายกองทุน                                | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | /FundFactsheet/fund/{proj_id}/policy                | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 09. ประเภทกองทุนตามลักษณะพิเศษ                                  | 3. ประเภทกองทุนตามลักษณะพิเศษ                                   | /FundFactsheet/fund/{proj_id}/specification         | /v2/fund/general-info/specifications                | Updated           | ปรับโครงสร้าง endpoint                   |
| 10. ประเภทกองทุน Feeder Fund (เฉพาะกรณีที่เป็น Feeder Fund เท่านั้น) | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | /FundFactsheet/fund/{proj_id}/feeder_fund           | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 11. ระยะเวลาขายและรับซื้อคืน                                     | 10. ระยะเวลาขายและรับซื้อคืน                                     | /FundFactsheet/fund/{proj_id}/redemption            | /v2/fund/factsheet/subscription-redemption-periods  | Updated           | ปรับโครงสร้าง endpoint                   |
| 12. ความเหมาะสมกับผู้ลงทุนและความเสี่ยงของกองทุน                    | 11. ระดับความเสี่ยงของกองทุน                                     | /FundFactsheet/fund/{proj_id}/suitability           | /v2/fund/factsheet/risk-spectrum                    | Updated           | ปรับโครงสร้าง endpoint                   |
| 13. ปัจจัยความเสี่ยงที่สำคัญ                                        | ยกเลิก                                                        | /FundFactsheet/fund/{proj_id}/risk                  | /v2/fund/general-info/profiles                      | Deprecated        |                                        |
| 14. สัดส่วนประเภททรัพย์สินที่ลงทุนของกองทุน                           | 16. สัดส่วนประเภททรัพย์สินที่ลงทุนของกองทุนรวม                        | /FundFactsheet/fund/{proj_id}/asset                 | /v2/fund/factsheet/asset-allocation                 | Updated           | ปรับโครงสร้าง endpoint                   |
| 15. อัตราส่วนหมุนเวียนการลงทุนของกองทุนรวม                         | 12. ข้อมูลเชิงสถิติของกองทุน                                       | /FundFactsheet/fund/{proj_id}/turnover_ratio        | /v2/fund/factsheet/statistics                       | Merged            |                                        |
| 16. ประมาณผลตอบแทนและระยะเวลาการลงทุนที่กองทุนจะได้รับ (โดยประมาณ) | ยกเลิก                                                        | -                                                   | -                                                   | Deprecated        |                                        |
| 17. ประมาณการพอร์ตการลงทุนของกองทุน Buy & Hold                  | ยกเลิก                                                        | -                                                   | -                                                   | Deprecated        |                                        |
| 18. ดัชนีชี้วัดกองทุน                                              | 8. ดัชนีชี้วัดกองทุน                                               | /FundFactsheet/fund/{proj_id}/benchmark             | /v2/fund/factsheet/benchmarks                       | Updated           | ปรับโครงสร้าง endpoint                   |
| 19. ประเภทกองทุนรวมเพื่อใช้เปรียบเทียบผลการดำเนินงาน ณ จุดขาย        | ยกเลิก                                                        | -                                                   | -                                                   | Deprecated        |                                        |
| 20. ประเภทหน่วยลงทุนที่มีในกองทุน (ถ้ามีมากกว่า 1 ประเภท)             | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | /FundFactsheet/fund/{proj_id}/class_fund            | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 21. ค้นหารหัสกองลงทุนด้วยชื่อย่อกองทุนหรือชื่อย่อชนิดหน่วยลงทุน             | 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน | POST /FundFactsheet/fund/class_fund                 | /v2/fund/general-info/profiles                      | Merged            |                                        |
| 22. ผลการดำเนินงานย้อนหลังของกองทุน                              | 15. ผลการดำเนินงานย้อนหลังของกองทุนรวม                           | /FundFactsheet/fund/{proj_id}/performance           | /v2/fund/factsheet/performance                      | Updated           | ปรับโครงสร้าง endpoint                   |
| 23. ผลขาดทุนสูงสุดในช่วง 5 ปีและความผันผวนของผลการดำเนินงานย้อนหลัง 5 ปี | 12. ข้อมูลเชิงสถิติของกองทุน                                       | -                                                   | /v2/fund/factsheet/statistics                       | Merged            |                                        |
| 24. นโยบายการจ่ายเงินปันผลตามชนิดหน่วยลงทุนของกองทุน                | 13. นโยบายการจ่ายเงินปันผลของกองทุนรวม                           | /FundFactsheet/fund/{proj_id}/dividend              | /v2/fund/factsheet/dividend-policy                  | Updated           | ปรับโครงสร้าง endpoint                   |
| 25. ค่าธรรมเนียมกองทุน                                          | 14. ค่าธรรมเนียมของกองทุน                                       | /FundFactsheet/fund/{proj_id}/fee                   | /v2/fund/factsheet/fees                             | Updated           | ปรับโครงสร้าง endpoint                   |
| 26. ผู้เกี่ยวข้องกับกองทุน                                          | 5. ผู้เกี่ยวข้องกับกองทุน                                           | /FundFactsheet/fund/{proj_id}/InvolveParty          | /v2/fund/general-info/involve-parties               | Updated           | ปรับโครงสร้าง endpoint                   |
| 27. การลงทุนของกองทุนรวม ณ สิ้นสุดวันทำการแต่ละรอบไตรมาส            | 18. การลงทุนของกองทุนรวม ณ วันทำการสุดท้ายแต่ละไตรมาส              | /FundFactsheet/fund/{proj_id}/FundPort/{period}     | /v2/fund/outstanding/portfolio                      | Updated           | ปรับโครงสร้าง endpoint                   |
| 28. สัดส่วนของการลงทุนของกองทุนรวม                               | 19. สัดส่วนการลงทุนของกองทุนรวมตามประเภทสินทรัพย์ ณ วันทำการสุดท้ายของเดือน | /FundFactsheet/fund/{proj_id}/FundFullPort/{period} | /v2/fund/outstanding/portfolio-asset-type           | Updated           | ปรับโครงสร้าง endpoint และโครงสร้างข้อมูล   |
| 29. หลักทรัพย์ 5 อันดับแรกที่ลงทุน                                   | 17. ทรัพย์สินที่ลงทุน 5 อันดับแรก                                    | /FundFactsheet/fund/{proj_id}/FundTop5/{period}     | /v2/fund/factsheet/top5-holdings                    | Updated           | ปรับโครงสร้าง endpoint                   |
| 30. ประวัติการเปลี่ยนชื่อ / นโยบาย / การลงทุนต่างประเทศ / ลักษณะโครงการ | อยู่ระหว่างปรับปรุง                                               | /FundFactsheet/fund/{proj_id}/FundHist              | -                                                   | Under Development | Under development                      |
| 31. ความผันผวนของส่วนต่างของผลตอบแทนเฉลี่ยของกองทุนรวมและผลตอบแทนของดัชนีอ้างอิงย้อนหลัง 1 ปี (Tracking Error) | 12. ข้อมูลเชิงสถิติของกองทุน                                       | /FundFactsheet/fund/{proj_id}/FundTrackingError     | /v2/fund/factsheet/statistics                       | Merged            |                                        |
| 32. ประวัติการเปลี่ยนบริษัทจัดการของกองทุน                           | ยกเลิก                                                        | -                                                   | -                                                   | Deprecated        |                                        |

## Fund Daily Info API Mapping

| Fund API เดิม                   | Fund API ใหม่                             | Endpoint เดิม                                 | Endpoint ใหม่                         | Change Type | หมายเหตุ                                 |
| ------------------------------ | ---------------------------------------- | -------------------------------------------- | ------------------------------------ | ----------- | --------------------------------------- |
| 01. NAV กองทุนรวมรายวัน          | 20. มูลค่าทรัพย์สินสุทธิ (NAV) ของกองทุนรวมรายวัน | /FundDailyInfo/{proj_id}/dailynav/{nav_date} | /v2/fund/daily-info/nav              | Updated     | ปรับโครงสร้าง endpoint และโครงสร้างของข้อมูล |
| 02. ประวัติการจ่ายเงินปันผลของกองทุน | 21. ประวัติการจ่ายเงินปันผลของกองทุนรวม        | /FundDailyInfo/{proj_id}/dividend            | /v2/fund/daily-info/dividend-history | Updated     | ปรับโครงสร้าง endpoint                    |
| 03. รายชื่อบริษัทที่ส่งข้อมูลรายวัน      | ยกเลิก                                    | -                                            | -                                    | Deprecated  |                                         |

### 1. รายชื่อบริษัทจัดการกองทุนรวม (บลจ.)

ข้อมูลรายชื่อบริษัทจัดการกองทุนรวม (บลจ.) ที่อยู่ภายใต้การกำกับดูแลของสำนักงานก.ล.ต.

[!NOTE] สามารถนำรหัสบริษัทหลักทรัพย์จัดการกองทุน (unique_id) ไปใช้ร่วมกับ Fund API ข้ออื่น เช่น ข้อ 02. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน เพื่อค้นหากองทุนที่บลจ.นั้น ๆ บริหารดูแล

### Endpoint

```
GET/v2/fund/general-info/amcs
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].unique_id

string

รหัสบริษัทหลักทรัพย์จัดการกองทุน

items[].comp_name_th

string

ชื่อบริษัทหลักทรัพย์จัดการกองทุนภาษาไทย

items[].comp_name_en

string

ชื่อบริษัทหลักทรัพย์จัดการกองทุนภาษาอังกฤษ

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด

### 2. กองทุนรวมภายใต้การบริหารจัดการของบลจ.และลักษณะทั่วไปของแต่ละกองทุน

ข้อมูลกองทุนรวมภายใต้การบริหารจัดการของแต่ละบริษัทหลักทรัพย์จัดการกองทุน (บลจ.) พร้อมลักษณะทั่วไปของแต่ละกองทุน เช่น สถานะกองทุน นโยบายการลงทุน ลักษณะโครงการ อายุโครงการ ชนิดหน่วยลงทุน (Class Fund) รวมถึงข้อมูลกองทุนหลักในกรณีที่เป็น Feeder Fund

[!NOTE] หากต้องการดึงข้อมูลเฉพาะกองที่ยังมีสถานะ active อยู่ในปัจจุบัน (กำลังอยู่ระหว่างเสนอขาย หรือ จดทะเบียน) ให้ผู้ใช้งานทำการกรองผลลัพธ์จาก API ข้อนี้ด้วยคอลัมน์ fund_status ที่มีค่าเป็น 'IPO' และ 'Registered'

### Endpoint

```
GET/v2/fund/general-info/profiles
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

fund_status

string

สถานะกองทุน ใช้สำหรับกรองข้อมูลตามสถานะที่สนใจ

project_info

string

ข้อมูลโครงการ: ค้นหาแบบตรงตัว (exact match) จาก proj_id และค้นหาแบบบางส่วน (partial search) จาก proj_name_th, proj_name_en และ proj_abbr_name

company_info

string

ข้อมูลบริษัท: ค้นหาแบบตรงตัว (exact match) จาก unique_id และค้นหาแบบบางส่วน (partial search) จาก comp_name_th และ comp_name_en

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].unique_id

string

รหัสบริษัทหลักทรัพย์จัดการกองทุน

items[].comp_name_th

string

ชื่อบริษัทหลักทรัพย์จัดการกองทุนภาษาไทย

items[].comp_name_en

string

ชื่อบริษัทหลักทรัพย์จัดการกองทุนภาษาอังกฤษ

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].regis_id

string

เลขที่จดทะเบียนกองทุน

items[].proj_name_th

string

ชื่อโครงการจัดการกองทุนรวม (ไทย)

items[].proj_name_en

string

ชื่อโครงการจัดการกองทุนรวม (อังกฤษ)

items[].proj_abbr_name

string

ชื่อย่อโครงการจัดการกองทุนรวม

items[].fund_status

string

สถานะกองทุนรวม:

- Registered =จดทะเบียน
- IPO =เสนอขายหน่วยลงทุนครั้งแรก
- Expired =หมดเวลาเสนอขาย
- Canceled =เลิกโครงการ
- Liquidated =จดทะเบียนเลิก

items[].init_date

date

วันที่จัดตั้งกองทุนรวม

items[].regis_date

date

วันที่จดทะเบียนกองทุนรวม

items[].cancel_date

date

วันที่ยกเลิกกองทุนรวม

items[].invest_country_flag

string

ความเสี่ยงการลงทุนในต่างประเทศ:

- 1 =เน้นลงทุนต่างประเทศ
- 2 =ลงทุนในต่างประเทศบางส่วน
- 3 =ไม่มีความเสี่ยงต่างประเทศ
- 4 =มีความเสี่ยงทั้งในและต่างประเทศ

items[].proj_retail_type

string

ลักษณะโครงการ:

- A =กองทุนรวมที่เสนอขายเฉพาะผู้ลงทุนที่มิใช่รายย่อย
- B =กองทุนรวมที่เสนอขายเฉพาะผู้มีเงินลงทุนสูง
- F =กองทุนรวมเสริมสภาพคล่องเพื่อลดความเสี่ยงของการระดมทุนในตลาดตราสารหนี้ภาคเอกชน
- G =กองทุนรวมพิเศษเพื่อตอบสนองนโยบายภาครัฐ
- H =กองทุนรวมที่เสนอขายผู้ลงทุนที่มิใช่รายย่อยและผู้มีเงินลงทุนสูง
- N =กองทุนเพื่อผู้ลงทุนสถาบัน
- R =กองทุนเพื่อผู้ลงทุนทั่วไป
- V =กองทุนรวมเพื่อผู้ลงทุนที่เป็นกองทุนสำรองเลี้ยงชีพ
- X =กองทุนรวมที่เสนอขายผู้ลงทุนสถาบันและผู้ลงทุนรายใหญ่พิเศษ

items[].proj_term_flag

string

อายุโครงการ (Y = กำหนด N = ไม่กำหนด)

items[].proj_term_year

string

อายุโครงการ (ปี)

items[].proj_term_month

string

อายุโครงการ (เดือน)

items[].proj_term_day

string

อายุโครงการ (วัน)

items[].policy_desc

string

ประเภทกองทุนตามนโยบายกองทุน

items[].investment_policy_desc

string

นโยบายการลงทุน (ข้อมูลเป็นข้อความยาว อาจอยู่ในรูป HTML หรือ String ที่ Encode ด้วย Base64)

items[].management_style

string

กลยุทธ์การบริหารจัดการกองทุน (Management Style):

- AM =มุ่งหวังให้ผลประกอบการเคลื่อนไหวสูงกว่าดัชนีชี้วัด (active management)
- AN =กองทุนไทยมุ่งหวังให้ผลประกอบการเคลื่อนไหวตามกองทุนหลัก ส่วนกองทุนหลักมุ่งหวังให้ผลประกอบการสูงกว่าดัชนีชี้วัด
- PM =มุ่งหวังให้ผลประกอบการเคลื่อนไหวตามดัชนีชี้วัด (passive management/index tracking)
- PN =กองทุนไทยมุ่งหวังให้ผลประกอบการเคลื่อนไหวตามกองทุนหลัก ส่วนกองทุนหลักมุ่งหวังให้ผลประกอบการเคลื่อนไหวตามดัชนีชี้วัด
- IM =มุ่งหวังให้ได้รับผลประกอบการเคลื่อนไหวตรงกันข้ามกับผลตอบแทนรายวันของดัชนีอ้างอิง (inverse management)
- IN =กองทุนไทยมุ่งหวังให้ผลประกอบการเคลื่อนไหวตามกองทุนหลัก ส่วนกองทุนหลักมุ่งหวังให้ได้รับผลประกอบการเคลื่อนไหวตรงกันข้ามกับผลตอบแทนรายวันของดัชนีอ้างอิง
- LM =มุ่งหวังให้ได้รับผลประกอบการเคลื่อนไหวทวีคูณกับผลตอบแทนรายวันของดัชนีอ้างอิง (leveraged management)
- LN =กองทุนไทยมุ่งหวังให้ผลประกอบการเคลื่อนไหวตามกองทุนหลัก ส่วนกองทุนหลักมุ่งหวังให้ได้รับผลประกอบการเคลื่อนไหวทวีคูณกับผลตอบแทนรายวันของดัชนีอ้างอิง
- BH =มีกลยุทธ์การลงทุนครั้งเดียว (buy-and-hold)
- SM =มุ่งหวังให้ผลประกอบการเคลื่อนไหวตามดัชนีชี้วัด และในบางโอกาสอาจสร้างผลตอบแทนสูงกว่าดัชนีชี้วัด
- OT =อื่น ๆ

items[].feederfund_master_fund

string

ชื่อกองทุนหลัก (Master Fund)

items[].feederfund_country

string

ประเทศที่จดทะเบียนของกองทุนหลัก

items[].exchange_rate_protection_policy

string

นโยบายป้องกันความเสี่ยงจากอัตราแลกเปลี่ยน

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].fund_class_detail

string

ชื่อชนิดหน่วยลงทุน

items[].fund_class_description

string

คำอธิบายชนิดหน่วยลงทุนเพิ่มเติม (ถ้ามี)

items[].fund_class_tax_incentive_type

string

สิทธิประโยชน์ทางภาษี (SSF, Thai ESG)

items[].fund_class_isin_code

string

ISIN Code ของชนิดหน่วยลงทุน

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 3. ประเภทกองทุนรวมตามลักษณะพิเศษ

ข้อมูลประเภทกองทุนรวมตามลักษณะพิเศษ (Fund Specification) ซึ่งนิยามตามประกาศสำนักงาน ก.ล.ต. สน.87/2558 ภาคผนวก 2 ในระดับชนิดหน่วยลงทุน (Class Fund)

### Endpoint

```
GET/v2/fund/general-info/specifications
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].spec_code

string

รหัสลักษณะพิเศษ

items[].spec_desc

string

ประเภทกองทุนตามลักษณะพิเศษ (นิยามตามประกาศ สน.87/2558 ภาคผนวก 2)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด

### 4. ค่าธรรมเนียมที่เรียกเก็บจากกองทุนรวม และค่าธรรมเนียมทั้งหมด

ข้อมูลรายละเอียดค่าธรรมเนียมที่เรียกเก็บจากกองทุนรวมในระดับชนิดหน่วยลงทุน (Class Fund) แยกตามประเภทค่าธรรมเนียม เช่น ค่าธรรมเนียมการจัดการ (Management Fee), ค่าธรรมเนียมผู้ดูแลผลประโยชน์ (Trustee Fee), ค่าธรรมเนียมนายทะเบียนหน่วยลงทุน (Registrar Fee) รวมถึงค่าธรรมเนียมทั้งหมด (Total Fee) ตามที่ระบุไว้ในโครงการของกองทุน

### Endpoint

```
GET/v2/fund/general-info/mutual-fund-fees
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].fee_type_desc

string

ประเภทค่าธรรมเนียม ได้แก่ Distributor Fee, Investment Advisor Fee, Management Fee, Other Fee, Registrar Fee, Total Fee และ Trustee Fee

items[].rate

string

อัตราตามโครงการ

items[].rate_unit

string

หน่วยของอัตราตามโครงการ

items[].fee_other_desc

string

หมายเหตุเพิ่มเติม (ถ้ามี)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 5. ผู้เกี่ยวข้องกับกองทุนรวม

ข้อมูลบุคคลหรือนิติบุคคลที่เกี่ยวข้องกับกองทุนรวม ตามบทบาทหน้าที่ที่กำหนดไว้ในโครงการกองทุน เช่น ผู้ดูแลผลประโยชน์ นายทะเบียน ผู้แทนจำหน่าย ผู้สร้างสภาพคล่อง ที่ปรึกษาการลงทุน และหน่วยงานอื่นที่เกี่ยวข้อง

### Endpoint

```
GET/v2/fund/general-info/involve-parties
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

entity_type

string

ค้นหาประเภทบุคคล/นิติบุคคลที่เกี่ยวข้อง

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].entity_type

string

ประเภทบุคคล/นิติบุคคลที่เกี่ยวข้อง (ENTITY_TYPE):

- A =ผู้สอบบัญชี
- U =ผู้จัดจำหน่าย
- S =ผู้สนับสนุนการขายและรับซื้อคืน
- R =นายทะเบียนหน่วยลงทุน
- V =ผู้ดูแลผลประโยชน์
- M =ที่ปรึกษาการลงทุน
- O =ผู้รับมอบหมายงานด้านการจัดการลงทุน
- P =ผู้ลงทุนรายใหญ่
- K =ผู้ดูแลสภาพคล่อง
- N =ที่ปรึกษาทางการเงิน
- F =ผู้จัดการกองทุน

items[].entity_name_th

string

ชื่อบุคคล/นิติบุคคล (ภาษาไทย)

items[].entity_name_en

string

ชื่อบุคคล/นิติบุคคล (ภาษาอังกฤษ)

items[].address

string

ที่อยู่

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 6. URL และ ไฟล์ pdf ของ Fund Fact Sheet

ข้อมูลลิงก์ดาวน์โหลดไฟล์ PDF ของ Fund Fact Sheet (pdf_factsheet) รวมไปถึง URL สำหรับเข้าถึง Factsheet จากเว็บไซต์ของบลจ. (amc_url_factsheet) ซึ่งเป็นไฟล์ PDF และลิงก์ที่บลจ.จัดส่งให้สำนักงานโดยตรงในระดับชนิดหน่วยลงทุน (Class Fund) สำหรับกองทุนที่มีหลายชนิดหน่วยลงทุน (Class Fund) บลจ.จะจัดส่งไฟล์ PDF เพียงไฟล์เดียวให้สำนักงาน โดยภายในไฟล์ดังกล่าวได้รวบรวมข้อมูลของทุกชนิดหน่วยลงทุนไว้ ซึ่งสำนักงาน ก.ล.ต.นำไฟล์ PDF นี้มาให้บริการต่อผ่าน API โดยไม่มีการแยกไฟล์หรือปรับแก้ไขเนื้อหาเพิ่มเติม

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลา โดยแต่ละแถวจะแสดงข้อมูล Fund Factsheet ณ วันที่ใดวันที่หนึ่ง (as_of_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/urls
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการกองทุนรวม ({Type}{ID}_YYYY) เช่น M0000_2552

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].prospectus_type

string

รูปแบบหรือความถี่ของเอกสารชี้ชวน / factsheet ที่จัดทำ เช่น Monthly (รายเดือน)

items[].amc_url_factsheet

string

ลิงก์ไปยังเอกสาร Fund Factsheet บนเว็บไซต์ของบริษัทหลักทรัพย์จัดการกองทุน (AMC)

items[].pdf_factsheet

string

ลิงก์ไฟล์ PDF ของ Fund Factsheet ที่จัดเก็บโดย ก.ล.ต.

items[].as_of_date

date

วันที่อ้างอิงข้อมูลในเอกสาร Fund Factsheet (As of date)

items[].last_upd_date

datetime

วันที่และเวลาที่มีการแก้ไขข้อมูลล่าสุด



### 7. การเสนอขายกองทุนรวม

ข้อมูลการเสนอขายครั้งแรก (IPO) ของกองทุนรวม โดยอ้างอิงข้อมูลช่วงเวลาเริ่มต้น IPO (first_sell_start_date) และสิ้นสุด IPO (first_sell_end_date) ตามที่บลจ.นำส่งใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/ipos
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

string

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

string

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].first_sell_start_date

string

วันเริ่ม IPO

items[].first_sell_end_date

string

วันสิ้นสุด IPO

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 8. ดัชนีชี้วัดกองทุนรวม

ข้อมูลดัชนีชี้วัดของกองทุนรวมตามที่บลจ.นำส่งข้อมูลใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/benchmarks
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

date

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

string

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].group_seq

string

ลำดับกลุ่ม

items[].benchmark

string

ดัชนีชี้วัด (8.1)

items[].remark

string

หมายเหตุ (ถ้ามี)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด8. ดัชนีชี้วัดกองทุนรวม

ข้อมูลดัชนีชี้วัดของกองทุนรวมตามที่บลจ.นำส่งข้อมูลใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/benchmarks
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

date

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

string

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].group_seq

string

ลำดับกลุ่ม

items[].benchmark

string

ดัชนีชี้วัด (8.1)

items[].remark

string

หมายเหตุ (ถ้ามี)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด

### 9. มูลค่าและจำนวนหน่วยลงทุนขั้นต่ำในการสั่งซื้อ สั่งขายคืน หรือคงเหลือของกองทุนรวม

ข้อมูลมูลค่าและจำนวนหน่วยลงทุนขั้นต่ำสำหรับการสั่งซื้อครั้งแรกและครั้งถัดไป การสั่งขายคืน และจำนวนหน่วยลงทุนคงเหลือขั้นต่ำของกองทุนรวมในแต่ละชนิดหน่วยลงทุน (Class Fund) ตามที่บลจ.นำส่งข้อมูลใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/subscription-redemption-minimums
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].minimum_sub_ipo

float

มูลค่าขั้นต่ำของการสั่งซื้อครั้งแรก (9.5.3)

items[].minimum_sub_ipo_cur

string

หน่วย มูลค่าขั้นต่ำของการสั่งซื้อครั้งแรก (9.5.3)

items[].minimum_sub

float

มูลค่าขั้นต่ำของการสั่งซื้อครั้งถัดไป (9.5.4)

items[].minimum_sub_cur

string

หน่วย มูลค่าขั้นต่ำของการสั่งซื้อครั้งถัดไป (9.5.4)

items[].minimum_sub_unit

string

จำนวนหน่วยลงทุนขั้นต่ำของการสั่งซื้อครั้งถัดไป (9.5.4)

items[].minimum_redempt

float

มูลค่าขั้นต่ำของการสั่งขายคืน (9.5.6)

items[].minimum_redempt_cur

string

หน่วย (มูลค่าขั้นต่ำของการสั่งขายคืน) (9.5.6)

items[].minimum_redempt_unit

string

จำนวนหน่วยลงทุนขั้นต่ำของการสั่งขายคืน (9.5.6)

items[].lowbal_val

float

มูลค่าคงเหลือขั้นต่ำ

items[].lowbal_val_cur

string

หน่วย มูลค่าคงเหลือขั้นต่ำ

items[].lowbal_unit

string

จำนวนหน่วยคงเหลือขั้นต่ำ

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 10. ระยะเวลาขายและรับซื้อคืนของกองทุนรวม

ข้อมูลระยะเวลารับคำสั่งซื้อ (Subscription) และคำสั่งขายคืน (Redemption) รวมถึงระยะเวลาการรับเงินค่าขายคืนของกองทุนรวมในแต่ละชนิดหน่วยลงทุน (Class Fund) ตามที่บลจ.นำส่งข้อมูลใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/subscription-redemption-periods
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].type

string

ประเภทขายและรับซื้อคืน ได้แก่ subscription และ redemption

items[].period

string

ระยะเวลาขายและรับซื้อคืน

items[].redemp_period_oth

string

คำอธิบายการขายและรับซื้อคืน (กรณีที่ period มีค่าเป็น อื่น ๆ)

items[].settlement_period

string

ระยะเวลาการรับเงินค่าขายคืน

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 11. ระดับความเสี่ยงของกองทุนรวม

ข้อมูลระดับความเสี่ยงของกองทุนรวม (Risk Spectrum) ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/risk-spectrum
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].risk_spectrum

string

ระดับความเสี่ยงของกองทุนรวม (RS1–RS8 และ RS81)

items[].risk_spectrum_desc

string

รายละเอียดความเสี่ยงของกองทุนรวม

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 12. ข้อมูลเชิงสถิติของกองทุนรวม

ข้อมูลสถิติสำคัญของกองทุนรวม (Fund Statistics) ในแต่ละชนิดหน่วยลงทุน (Class Fund) ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน เช่น อัตราหมุนเวียนพอร์ต (Portfolio Turnover Ratio), Maximum Drawdown, Sharpe Ratio, Beta, Alpha, Yield to Maturity เป็นต้น

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/statistics
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].portfolio_turnover_ratio

string

อัตราส่วนหมุนเวียนการลงทุน (Portfolio Turn Over Ratio)

items[].recovering_period

string

ระยะเวลาที่ฟื้นตัว (Recovering Period)

items[].portfolio_duration_period

string

อายุเฉลี่ยของกองทุนตราสารหนี้ (Portfolio Duration)

items[].maximum_drawdown

string

อัตราผลขาดทุนสูงสุดของกองทุนรวมในระยะเวลา 5 ปีย้อนหลัง (หรือตั้งแต่จัดตั้งกองทุนกรณีที่ยังไม่ครบ 5 ปี) (Maximum Drawdown)

items[].sharpe_ratio

string

Sharpe Ratio (หมายเหตุ : เฉพาะกองตราสารทุน)

items[].beta

string

Beta (หมายเหตุ : เฉพาะกองตราสารทุน)

items[].alpha

string

Alpha (หมายเหตุ : เฉพาะกองตราสารทุน)

items[].fx_hedging

string

FX Hedging

items[].tracking_error

string

Tracking Error

items[].yield_to_maturity

string

Yield to Maturity

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด

### 13. นโยบายการจ่ายเงินปันผลของกองทุนรวม

ข้อมูลนโยบายการจ่ายเงินปันผลของกองทุนรวม (Fund Dividend Policy) ในแต่ละชนิดหน่วยลงทุน (Class Fund) ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน ซึ่งกองทุนหรือชนิดหน่วยลงทุนอาจมีการเปลี่ยนแปลงนโยบายการจ่ายเงินปันผลได้

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/dividend-policy
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].dividend_policy

string

นโยบายการจ่ายเงินปันผล

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 14. ค่าธรรมเนียมของกองทุนรวม

ข้อมูลค่าธรรมเนียมของกองทุนรวมในแต่ละชนิดหน่วยลงทุน (Class Fund) เช่น ค่าธรรมเนียมการรับซื้อคืนหน่วยลงทุน (Back-end Fee), ค่าธรรมเนียมการสับเปลี่ยนหน่วยลงทุนเข้า (Switching In Fee), ค่าธรรมเนียมการโอนหน่วยลงทุน (Transfer Fee) เป็นต้น ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/fees
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].fee_type_desc

string

ประเภทค่าธรรมเนียม:

- Front-end Fee =ค่าธรรมเนียมการขายหน่วยลงทุน
- Back-end Fee =ค่าธรรมเนียมการรับซื้อคืนหน่วยลงทุน
- Switching In =ค่าธรรมเนียมการสับเปลี่ยนหน่วยลงทุนเข้า
- Switching Out =ค่าธรรมเนียมการสับเปลี่ยนหน่วยลงทุนออก
- Transfer Fee =ค่าธรรมเนียมการโอนหน่วยลงทุน
- Total Fee and Expense =ค่าธรรมเนียมและค่าใช้จ่ายรวมทั้งหมด
- Management Fee =ค่าธรรมเนียมการจัดการ

items[].rate

float

อัตราตามโครงการ

items[].actual_value

float

อัตราที่จ่ายจริง

items[].fee_other_desc

string

หมายเหตุเพิ่มเติม (ถ้ามี)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 15. ผลการดำเนินงานย้อนหลังของกองทุนรวม

ข้อมูลผลการดำเนินงานย้อนหลังของกองทุนรวม (Historical Fund Performance) ในแต่ละชนิดหน่วยลงทุน (Class Fund) ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/performance
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].performance_type_desc

string

คำอธิบายประเภทผลตอบแทน

items[].reference_period

string

หมุดเวลาและปีย้อนหลัง

items[].performance_value

string

ผลการดำเนินงานย้อนหลังของกองทุน (8.3)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 16. สัดส่วนประเภททรัพย์สินที่ลงทุนของกองทุนรวม

ข้อมูลสัดส่วนการลงทุนจำแนกตามประเภททรัพย์สินของกองทุนรวม (Fund Asset Allocation by Asset Type) ตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน โดยแสดงสัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV) ในแต่ละประเภททรัพย์สิน เช่น หุ้นสามัญ หน่วยลงทุน เงินฝากธนาคาร และพันธบัตรรัฐบาล เป็นต้น

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/asset-allocation
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].asset_seq

number

ลำดับรายการ

items[].asset_name

string

ประเภททรัพย์สินที่ลงทุน

items[].asset_ratio

float

สัดส่วน (%NAV) ที่ลงทุนในประเภททรัพย์สินนั้น

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 17. ทรัพย์สินที่ลงทุน 5 อันดับแรก

ข้อมูลทรัพย์สินที่กองทุนรวมลงทุน 5 อันดับแรก โดยแสดงชื่อทรัพย์สิน ลำดับอันดับการลงทุน และสัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV) ในช่วงเวลานั้นตามที่บลจ.รายงานใน Fund Fact Sheet แต่ละงวดรายงาน

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ Fund Fact Sheet นั้น ๆ มีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ Fund Factsheet นั้นเริ่มมีผล (start_date) และวันที่สิ้นสุดผล (end_date) ซึ่งกองทุนหรือชนิดหน่วยลงทุนหนึ่งรายการอาจมีหลายงวดข้อมูลย้อนหลัง

### Endpoint

```
GET/v2/fund/factsheet/top5-holdings
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_date

date

ระบุวันที่เริ่มต้นที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี start_date มากกว่าหรือเท่ากับค่าที่ระบุ

end_date

date

ระบุวันที่สิ้นสุดที่ factsheet มีผล (รูปแบบ: YYYY-MM-DD) ระบบจะคืนข้อมูลที่มี end_date น้อยกว่าหรือเท่ากับค่าที่ระบุ

latest

boolean

หากต้องการเฉพาะข้อมูลจาก factsheet ที่มีผลล่าสุดเท่านั้น ให้ระบุค่า latest เป็น true และระบบจะไม่พิจารณา start_date และ end_date หากมีการส่งค่าเข้ามา

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].start_date

date

วันที่เริ่มต้นที่ factsheet มีผล

items[].end_date

date

วันที่สิ้นสุดที่ factsheet มีผล หมายเหตุ: หากเป็นข้อมูลจาก factsheet ที่มีผลล่าสุด end_date จะมีค่าเป็น null

items[].prospectus_type

string

ประเภทการส่ง factsheet ของบลจ.:

- IPO =ส่งเมื่อยื่นขอจัดตั้งกองทุน
- Monthly =ส่งรายเดือน
- SignificantFactsheet =ส่งเมื่อมีการเปลี่ยนแปลงข้อมูลอย่างมีนัยสำคัญ

items[].asset_seq

number

ลำดับรายการ

items[].asset_name

string

ทรัพย์สินที่ลงทุน

items[].asset_ratio

number

สัดส่วน (%NAV) ที่ลงทุนในทรัพย์สินนั้น

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 18. การลงทุนของกองทุนรวม ณ วันทำการสุดท้ายแต่ละไตรมาส

ข้อมูลการลงทุนของกองทุนรวม ณ วันทำการสุดท้ายของไตรมาส (Fund Portfolio) โดยแสดงข้อมูลรายละเอียดสินทรัพย์และหนี้สินที่กองทุนถือครองในแต่ละไตรมาส ได้แก่ ประเภททรัพย์สิน ชื่อหลักทรัพย์ ผู้ออกหลักทรัพย์ มูลค่าตลาด และสัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV)

[!NOTE] ข้อมูลเป็นข้อมูลรายไตรมาสย้อนหลัง 3 ปี โดยงวดข้อมูลล่าสุดมีระยะเวลาในการนำมาเปิดเผย (lag time) 45 วัน หลังวันทำการสุดท้ายของไตรมาสนั้น ๆ ผู้ใช้งานสามารถดึงข้อมูลงวดที่ต้องการได้ผ่านพารามิเตอร์ period_start และ period_end โดยข้อมูลแต่ละแถวจะระบุงวดข้อมูล (period ในรูปแบบ YYYYMM) และวันที่อ้างอิง (as_of_date) กำกับเพื่อระบุช่วงเวลาที่ข้อมูลนั้นมีผล

### Endpoint

```
GET/v2/fund/outstanding/portfolio
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_period

date

ระบุงวดข้อมูลแรกที่ต้องการดึงข้อมูล (รูปแบบ: YYYYMM) หมายเหตุ: หากต้องการดึงข้อมูลงวดเดียว ให้ระบุ period_start และ period_end เป็นงวดเดียวกัน

end_period

date

ระบุงวดข้อมูลสุดท้ายที่ต้องการดึงข้อมูล (รูปแบบ: YYYYMM) หมายเหตุ: หากต้องการดึงข้อมูลงวดเดียว ให้ระบุ period_start และ period_end เป็นงวดเดียวกัน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].as_of_date

date

ข้อมูล ณ วันที่ (YYYY-MM-DD)

items[].assetliab_code

string

รหัสประเภทสินทรัพย์หนี้สิน

items[].assetliab_desc

string

ประเภทสินทรัพย์หนี้สิน

items[].issue_code

string

ชื่อย่อหลักทรัพย์

items[].isin_code

string

ISIN Code

items[].issuer

string

ชื่อผู้ออกหลักทรัพย์

items[].market_value

number

มูลค่าตามราคาตลาด (บาท) ปัดเศษทศนิยม 5 ตำแหน่ง

items[].percent_nav

number

%NAV ปัดเศษทศนิยม 5 ตำแหน่ง (เนื่องจากการปัดเศษ อาจทำให้สัดส่วนรวมเกิน 100% ได้ถึง 100.20% ของ NAV)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 19. สัดส่วนการลงทุนของกองทุนรวมตามประเภทสินทรัพย์ ณ วันทำการสุดท้ายของเดือน

ข้อมูลสัดส่วนการลงทุนของกองทุนรวม ณ วันทำการสุดท้ายของเดือน โดยจำแนกตามกลุ่มสินทรัพย์และหนี้สินของกองทุน (เช่น กลุ่มเงินฝากธนาคาร กลุ่มหุ้น กลุ่มหน่วยลงทุน เป็นต้น) และแสดงมูลค่าตลาด (บาท) และสัดส่วนการลงทุนต่อมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV)

[!NOTE] ข้อมูลเป็นข้อมูลรายเดือนย้อนหลัง 3 ปี โดยงวดข้อมูลล่าสุดจะมีระยะเวลาในการเปิดเผย (lag time) 45 วันภายหลังวันทำการสุดท้ายของเดือน ผู้ใช้งานสามารถดึงข้อมูลงวดที่ต้องการได้ผ่านพารามิเตอร์ period_start และ period_end โดยข้อมูลแต่ละแถวจะระบุงวดข้อมูล (period ในรูปแบบ YYYYMM) กำกับเพื่อระบุช่วงเวลาที่ข้อมูลนั้นมีผล

### Endpoint

```
GET/v2/fund/outstanding/portfolio-asset-type
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_period

string

ระบุงวดข้อมูลแรกที่ต้องการดึงข้อมูล (รูปแบบ: YYYYMM) หมายเหตุ: หากต้องการดึงข้อมูลงวดเดียว ให้ระบุ period_start และ period_end เป็นงวดเดียวกัน

end_period

string

ระบุงวดข้อมูลสุดท้ายที่ต้องการดึงข้อมูล (รูปแบบ: YYYYMM) หมายเหตุ: หากต้องการดึงข้อมูลงวดเดียว ให้ระบุ period_start และ period_end เป็นงวดเดียวกัน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].assetliab_code

string

รหัสประเภทการลงทุน

items[].assetliab_desc

string

ประเภทการลงทุน

items[].market_value

number

มูลค่าตลาด

items[].percent_nav

number

สัดส่วนต่อมูลค่าสินทรัพย์สุทธิ



### 20. มูลค่าทรัพย์สินสุทธิ (NAV) ของกองทุนรวมรายวัน

ข้อมูลมูลค่าหน่วยลงทุน (Net Asset Value: NAV) ของกองทุนรวมในรูปแบบรายวัน โดยแสดงรายละเอียดจำนวนมูลค่าทรัพย์สินสุทธิของกองทุน (Net Asset), มูลค่าหน่วยลงทุน (NAV per unit), ราคาซื้อ–ขายปกติ และราคาซื้อ–ขายสำหรับการสับเปลี่ยนหน่วยลงทุน (Switching)

[!NOTE] ผู้ใช้งานสามารถค้นหาข้อมูลเฉพาะกองทุนหรือช่วงวันที่ต้องการได้ผ่านพารามิเตอร์ proj_id, nav_date_start, และ nav_date_end

### Endpoint

```
GET/v2/fund/daily-info/nav
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

start_nav_date

date

ระบุวันที่เริ่มต้นของ NAV ที่ต้องการดึงข้อมูล (รูปแบบ: YYYY-MM-DD)

end_nav_date

date

ระบุวันที่สิ้นสุดของ NAV ที่ต้องการดึงข้อมูล (รูปแบบ: YYYY-MM-DD)

fund_class_name

string

ชื่อชนิดหน่วยลงทุน

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].nav_date

date

วันที่ NAV (YYYY-MM-DD)

items[].fund_class_name

string

ชื่อย่อชนิดหน่วยลงทุน (Class Fund) หมายเหตุ: เป็น "main" ถ้าเป็นกองทุนที่ไม่ใช่ Class Fund

items[].net_asset

number

มูลค่าทรัพย์สินสุทธิ (บาท)

items[].last_val

number

มูลค่าหน่วยลงทุน (บาท/หน่วย)

items[].unique_id

string

รหัสอ้างอิงบริษัทจัดการที่เป็นผู้ส่งข้อมูล

items[].sell_price

number

ราคาขาย (บาท/หน่วย)

items[].buy_price

number

ราคาซื้อคืน (บาท/หน่วย)

items[].sell_swap_price

number

ราคาขายสับเปลี่ยน (บาท/หน่วย)

items[].buy_swap_price

number

ราคาซื้อคืนสับเปลี่ยน (บาท/หน่วย)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด



### 21. ประวัติการจ่ายเงินปันผลของกองทุนรวม

ข้อมูลประวัติการจ่ายเงินปันผลของกองทุนรวม โดยแสดงข้อมูลวันที่ปิดสมุดทะเบียน (Book Close Date), วันที่จ่ายเงินปันผล (Dividend Date) และจำนวนเงินปันผลต่อหน่วย (Dividend Value)

[!NOTE] ผลลัพธ์มีเฉพาะข้อมูลที่มีวันที่ปิดสมุดทะเบียน และวันที่จ่ายเงินปันผลครบถ้วนเท่านั้น

### Endpoint

```
GET/v2/fund/daily-info/dividend-history
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor

string

ค่า cursor ล่าสุดที่ได้รับจากการตอบกลับก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

proj_id

string

ระบุ proj_id เพื่อดึงข้อมูลของกองทุน 1 กอง

### Response

application/json

message

string

ข้อความสถานะของการเรียก API

page_size

number

จำนวนรายการที่ส่งกลับต่อครั้ง

next_cursor

string

ค่า cursor ที่ได้รับจาก Response ล่าสุด (กรณีที่ค่า next_cursor = "" หมายถึงระบบส่งข้อมูลให้ครบทั้งหมดแล้ว ไม่มีหน้าถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].unique_id

string

รหัสอ้างอิงบริษัทจัดการที่เป็นผู้ส่งข้อมูล

items[].proj_id

string

เลขที่โครงการ({Type}{ID}_YYYY)

items[].class_abbr_name

string

ชื่อกองทุน

items[].book_close_date

date

วันที่ปิดสมุดทะเบียน (YYYY-MM-DD)

items[].dividend_date

date

วันที่จ่ายเงินปันผล (YYYY-MM-DD)

items[].dividend_value

number

เงินปันผลต่อหน่วย (บาท)

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด