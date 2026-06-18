### 1. บุคคลที่ได้รับความเห็นชอบจากสำนักงาน

ข้อมูลบุคคลที่ได้รับความเห็นชอบจากสำนักงาน (Approval of personnel in capital market industry) ที่อยู่ภายใต้การกำกับของ ก.ล.ต. โดยสามารถสืบค้นจากส่วนหนึ่งของชื่อหรือเลขทะเบียน

### Endpoint

```
POST/v1/license-check/licensee/person
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Request Body

Namestring

regis_sale_nostring

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].unique_id

string

รหัสบุคคล

items[].regis_sale_no

string

เลขทะเบียน (เฉพาะผู้ที่ได้รับ/เคยได้รับความเห็นชอบ ผู้แนะนำ/นักวิเคราะห์/ผู้วางแผนการลงทุน เท่านั้น)

items[].prefix_th

string

คำนำหน้าชื่อ (ภาษาไทย)

items[].givenname_th

string

ชื่อบุคคล (ภาษาไทย)

items[].surname_th

string

นามสกุล (ภาษาไทย)

items[].prefix_en

string

คำนำหน้าชื่อ (ภาษาอังกฤษ)

items[].givenname_en

string

ชื่อบุคคล (ภาษาอังกฤษ)

items[].surname_en

string

นามสกุล (ภาษาอังกฤษ)

### 2. นิติบุคคลที่ได้รับใบอนุญาตจากสำนักงาน หรือ จดทะเบียนประกอบธุรกิจกับสำนักงาน

ข้อมูลนิติบุคคลที่เคยได้รับใบอนุญาตจากสำนักงาน หรือ เคยจดทะเบียนประกอบธุรกิจกับสำนักงาน ก.ล.ต.

### Endpoint

```
GET/v1/license-check/licensee/company
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].unique_id

string

รหัสนิติบุคคล

items[].name_th

string

ชื่อนิติบุคคล (ภาษาไทย)

items[].name_en

string

ชื่อนิติบุคคล (ภาษาอังกฤษ)



### 3. นิติบุคคลที่ได้รับใบอนุญาตจากสำนักงาน หรือ จดทะเบียนประกอบธุรกิจกับสำนักงาน

ข้อมูลนิติบุคคลที่เคยได้รับใบอนุญาตจากสำนักงาน หรือ เคยจดทะเบียนประกอบธุรกิจกับสำนักงาน ก.ล.ต. โดยสามารถสืบค้นจากส่วนหนึ่งของชื่อ

### Endpoint

```
POST/v1/license-check/licensee/company
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Request Body

Namestring

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].unique_id

string

รหัสนิติบุคคล

items[].name_th

string

ชื่อนิติบุคคล (ภาษาไทย)

items[].name_en

string

ชื่อนิติบุคคล (ภาษาอังกฤษ)



### 4. ประเภทความเห็นชอบของบุคคลที่ได้รับความเห็นชอบจากสำนักงาน

ข้อมูลรายละเอียดการได้รับความเห็นชอบของบุคคลจากสำนักงาน ก.ล.ต. โดยแสดงรหัสประเภทการได้รับความเห็นชอบ (lic_code) วันที่ได้รับความเห็นชอบ (effective_date) และวันที่หมดอายุความเห็นชอบ (expire_date)

### Endpoint

```
GET/v1/license-check/licensee/person/{unique_id}/license
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

Person's Unique Id

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].regis_sale_no

string

เลขทะเบียน (เฉพาะผู้ที่ได้รับ/เคยได้รับความเห็นชอบ ผู้แนะนำ/นักวิเคราะห์/ผู้วางแผนการลงทุน เท่านั้น)

items[].lic_code

string

รหัสประเภทการได้รับความเห็นชอบ

items[].lic_name_th

string

ชื่อประเภทการได้รับความเห็นชอบ (ภาษาไทย)

items[].lic_name_en

string

ชื่อประเภทการได้รับความเห็นชอบ (ภาษาอังกฤษ)

items[].effective_date

date

วันที่ได้รับความเห็นชอบ (YYYY-MM-DD)

items[].expire_date

date|string

