### 1. รายชื่อบริษัทจัดการกองทุน (บลจ.)

ข้อมูลรายชื่อบริษัทจัดการกองทุน (บลจ.) ที่อยู่ภายใต้การกำกับดูแลของสำนักงานก.ล.ต.

[!NOTE] สามารถนำรหัสบริษัทหลักทรัพย์จัดการกองทุน (unique_id) ไปใช้ร่วมกับ PVD API ข้ออื่น เช่น ข้อ 02. กองทุนภายใต้การบริหารจัดการของบริษัทหลักทรัพย์จัดการกองทุน เพื่อค้นหากองทุนที่บลจ.นั้น ๆ บริหารดูแล

### Endpoint

```
GET/v1/pvd/factsheet/amc
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601)

items[].unique_id

string

รหัสนิติบุคคลบริษัทจัดการ

items[].name_th

string

ชื่อนิติบุคคลบริษัทจัดการ (ไทย)

items[].name_en

string

ชื่อนิติบุคคลบริษัทจัดการ (อังกฤษ)

items[].abbr_name

string

ชื่อย่อนิติบุคคลบริษัทจัดการ



### 2. กองทุนสำรองเลี้ยงชีพภายใต้การบริหารจัดการของบริษัทหลักทรัพย์จัดการกองทุน

ข้อมูลกองทุนสำรองเลี้ยงชีพภายใต้การบริหารจัดการของแต่ละบริษัทหลักทรัพย์จัดการกองทุน (บลจ.) พร้อมลักษณะทั่วไปของแต่ละกองทุน เช่น สถานะกองทุน ประเภทกองทุน

[!NOTE] หากต้องการดึงข้อมูลเฉพาะกองที่ยังมีสถานะ active อยู่ในปัจจุบัน (กำลังอยู่ระหว่างเสนอขาย หรือ จดทะเบียน) ให้ผู้ใช้งานทำการกรองผลลัพธ์จาก API ข้อนี้ด้วยคอลัมน์ fund_status ที่มีค่าเป็น 'SE' และ 'RG' ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{unique_id}/fund
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสบริษัทหลักทรัพย์จัดการกองทุน

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY) เช่น V0001_2544

items[].regis_id

string

เลขที่จดทะเบียนกองทุน

items[].regis_date

date|string

วันที่จดทะเบียนกองทุน (YYYY-MM-DD — อาจใช้ พ.ศ.)

items[].cancel_date

date|string

วันที่เลิกกองทุน (YYYY-MM-DD) หรือ "-" หากยังไม่เลิก

items[].proj_name_th

string

ชื่อโครงการจัดการ (ไทย)

items[].fund_type

string

ประเภทกองทุน:

- PF =กองทุนร่วม
- PM =Master Pooled Fund

items[].fund_status

string

สถานะกองทุน:

- SE =Filing
- EX =หมดเวลาเสนอขาย
- RG =จดทะเบียน
- CA =เลิกโครงการ
- LI =จดทะเบียนเลิก

items[].unique_id

string

รหัสบริษัทหลักทรัพย์จัดการกองทุน



### 3. กองทุนสำรองเลี้ยงชีพภายใต้การบริหารจัดการของบริษัทหลักทรัพย์จัดการกองทุน

ข้อมูลกองทุนสำรองเลี้ยงชีพภายใต้การบริหารจัดการของแต่ละบริษัทหลักทรัพย์จัดการกองทุน (บลจ.) พร้อมลักษณะทั่วไปของแต่ละกองทุน เช่น สถานะกองทุน ประเภทกองทุน

[!NOTE] หากต้องการดึงข้อมูลเฉพาะกองที่ยังมีสถานะ active อยู่ในปัจจุบัน (กำลังอยู่ระหว่างเสนอขาย หรือ จดทะเบียน) ให้ผู้ใช้งานทำการกรองผลลัพธ์จาก API ข้อนี้ด้วยคอลัมน์ fund_status ที่มีค่าเป็น 'SE' และ 'RG' ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
POST/v1/pvd/factsheet/fund
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Request Body

FundNamestring

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY) เช่น V0001_2544

items[].regis_id

string

เลขที่จดทะเบียนกองทุน

items[].regis_date

date|string

วันที่จดทะเบียนกองทุน (YYYY-MM-DD — อาจใช้ พ.ศ.)

items[].cancel_date

date|string

วันที่เลิกกองทุน (YYYY-MM-DD) หรือ "-" หากยังไม่เลิก

items[].proj_name_th

string

ชื่อโครงการจัดการ (ไทย)

items[].fund_type

string

ประเภทกองทุน:

- PF =กองทุนร่วม
- PM =Master Pooled Fund

items[].fund_status

string

สถานะกองทุน:

- SE =Filing
- EX =หมดเวลาเสนอขาย
- RG =จดทะเบียน
- CA =เลิกโครงการ
- LI =จดทะเบียนเลิก

items[].unique_id

string

รหัสบริษัทหลักทรัพย์จัดการกองทุน



### 4. นโยบายการลงทุนของกองทุนสำรองเลี้ยงชีพ

ข้อมูลนโยบายการลงทุน นโยบายการลงทุนย่อย ระดับความเสี่ยง ความเสี่ยงต่างประเทศ ประเภทกองทุนตาม AIMC Category และวัตถุประสงค์การลงทุนกองทุนสำรองเลี้ยงชีพ

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/policy
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].sub_policy_id

string

รหัสนโยบายการลงทุนย่อย

items[].sub_policy_name

string

ชื่อนโยบายการลงทุนย่อย

items[].sub_policy_start_date

date|string

วันจัดตั้งนโยบายการลงทุนย่อย (YYYY-MM-DD, อาจเป็น พ.ศ.)

items[].sub_policy_inception_date

date|string

วันที่เริ่มต้นบริหารนโยบายย่อย (YYYY-MM-DD, อาจเป็น พ.ศ.)

items[].sub_policy_end_date

date|string

วันยกเลิกนโยบายการลงทุนย่อย (YYYY-MM-DD) หรือ "-" หากยังไม่สิ้นสุด

items[].sub_policy_nav_start

number

NAV ณ วันเริ่มต้น

items[].risk_level

string

ระดับความเสี่ยง:

- RS1 =ต่ำ
- RS2–RS5 =ปานกลางค่อนไปทางต่ำ
- RS6–RS7 =สูง
- RS8 =สูงมาก

items[].foreign_risk_level

string

ความเสี่ยงต่างประเทศ:

- 01 =ลงทุนต่างประเทศเท่านั้น
- 02 =ทั้งในและต่างประเทศ
- 03 =ในประเทศเท่านั้น

items[].aimc_type

string

ประเภทกองทุนตาม AIMC Category

items[].aimc_description

string

คำอธิบายการจัดประเภทกองทุนตาม AIMC Category

items[].objective

string

วัตถุประสงค์การลงทุน

items[].mf_invest_flag

string

PVD ลงทุนในกองทุนรวมอื่นหรือไม่ (Y=ใช่, N=ไม่ใช่)

items[].new_member_offer

string

เปิดเสนอขายให้สมาชิกใหม่หรือไม่ (Y=เสนอ, N=ไม่เสนอ)



### 5. ผลตอบแทนย้อนหลังของกองทุนสำรองเลี้ยงชีพ

ข้อมูลผลตอบแทนย้อนหลังในแต่ละกองทุนสำรองเลี้ยงชีพในระดับแต่ละนโยบายการลงทุน และนโยบายการลงทุนย่อย

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/return
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_updated

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].seq

number

ลำดับที่: 1–10 = ผลตอบแทนย้อนหลังปีที่ 1–10, 11 = Since inception, 12 = YTD

items[].return_year

string

ประเภทผลตอบแทนย้อนหลัง (เช่น "ปีที่ 1", "Since inception", "YTD")

items[].return_rate

number|string

ผลตอบแทนย้อนหลัง (หน่วยเป็น %, ใส่เป็นตัวเลข ไม่ต้องมีสัญลักษณ์ %; อาจติดลบได้)



### 6. ผลตอบแทนย้อนหลังแบบปักหมุดของกองทุนสำรองเลี้ยงชีพ

ข้อมูลผลตอบแทนย้อนหลังแบบปักหมุดในแต่ละกองทุนสำรองเลี้ยงชีพในระดับแต่ละนโยบายการลงทุน และนโยบายการลงทุนย่อย

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/trailreturn
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_updated

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].seq

number

ลำดับที่

items[].return_year

string

ประเภทผลตอบแทนย้อนหลัง (เช่น เดือนที่ 3, ปีที่ 1, ปีที่ 3 ฯลฯ)

items[].return_rate

number

ผลตอบแทนย้อนหลัง (หน่วยเป็น %)



### 7. ค่าธรรมเนียมของกองทุนสำรองเลี้ยงชีพ

ข้อมูลค่าธรรมเนียมของกองทุนสำรองเลี้ยงชีพในระดับแต่ละนโยบายการลงทุน และนโยบายการลงทุนย่อย ได้แก่ ค่าธรรมเนียมการจัดการ ค่าธรรมเนียมรวม ค่าธรรมเนียมรวมสูงสุดที่เก็บจริงในระดับกองทุน และค่าธรรมเนียมรวมต่ำสุดที่เก็บจริงในระดับกองทุน

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/fee
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_updated

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].seq

number

ลำดับที่

items[].fee_type_desc

string

ชื่อประเภทค่าธรรมเนียม:

- ManagementFee =ค่าธรรมเนียมการจัดการของ PVD (% ต่อปีของ NAV)
- TotalFee =ค่าธรรมเนียมรวมของ PVD (% ต่อปีของ NAV)
- TotalFeeMax =ค่าธรรมเนียมรวมสูงสุดที่เก็บจริงระดับกองทุนรวม
- TotalFeeMin =ค่าธรรมเนียมรวมต่ำสุดที่เก็บจริงระดับกองทุนรวม

items[].fee_rate

number

อัตราค่าธรรมเนียม (หน่วยเป็น % ต่อปีของ NAV; เป็นตัวเลขทศนิยมได้)



### 8. สัดส่วนการลงทุนของกองทุนสำรองเลี้ยงชีพ

ข้อมูลสัดส่วนการลงทุนจำแนกตามประเภททรัพย์สินที่ลงทุนของกองทุนสำรองเลี้ยงชีพ โดยจำแนกตามกลุ่มสินทรัพย์และหนี้สินของกองทุน (เช่น กลุ่มหุ้น กลุ่มหุ้นกู้ กลุ่มหน่วยลงทุน กลุ่มพันธบัตรรัฐบาล เป็นต้น) และแสดงสัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV) พร้อมมูลค่าตลาดในแต่ละกลุ่มประเภททรัพย์สิน

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund) ข้อมูลเป็นข้อมูลรายเดือนย้อนหลัง โดยงวดข้อมูลล่าสุดจะมีระยะเวลาในการเปิดเผย (lag time) 45 วันภายหลังวันทำการสุดท้ายของเดือน

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/PVDFullPort/{period}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

periodrequired

string

งวดข้อมูล (YYYYMM)

### Response

application/json

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].assetliab_code

string

รหัสประเภทการลงทุน:

- 101 =หุ้น
- 103 =หุ้นกู้
- 108 =หน่วยลงทุน
- 110 =ใบสำคัญแสดงสิทธิ
- 201 =เงินฝาก/PN/BE
- 206 =พันธบัตรรัฐบาล
- 401 =ตราสารอนุพันธ์
- 450 =ทองคำแท่ง
- 700 =สินทรัพย์/หนี้สินอื่นๆ
- 903 =รวม

items[].assetliab_name_th

string

ชื่อประเภทการลงทุน (ภาษาไทย)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].market_value

number

มูลค่าตลาด

items[].percent_nav

number

สัดส่วนต่อมูลค่าสินทรัพย์สุทธิ



### 9. ข้อมูลเชิงสถิติของกองทุนสำรองเลี้ยงชีพ

ข้อมูลสถิติสำคัญของกองทุนสำรองเลี้ยงชีพ (Provident Fund Statistics) ในแต่ละกองทุน เช่น อัตราหมุนเวียนพอร์ต (Portfolio Turnover Ratio), Maximum Drawdown, Sharpe Ratio, Beta, Alpha, Yield to Maturity เป็นต้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/statistics
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].max_drawdown

number

Maximum Drawdown (%)

items[].tracking_error

number|null

Tracking Error (%)

items[].recovering_period

number

Recovering Period (Day)

items[].port_turnover

number

Portfolio Turnover Ratio

items[].sharpe_ratio

number|null

Sharpe Ratio

items[].alpha

number|null

Alpha (%)

items[].fx_hedging

number|null

FX Hedging (%)

items[].beta

number|null

Beta

items[].port_duration

number

Portfolio Duration (Day)

items[].yield_to_maturity

number

Yield to Maturity (%)



### 10. สัดส่วนการลงทุนตามประเภททรัพย์สิน 5 อันดับแรก ตามรายนโยบายย่อย

ข้อมูลประเภททรัพย์สินที่กองทุนสำรองเลี้ยงชีพลงทุน 5 อันดับแรกตามนโยบายย่อยของแต่ละกองทุน โดยแสดงประเภททรัพย์สิน ลำดับอันดับการลงทุน และสัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV) ในช่วงเวลานั้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/top5/assettype
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].asset_allocation_seq

number

ลำดับการลงทุน (1-5)

items[].assetliab_name_th

string

ชื่อประเภททรัพย์สินที่ลงทุน (ภาษาไทย)

items[].asset_ratio

number

% สัดส่วนของประเภททรัพย์สินที่ลงทุน



### 11. สัดส่วนการลงทุนของหลักทรัพย์ 5 อันดับแรก ตามรายนโยบายย่อย

ข้อมูลทรัพย์สินหรือหลักทรัพย์ที่กองทุนสำรองเลี้ยงชีพลงทุน 5 อันดับแรกตามนโยบายย่อยของแต่ละกองทุน โดยแสดงชื่อทรัพย์สินหรือหลักทรัพย์ (secur_name) ลำดับอันดับการลงทุน (secur_seq) สัดส่วนการลงทุนคิดเป็นร้อยละของมูลค่าสินทรัพย์สุทธิของกองทุน (%NAV) (secur_invest_size) อันดับความน่าเชื่อถือของหลักทรัพย์ในกรณีตราสารหนี้ (secur_credit_rating) และ ISIN Code ของกองทุนหลักสำหรับนโยบายที่มีการลงทุนตรงในกองทุนต่างประเทศ (secur_isin_code) ในช่วงเวลานั้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/top5/securities
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].secur_seq

number

ลำดับการลงทุน (1-5)

items[].secur_invest_size

number

% สัดส่วนการลงทุนของหลักทรัพย์

items[].secur_name

string

ชื่อหลักทรัพย์

items[].secur_credit_rating

string|null

อันดับความน่าเชื่อถือของหลักทรัพย์ (ตราสารหนี้)

items[].secur_isin_code

string|null

ISIN Code ของกองทุนหลัก (ถ้ามี)



### 12. การจัดสรรการลงทุนในต่างประเทศ 5 อันดับแรก (เฉพาะกรณีลงทุนตรง)

ข้อมูลประเทศที่กองทุนสำรองเลี้ยงชีพลงทุนโดยตรง 5 อันดับแรกตามนโยบายย่อยของแต่ละกองทุน โดยแสดงประเทศที่ลงทุน (country) ลำดับอันดับการลงทุน (secur_seq_country) และสัดส่วนประเทศที่ลงทุน (country_size) ในช่วงเวลานั้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/top5/foreign
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].secur_seq_country

number

ลำดับการลงทุน (1-5)

items[].country

string|null

ประเทศที่ลงทุน

items[].country_size

number|null

% สัดส่วนประเทศที่ลงทุน



### 13. การจัดสรรการลงทุนในกลุ่มอุตสาหกรรม 5 อันดับแรก (เฉพาะนโยบายตราสารทุนที่เป็นการลงทุนตรง)

ข้อมูลอุตสาหกรรมที่กองทุนสำรองเลี้ยงชีพ (เฉพาะกองที่มีนโยบายเป็นตราสารทุน) ลงทุนโดยตรง 5 อันดับแรกตามนโยบายย่อยของแต่ละกองทุน โดยแสดงกลุ่มอุตสาหกรรมที่ลงทุน (industry) ลำดับอันดับการลงทุน (secur_seq_industry) และสัดส่วนกลุ่มอุตสาหกรรมที่ลงทุน (industry_size) ในช่วงเวลานั้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/top5/industry
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].secur_seq_industry

number

ลำดับการลงทุน (1-5)

items[].industry

string|null

กลุ่มอุตสาหกรรมที่ลงทุน

items[].industry_size

number|null

% สัดส่วนกลุ่มอุตสาหกรรมที่ลงทุน



### 14. การจัดสรรการลงทุนในผู้ออกตราสาร 5 อันดับแรก (เฉพาะนโยบายตราสารหนี้ที่เป็นการลงทุนตรง)

ข้อมูลผู้ออกตราสารที่กองทุนสำรองเลี้ยงชีพ (เฉพาะกองที่มีนโยบายเป็นตราสารหนี้) ลงทุนโดยตรง 5 อันดับแรกตามนโยบายย่อยของแต่ละกองทุน โดยแสดงผู้ออกตราสารที่ลงทุน (issuer) ลำดับอันดับการลงทุน (secur_seq_issuer) และสัดส่วนของผู้ออกตราสาร (issuer_size) ในช่วงเวลานั้น

[!NOTE] ข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/top5/issuer
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].period

string

งวดข้อมูล (YYYYMM)

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].secur_seq_issuer

number

ลำดับการลงทุน (1-5)

items[].issuer

string

ชื่อผู้ออกตราสาร (issuer)

items[].issuer_size

number

% สัดส่วนของผู้ออกตราสาร



### 15. มูลค่าทรัพย์สินสุทธิ (NAV) ของกองทุนสำรองเลี้ยงชีพ ตามรายนโยบายย่อยรายเดือน

ข้อมูลมูลค่าหน่วยลงทุน (Net Asset Value: NAV) ของกองทุนสำรองเลี้ยงชีพในรูปแบบรายเดือน ตามรายนโยบายย่อย โดยแสดงรายละเอียดจำนวนมูลค่าทรัพย์สินสุทธิของกองทุน (net_asset), มูลค่าหน่วยลงทุน (net_asset_per_unit) และวันที่ NAV (nav_date)

[!NOTE] ข้อมูลเป็นข้อมูลรายเดือนย้อนหลัง 3 ปี โดยงวดข้อมูลล่าสุดจะมีระยะเวลาในการเปิดเผย (lag time) 60 วันภายหลังวันทำการสุดท้ายของเดือน โดยมีข้อมูลงวดแรกคือ 20240630 และเป็นข้อมูลเฉพาะกองทุนสำรองเลี้ยงชีพประเภทกองทุนหลายนายจ้างที่มีนโยบายเดียว (Pooled Fund) และกองทุนหลายนายจ้างที่มีหลายนโยบาย (Master Pooled Fund)

### Endpoint

```
GET/v1/pvd/factsheet/{proj_id}/nav/{nav_date}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

proj_idrequired

string

เลขที่โครงการ ({Type}{ID}_YYYY)

nav_daterequired

string

วันที่ของ NAV (YYYYMMDD) : YYYY คือ ปี ค.ศ. MM คือ เดือน และ DD คือ วันที่สุดท้ายของเดือน โดยแสดงข้อมูลย้อนหลังไม่เกิน 3 ปี และหลังสิ้นเดือนอย่างน้อย 60 วัน ข้อมูลงวดแรก คือ 20240630

### Response

application/json

items[].last_upd_date

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)

items[].proj_id

string

เลขที่โครงการ ({Type}{ID}_YYYY)

items[].policy_id

string

รหัสนโยบายการลงทุน

items[].policy_name

string

ชื่อนโยบายการลงทุน

items[].unique_sub_policy_id

string

รหัสนโยบายการลงทุนย่อย (ก.ล.ต.)

items[].nav_date

string

วันที่ NAV (YYYYMMDD)

items[].net_asset

number

มูลค่าทรัพย์สินสุทธิ (บาท)

items[].net_asset_per_unit

number

มูลค่าหน่วยลงทุน (บาท/หน่วย)