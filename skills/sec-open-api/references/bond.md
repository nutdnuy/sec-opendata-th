### 1. ชื่อผู้ออกตราสารหนี้

ข้อมูลรายชื่อผู้ออกตราสารหนี้

### Endpoint

```
GET/v2/bond/issuers
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

search

string

ค้นหาโดยเลขที่โครงการ ({Type}{ID}_YYYY) หรือชื่อย่อชนิดหน่วยลงทุน (Class Fund)

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

items[].company_id

string

รหัสบริษัท

items[].company_name_th

string

ชื่อบริษัทภาษาไทย

items[].company_name_en

string

ชื่อบริษัทภาษาอังกฤษ



### 2. ข้อมูลลักษณะทั่วไปของตราสารหนี้

ข้อมูลตราสารหนี้ที่ถูกออกโดยแต่ละผู้ออกตราสาร พร้อมลักษณะทั่วไปของแต่ละตราสาร เช่น ประเภทตราสาร ประเภทการเรียกไถ่ถอน การเสนอขาย การครบกำหนด เป็นต้น

### Endpoint

```
GET/v2/bond/features
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

search_term

string

ค้นหาแบบบางส่วน (partial search) จาก thaibma_symbol, isin_code และ company_id

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

ค่า cursor สำหรับหน้าถัดไป (ถ้าเป็นค่าว่างแปลว่าไม่มีข้อมูลถัดไป)

▼items

array<object>

รายการข้อมูลหลักที่ส่งกลับมา

items[].bond_id

string

รหัสตราสารหนี้

items[].company_id

string

รหัสบริษัท (อาจมีช่องว่างด้านท้าย)

items[].isin_code

string

รหัสตราสาร ISIN (อาจไม่มีข้อมูล)

items[].cfi_code

string

รหัสตราสาร CFI (อาจไม่มีข้อมูล)

items[].thaibma_symbol

string

รหัสตราสาร ThaiBMA (อาจไม่มีข้อมูล)

items[].bond_name_th

string

ชื่อตราสารหนี้ภาษาไทย

items[].bond_name_en

string

ชื่อตราสารหนี้ภาษาอังกฤษ

items[].bond_type

string

รหัสประเภทตราสารหนี้

items[].esg_bond_type

string

ประเภทตราสาร ESG (อาจไม่มีข้อมูล):

- GreenBond =ตราสารหนี้เพื่ออนุรักษ์สิ่งแวดล้อม
- SocialBond =ตราสารหนี้เพื่อพัฒนาสังคม
- SustainableBond =ตราสารหนี้เพื่อความยั่งยืน
- SustainabilityLinkBond =ตราสารหนี้ที่ส่งเสริมความยั่งยืน

items[].subordinated_type

string

รหัสประเภทการด้อยสิทธิ

items[].embedded_option

string

รหัสสิทธิเรียกไถ่ถอน:

- 001 =ผู้ออกมีสิทธิเรียกไถ่ถอนก่อนกำหนด (Call)
- 002 =ผู้ถือมีสิทธิเรียกไถ่ถอนก่อนกำหนด (Put)
- 003 =ผู้ออกและผู้ถือมีสิทธิเรียกไถ่ถอนก่อนกำหนด (Call & Put)
- 004 =ไม่มีสิทธิเรียกไถ่ถอนก่อนกำหนด
- 005 =อื่น ๆ
- 999 =ไม่ระบุ

items[].secured_type

string

รหัสประเภทการมีประกัน:

- 001 =มีประกัน
- 002 =ไม่มีประกัน
- 003 =มีประกันบางส่วน
- 999 =ไม่ระบุ

items[].offering.place

string

สถานที่เสนอขาย:

- T =ไทย
- F =ต่างประเทศ

items[].offering.target

string

กลุ่มเป้าหมาย

items[].offering.currency

string

สกุลเงิน

items[].offering.exchange_rate

number

อัตราแลกเปลี่ยน

items[].offering.unit

number

มูลค่าต่อหน่วย