วันที่หมดอายุความเห็นชอบ (YYYY-MM-DD) — ค่าว่าง "" หมายถึงไม่มีวันหมดอายุ

items[].privilege_type

string

MD=ใช้สิทธิผู้บริหาร, FM=ทะเบียนผู้มีคุณสมบัติเป็นผู้จัดการกองทุน, ค่าว่าง "" = ไม่ได้ใช้สิทธิ



### 5. การปฏิบัติหน้าที่ของบุคคลภายใต้นิติบุคคล

ข้อมูลการปฏิบัติหน้าที่ของบุคคลภายใต้นิติบุคคลนั้น ๆ ในมุมมองของนิติบุคคล เพื่อระบุว่านิติบุคคลแต่ละแห่งมีบุคคลใดปฏิบัติหน้าที่อยู่ พร้อมรหัสฐานะการปฏิบัติหน้าที่ (lic_action_code) และช่วงเวลาการปฏิบัติหน้าที่ (action_start_date และ action_end_date)

[!NOTE] แสดงผลลัพธ์เฉพาะรายการปฏิบัติหน้าที่ที่มีผลในปัจจุบัน

### Endpoint

```
GET/v1/license-check/licensee/company/{unique_id}/personnel
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสนิติบุคคล

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].company_unique_id

string

รหัสนิติบุคคล

items[].person_unique_id

string

รหัสบุคคล

items[].lic_action_code

string

รหัสฐานะการปฏิบัติหน้าที่

items[].lic_action_name_th

string

ชื่อฐานะการปฏิบัติหน้าที่ (ภาษาไทย)

items[].lic_action_name_en

string

ชื่อฐานะการปฏิบัติหน้าที่ (ภาษาอังกฤษ)

items[].action_start_date

date

วันที่เริ่มปฏิบัติหน้าที่ (YYYY-MM-DD)

items[].action_end_date

date|string

วันที่สิ้นสุดการปฏิบัติหน้าที่ (YYYY-MM-DD) — ค่าว่าง "" หมายถึงยังคงปฏิบัติหน้าที่อยู่



### 6. การปฏิบัติหน้าที่บุคคลที่ได้รับความเห็นชอบจากสำนักงาน ในแต่ละนิติบุคคล

ข้อมูลการปฏิบัติหน้าที่ของบุคคลที่ได้รับความเห็นชอบจากสำนักงาน ก.ล.ต. ในแต่ละนิติบุคคล ในมุมมองของบุคคล เพื่อระบุว่าบุคคลแต่ละรายปฏิบัติหน้าที่อยู่ภายใต้นิติบุคคลใดบ้าง พร้อมรหัสฐานะการปฏิบัติหน้าที่ (lic_action_code) และช่วงเวลาการปฏิบัติหน้าที่ (action_start_date และ action_end_date)

[!NOTE] แสดงผลลัพธ์เฉพาะรายการปฏิบัติหน้าที่ที่มีผลในปัจจุบัน

### Endpoint

```
GET/v1/license-check/licensee/person/{unique_id}/work_info
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสบุคคล

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].company_unique_id

string

รหัสนิติบุคคล

items[].person_unique_id

string

รหัสบุคคล

items[].lic_action_code

string

รหัสฐานะการปฏิบัติหน้าที่

items[].lic_action_name_th

string

ชื่อฐานะการปฏิบัติหน้าที่ (ภาษาไทย)

items[].lic_action_name_en

string

ชื่อฐานะการปฏิบัติหน้าที่ (ภาษาอังกฤษ)

items[].action_start_date

date

วันที่เริ่มปฏิบัติหน้าที่ (YYYY-MM-DD)

items[].action_end_date

date|string

วันที่สิ้นสุดการปฏิบัติหน้าที่ (YYYY-MM-DD) — ค่าว่าง "" = ยังคงปฏิบัติหน้าที่



### 7. ประเภทใบอนุญาตหรือการจดทะเบียนของนิติบุคคลที่ได้รับใบอนุญาตจากสำนักงาน

ข้อมูลประเภทใบอนุญาตหรือการจดทะเบียนของนิติบุคคลที่ได้รับใบอนุญาตจากสำนักงาน

