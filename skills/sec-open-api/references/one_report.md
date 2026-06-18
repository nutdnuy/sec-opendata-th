### 01.ข้อมูลทั่วไปของบริษัท



### Endpoint

```
GET/v1/one-report/sbo/{report_year}/info/{language}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

languagerequired

string

ภาษา (T / E)

### Response

application/json

### 02.ข้อมูลการวิจัยและพัฒนา (R&D)



### Endpoint

```
GET/v1/one-report/sbo/{report_year}/rd/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 03.ข้อมูลโครงสร้างรายได้แบ่งตามกลุ่มธุรกิจ



### Endpoint

```
GET/v1/one-report/sbo/{report_year}/product_income/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท



### 04.ข้อมูลโครงสร้างรายได้แบ่งตามรายได้จากต่างประเทศ



### Endpoint

```
GET/v1/one-report/sbo/{report_year}/export_income/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 05.ข้อมูลรายละเอียดการบริหารจัดการความเสี่ยง



### Endpoint

```
GET/v1/one-report/sbo/{report_year}/risk/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 06.ข้อมูลนโยบายและเป้าหมายการจัดการด้านความยั่งยืน



### Endpoint

```
GET/v1/one-report/sustainability/{report_year}/detail/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 07.ข้อมูลด้านสิ่งแวดล้อม



### Endpoint

```
GET/v1/one-report/sustainability/{report_year}/environment_issue/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 08.ข้อมูลนโยบายสิทธิมนุษยชน



### Endpoint

```
GET/v1/one-report/sustainability/{report_year}/humanrights_issue/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 09.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - พนักงานและค่าตอบแทน



### Endpoint

```
GET/v1/one-report/scp/{report_year}/employee_info/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 10.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - การฝึกอบรมและความปลอดภัย



### Endpoint

```
GET/v1/one-report/scp/{report_year}/employee_development/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 11.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - ข้อพิพาทด้านแรงงาน



### Endpoint

```
GET/v1/one-report/scp/{report_year}/labor_dispute/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 12.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - CSR



### Endpoint

```
GET/v1/one-report/scp/{report_year}/csr_activity/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัทหลักทรัพย์

### Response

application/json



### 13.ข้อมูลนโยบายการกำกับดูแลกิจการ



### Endpoint

```
GET/v1/one-report/cgp/{report_year}/governance/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 14.ข้อมูลนโยบายและแนวปฏิบัติที่เกี่ยวกับคณะกรรมการ



### Endpoint

```
GET/v1/one-report/cgp/{report_year}/director/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 15.ข้อมูลจรรยาบรรณธุรกิจ



### Endpoint

```
GET/v1/one-report/cgp/{report_year}/code_of_conduct/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 16.งบการเงินและอัตราส่วนทางการเงิน



### Endpoint

```
GET/v1/one-report/fs/{report_year}/financial_statement/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 17.ข้อมูลองค์ประกอบของคณะกรรมการบริษัท



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/board/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 18.ข้อมูลเกี่ยวกับพนักงาน



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/employee/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 19.ข้อมูลบริษัทผู้สอบบัญชี



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/auditor_company/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 20.ข้อมูลการเข้าร่วมประชุมคณะกรรมการบริษัท



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/director_performance/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 21.ข้อมูลคณะกรรมการ (Board of directors)



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/bods/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 22.ข้อมูลผู้บริหาร



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/executives/{unique_id}
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json



### 23.ข้อมูลคณะกรรมการอื่น ๆ ของบริษัท



### Endpoint

```
GET/v1/one-report/cgs/{report_year}/committees/{unique_id}/others
```

### Headers

Ocp-Apim-Subscription-Keyrequired

string

คีย์ API เฉพาะของคุณสำหรับการยืนยันตัวตน

### Parameters

report_yearrequired

string

ปี

unique_idrequired

string

รหัสบริษัท

### Response

application/json