items[].offering.value

number

มูลค่าการเสนอขายรวม

items[].offering.face_value

number

มูลค่าที่ตราไว้

items[].offering.objective

string

วัตถุประสงค์การใช้เงิน (อาจไม่มีข้อมูล):

- 1 =ขยายกำลังการผลิต/กิจการ
- 2 =ลงทุนโครงการใหม่
- 3 =ชำระหนี้เดิม
- 4 =เงินทุนหมุนเวียน
- 5 =ปรับปรุงกิจการ
- 6 =นับเป็นเงินกองทุนตามธนาคารแห่งประเทศไทย
- 7 =อื่นๆ

items[].offering.objective_other_detail

string

รายละเอียดวัตถุประสงค์เพิ่มเติม (อาจไม่มีข้อมูล)

items[].maturity.issue_date

datetime

วันที่ออกตราสาร

items[].maturity.maturity_date

datetime

วันที่ครบกำหนดไถ่ถอน

items[].maturity.age_type

string

ประเภทอายุ

items[].maturity.term_year

number

อายุ (ปี)

items[].maturity.term_month

number

อายุ (เดือน)

items[].maturity.term_day

number

อายุ (วัน)

items[].selling.begin_date

datetime

วันที่เริ่มขาย

items[].selling.close_date

datetime

วันที่สิ้นสุดการขาย

items[].selling.value

number

มูลค่าการขาย

items[].coupon.type

string

รหัสประเภทดอกเบี้ย

items[].coupon.rate

number

อัตราดอกเบี้ย (%)

items[].coupon.name_th

string

ชื่อประเภทดอกเบี้ย (ไทย)

items[].coupon.name_en

string

ชื่อประเภทดอกเบี้ย (อังกฤษ)

items[].redemption.type

string

รหัสประเภทการไถ่ถอน

items[].redemption.conditions

string

เงื่อนไขการไถ่ถอน

items[].embedded_option_info.name_en

string

ชื่อสิทธิ (EN)

items[].secured_info.name_en

string

คำอธิบายหลักประกัน (EN)

items[].security_type.name_en

string

ชื่อประเภทตราสาร (EN)

items[].market.desc

string

คำอธิบายตลาด

items[].offer_type.name_en

string

ประเภทการเสนอขาย (EN)

items[].currency_info.name_en

string

ชื่อสกุลเงิน (EN)



### 3. การจัดอันดับความน่าเชื่อถือของตราสารหนี้ ตามช่วงเวลา

ข้อมูลอันดับความน่าเชื่อถือของแต่ละตราสารหนี้ในแต่ละช่วงเวลา

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่อันดับความน่าเชื่อถือของแต่ละตราสารหนี้นั้นมีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่อันดับความน่าเชื่อถือของตราสารนั้นเริ่มมีผลบังคับใช้ (efft_date) และ วันหมดอายุ (exp_date)

### Endpoint

```
GET/v2/bond/credit-ratings
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

bond_id

string

ระบุ bond_id เพื่อดึงข้อมูลของตราสาร 1 ตัว

efft_date

string

ระบุวันที่เริ่มต้นที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

exp_date

string

ระบุวันที่สิ้นสุดที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

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

items[].bond_id

string

รหัสของตราสารหนี้

items[].efft_date

date

วันที่เริ่มมีผลบังคับใช้

items[].exp_date

date

วันหมดอายุ (ถ้ามี)

items[].rating_code

string

อันดับความน่าเชื่อถือของตราสาร



### 4. มูลค่าคงค้างของตราสารหนี้ ตามช่วงเวลา

ข้อมูลมูลค่าคงค้างของแต่ละตราสารหนี้ในแต่ละช่วงเวลา

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่มูลค่าคงค้างของตราสารหนี้นั้นมีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่มูลค่าคงค้างของตราสารหนี้เริ่มมีผล (efft_date) และ วันที่สิ้นสุดมีผล(exp_date)

### Endpoint

```
GET/v2/bond/outstanding-values
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Query parameters

next_cursor