### Endpoint

```
GET/v1/license-check/licensee/company/{unique_id}/license
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสนิติบุคคล

### Response

application/json

items[].last_upd_date

date|null

วันที่แก้ไขข้อมูลล่าสุด (อาจเป็น null ได้)

items[].lic_no

string

เลขที่ใบอนุญาต (กรณีจดทะเบียนจะไม่มีหมายเลข → ค่าว่าง "")

items[].lic_code

string

รหัสประเภทใบอนุญาต

items[].lic_name_th

string

ชื่อประเภทใบอนุญาต (ภาษาไทย)

items[].lic_name_en

string

ชื่อประเภทใบอนุญาต (ภาษาอังกฤษ)

items[].acc_type

string

ประเภทตามกฎหมาย/ระบบ (เช่น พรบ.หลักทรัพย์)

items[].apply_type

string

สถานะการได้มา (เช่น ได้รับใบอนุญาต / จดทะเบียน)

items[].effective_date

date

วันที่ใบอนุญาตมีผล (YYYY-MM-DD)

items[].expire_date

date|string

วันที่ใบอนุญาตสิ้นสุด (YYYY-MM-DD) — ค่าว่าง "" หรือ " " หมายถึงไม่มีข้อมูล



### 8. การประกอบธุรกิจในปัจจุบันของนิติบุคคลที่ได้รับใบอนุญาตจากสำนักงาน

ข้อมูลสถานะการประกอบธุรกิจของนิติบุคคลที่ได้รับใบอนุญาตจากสำนักงานก.ล.ต. โดยประกอบด้วยรหัสประเภทใบอนุญาต (lic_code), รหัสประเภทการประกอบธุรกิจ (lic_action_code), ช่วงเวลาเริ่มประกอบธุรกิจ (action_start_date), สถานะการประกอบธุรกิจ (action_status) และหมายเหตุในกรณีหยุดประกอบธุรกิจ (action_remark)

### Endpoint

```
GET/v1/license-check/licensee/company/{unique_id}/business_act
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสนิติบุคคล

### Response

application/json

items.last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items.lic_code

string

รหัสประเภทใบอนุญาต/การจดทะเบียน

items.lic_name_th

string

ชื่อประเภทใบอนุญาต/การจดทะเบียน (ภาษาไทย)

items.lic_name_en

string

ชื่อประเภทใบอนุญาต/การจดทะเบียน (ภาษาอังกฤษ)

items.lic_action_code

string

รหัสประเภทการประกอบธุรกิจ

items.lic_action_name_th

string

ชื่อประเภทการประกอบธุรกิจ (ภาษาไทย)

items.lic_action_name_en

string

ชื่อประเภทการประกอบธุรกิจ (ภาษาอังกฤษ)

items.acc_type

string

ประเภทตามกฎหมาย/ระบบ (เช่น พรบ.หลักทรัพย์)

items.action_start_date

date|string

วันที่เริ่มประกอบธุรกิจ (YYYY-MM-DD)

items.action_status

string

สถานะการประกอบธุรกิจ (NORMAL / HOLD)

items.action_remark

string|null

หมายเหตุกรณีหยุดประกอบธุรกิจ (รองรับ null)



### 9. ประเภทความผิดและการกระทำของบุคคลหรือนิติบุคคลที่ได้รับความเห็นชอบหรือใบอนุญาตของสำนักงาน

ข้อมูลประเภทความผิดและการดำเนินการที่เกี่ยวข้องกับบุคคลหรือนิติบุคคลที่ได้รับความเห็นชอบหรือใบอนุญาตจากสำนักงาน ก.ล.ต. โดยมีประเภทการดำเนินการ (enforcement_type) เช่น การกล่าวโทษ การเปรียบเทียบ การปรับทางปกครอง การดำเนินการทางบริหาร และการดำเนินการทางแพ่ง รวมถึงรหัสอ้างอิงของคดี (case_id)

### Endpoint

