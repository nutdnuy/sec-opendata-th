### 1. รายชื่อผู้ประกอบธุรกิจสินทรัพย์ดิจิทัล

ข้อมูลรายชื่อผู้ประกอบธุรกิจสินทรัพย์ดิจิทัล (Digital Asset Business Operator) ที่อยู่ภายใต้การกำกับของ ก.ล.ต.

### Endpoint

```
POST/v1/digital-asset/profile/intermediary
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Request Body

IntermediaryNamestring

### Response

application/json

items[].unique_id

string

รหัสผู้ประกอบธุรกิจ

items[].name_th

string

ชื่อผู้ประกอบธุรกิจ (ไทย)

items[].name_en

string

ชื่อผู้ประกอบธุรกิจ (อังกฤษ)

items[].lic_code

string

รหัสประเภทใบอนุญาต

items[].lic_action_code

string

รหัสประเภทการประกอบธุรกิจ

items[].lic_efft_date

date

วันที่ใบอนุญาตมีผลบังคับใช้

items[].lic_exp_date

date

วันที่สิ้นสุดใบอนุญาต