ค่า cursor ล่าสุดที่ได้รับจาก response ก่อนหน้า (ใช้สำหรับโหลดข้อมูลเพิ่มเติม)

page_size

integer

จำนวนรายการข้อมูลต่อหน้าที่ต้องการให้ระบบส่งกลับ (ค่าเริ่มต้น 100) โดยรองรับค่าตั้งแต่ 1 ถึง 100 รายการ

bond_id



ระบุ bond_id เพื่อดึงข้อมูลของตราสาร 1 ตัว

efft_date



ระบุวันที่เริ่มต้นที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

exp_date



ระบุวันที่สิ้นสุดที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

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

items[].bond_id

string

รหัสตราสารหนี้

items[].efft_date

date

วันที่เริ่มมีผล

items[].exp_date

date

วันที่สิ้นสุดมีผล

items[].outstanding_value_mm_baht

number

มูลค่าคงค้างของตราสารหนี้ หน่วย:ล้านบาท



### 5. ผู้เกี่ยวข้องกับตราสารหนี้ ตามช่วงเวลา

ข้อมูลผู้เกี่ยวข้องกับตราสารหนี้ในแต่ละช่วงเวลา

[!NOTE] ข้อมูลในชุดนี้เป็นข้อมูลตามช่วงเวลาที่ผู้เกี่ยวข้องกับตราสารหนี้นั้นมีผล โดยแต่ละแถวจะแสดงข้อมูลตามวันที่ผู้เกี่ยวข้องกับตราสารหนี้เริ่มมีผล (efft_date) และ วันที่สิ้นสุดมีผล (exp_date)

### Endpoint

```
GET/v2/bond/involve-parties
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

bond_id

string

ระบุ bond_id เพื่อดึงข้อมูลของตราสาร 1 ตัว

efft_date

string

ระบุวันที่เริ่มต้นที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

exp_date

string

ระบุวันที่สิ้นสุดที่ rating มีผล (รูปแบบ: YYYY-MM-DD)

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

items[].bond_id

string

รหัสตราสารหนี้

items[].company_id

string

รหัสบริษัท

items[].function_type

string

หน้าที่ของบริษัท (role)

items[].function_type_name_th

string

ชื่อหน้าที่ (ภาษาไทย)

items[].function_type_name_en

string

ชื่อหน้าที่ (ภาษาอังกฤษ)

items[].efft_date

date

วันที่เริ่มมีผล (YYYY-MM-DD)

items[].exp_date

date

วันที่สิ้นสุดมีผล (YYYY-MM-DD), null หมายถึงยังมีผลอยู่



### 6. มูลค่าตราสารหนี้ในผู้ลงทุนแต่ละประเภท

ข้อมูลมูลค่าตราสารหนี้ในผู้ลงทุนแต่ละประเภท ได้แก่ นิติบุคคลไทย/ต่างประเทศ ผู้ลงทันสถาบันไทย/ต่างประเทศ ผู้ลงทุนรายใหญ่ไทย/ต่างประเทศ และ ผุ้ลงทุนรายย่อยไทย/ต่างประเทศ

### Endpoint

```
GET/v2/bond/investor-holdings
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

bond_id

string

ระบุ bond_id เพื่อดึงข้อมูลของตราสาร 1 ตัว

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

items[].bond_id

string

รหัสตราสารหนี้

items[].thai_juristic_value_baht

number

มูลค่าที่ถือโดยนิติบุคคลไทย

items[].thai_institution_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนสถาบันไทย

items[].thai_hnw_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนรายใหญ่ไทย

items[].thai_person_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนรายย่อยไทย

items[].foreign_juristic_value_baht

number

มูลค่าที่ถือโดยนิติบุคคลต่างประเทศ

items[].foreign_institution_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนสถาบันต่างประเทศ

items[].foreign_hnw_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนรายใหญ่ต่างประเทศ

items[].foreign_person_value_baht

number

มูลค่าที่ถือโดยผู้ลงทุนรายย่อยต่างประเทศ