```
GET/v1/license-check/licensee/{unique_id}/enforcement
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสบุคคล/นิติบุคคล

### Response

application/json

items[].last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items[].enforcement_type

string

ประเภทการดำเนินการ (กล่าวโทษ / เปรียบเทียบ / ปรับทางปกครอง / การดำเนินการทางบริหาร / การดำเนินการทางแพ่ง)

items[].case_id

string

รหัสอ้างอิง case ความผิด



### 10. การดำเนินการกับความผิดของบุคคลหรือนิติบุคคลที่ได้รับความเห็นชอบหรือใบอนุญาตของสำนักงาน

ข้อมูลรายละเอียดการดำเนินการกับความผิดที่เกี่ยวข้องกับบุคคลหรือนิติบุคคลที่ได้รับความเห็นชอบหรือใบอนุญาตจากสำนักงาน ก.ล.ต. โดยประกอบด้วยข้อมูลเกี่ยวกับมาตรา/กฎหมายที่เกี่ยวข้อง (enforcement_relevant_section_law), การกระทำของบุคคลหรือนิติบุคคลโดยสังเขป (enforcement_summarized_facts), วันที่ดำเนินการตามประเภทการดำเนินการ (enforcement_date), รายละเอียดการดำเนินการ (enforcement_details) และหมายเหตุเพิ่มเติม (enforcement_remark) ซึ่งสะท้อนลักษณะของมาตรการที่ใช้ เช่น การกล่าวโทษ การเปรียบเทียบ การลงโทษทางปกครอง การดำเนินการทางบริหาร หรือการดำเนินการทางแพ่ง

### Endpoint

```
GET/v1/license-check/licensee/{unique_id}/enforcement/{case_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

unique_idrequired

string

รหัสบุคคล/นิติบุคคล

case_idrequired

string

รหัสอ้างอิง case ความผิด

### Response

application/json

items.last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items.enforcement_relevant_section_law

string

มาตรา / กฎหมายที่เกี่ยวข้อง

items.enforcement_summarized_facts

string

การกระทำโดยสังเขป

items.enforcement_date

date

วันที่ดำเนินการ (YYYY-MM-DD) แสดงวันที่ตามประเภทการดำเนินการ:

- 1) วันที่กล่าวโทษ
- 2) วันที่เปรียบเทียบ
- 3) วันที่ดำเนินการทางบริหาร (แสดงวันที่ในหนังสือลงโทษ)
- 4) วันที่ลงโทษทางปกครอง
- 5) วันที่ทางแพ่ง

items.enforcement_details

string

รายละเอียดการดำเนินการ (แสดงตามประเภท):

- 1) รายละเอียดการกล่าวโทษ
- 2) เปรียบเทียบ → "มีคำสั่งเปรียบเทียบที่ [คำสั่งเปรียบเทียบที่] โดยปรับเป็นเงิน [ค่าปรับ] บาท"
- 3) ปรับทางปกครอง → "มี [เลขที่คำสั่ง] โดยปรับเป็นเงิน [ค่าปรับ] บาท"
- 4) การดำเนินการทางบริหาร เช่น สั่งพัก เพิกถอน ภาคทัณฑ์ ฯลฯ
- 5) การดำเนินการทางแพ่ง เช่น โทษอื่น ๆ

items.enforcement_remark

string

หมายเหตุ (แสดงรายละเอียดตามประเภท):

- 1) หมายเหตุการกล่าวโทษ
- 2) เปรียบเทียบ → หากไม่ชำระ/ชำระไม่ครบ ให้แสดงข้อความ: "ไม่ชำระค่าปรับ/ชำระไม่ครบถ้วน สำนักงานได้กล่าวโทษกรณีนี้ต่อพนักงานสอบแล้ว"
- 3) หมายเหตุการปรับทางปกครอง
- 4) การดำเนินการทางบริหาร → "คำสั่งมีผล ตั้งแต่วันที่ DD/MM/YYYY ถึงวันที่ DD/MM/YYYY"
- 5) หมายเหตุการดำเนินการทางแพ่ง



### 11. รายละเอียดข้อมูลเตือนผู้ลงทุน

ข้อมูลเตือนผู้ลงทุน (Investor Alert) เกี่ยวกับบริษัท นิติบุคคล บุคคลหรือเว็บไซต์ที่มิใช่ผู้ประกอบธุรกิจภายใต้การกำกับดูแลของสำนักงาน ก.ล.ต. เพื่อรักษาประโยชน์ของประชาชนหรือเพื่อคุ้มครองผู้ลงทุน สำนักงาน ก.ล.ต. ได้รวบรวมข้อมูลรายชื่อบุคคลหรือผู้ให้บริการที่มีประชาชนสอบถามเกี่ยวกับการชักชวนให้ลงทุนหรือใช้บริการและทำให้เข้าใจผิดว่าอยู่ภายใต้กำกับดูแลของสำนักงาน ก.ล.ต. ซึ่งสำนักงาน ก.ล.ต. สอบทานแล้วพบว่ามิใช่ผู้ได้รับอนุญาตหรือประกอบธุรกิจภายใต้การกำกับดูแลของสำนักงาน ก.ล.ต. ทั้งนี้ข้อมูลดังกล่าวอาจมิได้ครอบคลุมครบทุกรายและจะมีการปรับปรุงเป็นระยะ ๆ (หรือสามารถเข้าถึงข้อมูลได้จาก: https://market.sec.or.th/public/idisc/th/InvestorAlert)

### Endpoint

```
GET/v1/license-check/licensee/investoralert/alertdetail
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Response

application/json

items.last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items.case_id

string

รหัสอ้างอิง case ความผิด

items.disclosure_date

date

วันที่เปิดเผยข้อมูล (YYYY-MM-DD)

items.name_th

string

ชื่อบริษัทหรือนิติบุคคลและเว็บไซต์ที่ไม่ได้รับอนุญาต (ภาษาไทย)

items.name_en

string

ชื่อบริษัทหรือนิติบุคคล และ เว็บไซต์ที่ไม่ได้รับอนุญาต (ภาษาอังกฤษ)

items.address_th

string

ที่อยู่ (ภาษาไทย)

items.address_en

string

ที่อยู่ (ภาษาอังกฤษ)

items.persuade_desc

string

ลักษณะการชักชวน

items.website

string

website

items.facebook

string

facebook

items.line

string

line

items.remark

string

หมายเหตุ



### 12. ลักษณะการกระทำ

ข้อมูลลักษณะการกระทำที่เกี่ยวข้องกับข้อมูลเตือนผู้ลงทุน (Investor Alert) จากใน API ข้อ 11 รายละเอียดข้อมูลเตือนผู้ลงทุน ซึ่งสามารถเชื่อมโยงกันด้วยรหัสอ้างอิงคดีความผิด (case_id) โดยประกอบด้วยข้อมูลรายละเอียดลักษณะการกระทำทั้งภาษาไทยและภาษาอังกฤษ (license_th, license_en) ข้อมูลนี้ใช้เพื่อประกอบการทำความเข้าใจพฤติการณ์ชักชวนที่อาจทำให้ผู้ลงทุนเข้าใจผิดและสนับสนุนการเฝ้าระวังความเสี่ยงด้านการคุ้มครองผู้ลงทุน

### Endpoint

```
GET/v1/license-check/licensee/investoralert/{case_id}/alertaction
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

case_idrequired

string

รหัสอ้างอิง case ความผิด

### Response

application/json

items.last_upd_date

date

วันที่แก้ไขข้อมูลล่าสุด

items.case_id

string

รหัสอ้างอิง case ความผิด

items.seq_no

string

ลำดับที่

items.license_th

string

ลักษณะการกระทำ (ภาษาไทย)

items.license_en

string

ลักษณะการกระทำ (ภาษาอังกฤษ)



### 13. รายชื่อผู้สอบบัญชีที่ได้รับความเห็นชอบทั้งหมด

ข้อมูลรายชื่อผู้สอบบัญชีที่ได้รับความเห็นชอบจากสำนักงาน ก.ล.ต. ซึ่งประกอบด้วยข้อมูลชื่อบริษัทสอบบัญชี (company_name_th), ชื่อ–นามสกุลผู้สอบบัญชีทั้งภาษาไทยและภาษาอังกฤษ (auditor_name_th, auditor_name_en), เลขที่ทะเบียนผู้สอบบัญชี (auditor_license_number), วันที่ได้รับความเห็นชอบ (efft_date) และวันที่หมดอายุความเห็นชอบ (exp_date) (หรือสามารถเข้าถึงข้อมูลได้จาก: https://market.sec.or.th/public/orap/AUDITOR01.aspx?lang=th)

### Endpoint

```
GET/v1/license-check/licensee/auditors
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Response

application/json

items.company_name_th

string

ชื่อบริษัทสอบบัญชี (ภาษาไทย)

items.auditor_name_th

string

ชื่อนามสกุลผู้สอบบัญชี (ภาษาไทย) *อาจมีเครื่องหมาย (*), (**), (***) ต่อท้าย

items.auditor_name_en

string

ชื่อนามสกุลผู้สอบบัญชี (ภาษาอังกฤษ)

items.auditor_license_number

number (integer)

เลขที่ทะเบียน

items.efft_date

date

วันที่ได้รับความเห็นชอบ (YYYY-MM-DD)

items.exp_date

date

วันที่หมดอายุความเห็นชอบ (YYYY-MM-DD)

items.last_updated

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)



### 14. รายชื่อบริษัทสอบบัญชี

ข้อมูลรายชื่อบริษัทสอบบัญชี พร้อมทั้งเลขนิติบุคคลของแต่ละบริษัท

### Endpoint

```
GET/v1/license-check/licensee/auditingFirm
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Response

application/json

items.company_name

string

ชื่อบริษัทสอบบัญชี (ภาษาไทย)

items.company_name_en

string

ชื่อบริษัทสอบบัญชี (ภาษาอังกฤษ)

items.address

string

ที่อยู่บริษัท

items.post_code

string

เลขไปรษณีย์บริษัท

items.telephone

string

เบอร์โทรศัพท์บริษัท

items.fax

string

แฟกซ์

items.email

string

อีเมลล์บริษัท

items.link

string

เว็ปไซต์บริษัท

items.last_updated

datetime|null

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)



### 15. รายชื่อผู้สอบบัญชีที่ได้รับความเห็นชอบ (ค้นหาตามชื่อผู้สอบบัญชี)

ข้อมูลรายชื่อผู้สอบบัญชีที่ได้รับความเห็นชอบจากสำนักงาน ก.ล.ต. โดยสามารถค้นหาตามชื่อผู้สอบบัญชี ซึ่งประกอบด้วยข้อมูลชื่อบริษัทสอบบัญชี (company_name_th), ชื่อ–นามสกุลผู้สอบบัญชีทั้งภาษาไทยและภาษาอังกฤษ (auditor_name_th, auditor_name_en), เลขที่ทะเบียนผู้สอบบัญชี (auditor_license_number), วันที่ได้รับความเห็นชอบ (efft_date) และวันที่หมดอายุความเห็นชอบ (exp_date) (หรือสามารถเข้าถึงข้อมูลได้จาก: https://market.sec.or.th/public/orap/AUDITOR01.aspx?lang=th)

### Endpoint

```
GET/v1/license-check/licensee/auditors/search/name/{person_name}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

person_namerequired

string

### Response

application/json

items.company_name_th

string

ชื่อบริษัทสอบบัญชี (ภาษาไทย)

items.address

string

ที่อยู่บริษัท

items.post_code

string

เลขไปรษณีย์บริษัท

items.telephone

string

เบอร์โทรศัพท์บริษัท

items.fax

string

แฟกซ์

items.email

string

อีเมลล์บริษัท

items.link

string

เว็ปไซต์บริษัท

items.auditor_name

string

ชื่อนามสกุลผู้สอบบัญชี (รองรับไทย/อังกฤษ และอาจมี (*), (**), (***) ต่อท้ายตามหมายเหตุ)

items.auditor_license_number

number (integer)

เลขที่ทะเบียน

items.efft_date

date

วันที่ได้รับความเห็นชอบ (YYYY-MM-DD)

items.exp_date

date

วันที่หมดอายุความเห็นชอบ (YYYY-MM-DD)

items.last_updated

datetime

วันที่แก้ไขข้อมูลล่าสุด (ISO8601 datetime)