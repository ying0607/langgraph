## Query & Result

- User Query：想看T54274625在IDR24C0243訂單的每個料號系列各買了多少錢，及購買總金額
- Filter：erp_id、po_no、part_series、購買總金額
- Processing Check：✅

```markdown
# Denodo 透過 SQL Query 抓取的資料
ymd,erp_id,customername,po_no,part,part_series,pd,us_amt,qty
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-FS,AGS,SVCB,7.66,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-SS,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-PU-PC,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-NPF-PC,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-LS,AGS,SVCB,42.9,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-MS,AGS,SVCB,0.21,0.0
```
```markdown
# DataFrame 分析完產出的結果
Part Series,US Amount,Total Purchase Amount
AGS,50.769999999999996,50.77
```

---

- User Query：想看T52347361在ATWO006452訂單的每個pd各買了多少錢，及購買總金額
- Filter：erp_id、po_no、part_series、購買總金額
- Processing Check：❌ Dataframe 使用錯誤的 python code `df.append` 新增額外產生的欄位(total purchase amount)
    - 🔧 在 `customer_order_prompt` 419-434 新增 Example 2
    - ✅ 測試同樣需要 concat 的問題，問題已解決

```markdown
# Denodo 透過 SQL Query 抓取的資料
ymd,erp_id,customername,po_no,part,part_series,pd,us_amt,qty
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,22.89,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96MPI5A-3.0-18M17,96MPI5A,Socket CPU,189.0,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96PSA-A230W24P4-3,96PSA,Industrial Power Supply,39.43,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,PPC-315W-TGL-BTO,PPC,Panel PC,0.0,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,PPC-315W-PB50A,PPC,Panel PC,3549.17,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,1702002600,1702002600,UNO,7.59,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20704WX1VS0013,20704WX1VS0013,Panel PC,203.41,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,68.68,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AQD-SD4U8GN32-SE,AQD,System Core,65.48,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-C8MV2-128GDEDC,SQF,Industrial Storage,77.84,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96PSA-A120W24T2-4,96PSA,Industrial Power Supply,57.7,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,ARK-3534B-BTO,ARK,EBC,0.0,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,ARK-3534B-00A1,ARK,EBC,706.46,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQR-SD5N16G4K8SNBB,SQR,Industrial Storage,61.06,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-S25V1-256GDSDC,SQF,Industrial Storage,36.85,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,1702002600,1702002600,UNO,2.52,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20706WLV1S0017,20706WLV1S0017,SW Distribution,71.34,1.0
```
```markdown
# DataFrame 分析完產出的結果
PD,US Amount
CTOS,91.57000000000001
EBC,706.46
Industrial Power Supply,97.13
Industrial Storage,175.75
Panel PC,3752.58
SW Distribution,71.34
Socket CPU,189.0
System Core,65.48
UNO,10.11
Total,5159.42
```

---

- User Query：想看T54274625在IDR24C0243訂單中，購買金額為0的 part
- Filter：erp_id、po_no、part、購買金額
- Processing Check：✅

```markdown
# Denodo 透過 SQL Query 抓取的資料
ymd,erp_id,customername,po_no,part,part_series,pd,us_amt,qty
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-FS,AGS,SVCB,7.66,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-SS,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-PU-PC,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-NPF-PC,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-LS,AGS,SVCB,42.9,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-MS,AGS,SVCB,0.21,0.0
```
```markdown
# DataFrame 分析完產出的結果
Date,ERP ID,Customer Name,PO No,Part,Part Series,PD,US Amount,Qty
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-OW-SS,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-PU-PC,AGS,SVCB,0.0,0.0
2025-01-02,T54274625,LightMed Dental Technology corp. : 鐳鼎科技股份有限公司,IDR24C0243,AGS-NPF-PC,AGS,SVCB,0.0,0.0
```

---
- User Query：想看T52347361在ATWO006452訂單的購買單價大於20的pd
- Filter：erp_id、po_no、pd、購買單價
- Processing Check：✅

```markdown
# Denodo 透過 SQL Query 抓取的資料
ymd,erp_id,customername,po_no,part,part_series,pd,us_amt,qty
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,22.89,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96MPI5A-3.0-18M17,96MPI5A,Socket CPU,189.0,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96PSA-A230W24P4-3,96PSA,Industrial Power Supply,39.43,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AQD-SD4U8GN32-SE,AQD,System Core,65.48,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-C8MV2-128GDEDC,SQF,Industrial Storage,77.84,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96PSA-A120W24T2-4,96PSA,Industrial Power Supply,57.7,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,ARK-3534B-BTO,ARK,EBC,0.0,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,ARK-3534B-00A1,ARK,EBC,706.46,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQR-SD5N16G4K8SNBB,SQR,Industrial Storage,61.06,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-S25V1-256GDSDC,SQF,Industrial Storage,36.85,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,1702002600,1702002600,UNO,2.52,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20706WLV1S0017,20706WLV1S0017,SW Distribution,71.34,1.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,PPC-315W-TGL-BTO,PPC,Panel PC,0.0,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,PPC-315W-PB50A,PPC,Panel PC,3549.17,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,1702002600,1702002600,UNO,7.59,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20704WX1VS0013,20704WX1VS0013,Panel PC,203.41,3.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,68.68,3.0
```

```markdown
# DataFrame 分析完產出的結果
Date,ERP ID,Customer Name,PO No,Part,Part Series,PD,US Amount,Qty,Unit Price
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,22.89,1.0,22.89
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96MPI5A-3.0-18M17,96MPI5A,Socket CPU,189.0,1.0,189.0
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,96PSA-A230W24P4-3,96PSA,Industrial Power Supply,39.43,1.0,39.43
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AQD-SD4U8GN32-SE,AQD,System Core,65.48,3.0,21.826666666666668
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-C8MV2-128GDEDC,SQF,Industrial Storage,77.84,3.0,25.94666666666667
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,ARK-3534B-00A1,ARK,EBC,706.46,1.0,706.46
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQR-SD5N16G4K8SNBB,SQR,Industrial Storage,61.06,1.0,61.06
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,SQF-S25V1-256GDSDC,SQF,Industrial Storage,36.85,1.0,36.85
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20706WLV1S0017,20706WLV1S0017,SW Distribution,71.34,1.0,71.34
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,PPC-315W-PB50A,PPC,Panel PC,3549.17,3.0,1183.0566666666666
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,20704WX1VS0013,20704WX1VS0013,Panel PC,203.41,3.0,67.80333333333333
2025-03-10,T52347361,喬山健康科技股份有限公司,ATWO006452,AGS-CTOS-SYS-A,AGS,CTOS,68.68,3.0,22.893333333333334
```


## 附錄：


## 在思考測試問題時可以使用的 erp_id 跟 orderno
``` plaintext
    customer     orderno     Features                Folder Loc.                ===========備註==============
0  T54274625   IDR24C0243   不同的 part               Data/testing1 + testing3   us_amt、qty 會存在 0.0 的資料
1  T52347361   ATWO006452   不同的 pd                 Data/testing2 + testing4
2  T58506816   ATWO001211   只有一筆資料
3  T20939460   ATWO001090   不同的 part 
4  T53757193   TWO148548    同時存在不同的 pd 與 part 
5  T23161576   TWO146001
6  T23161576   TWO146001
7  T23161576   TWO146001
8  T23161576   TWO146001
9  T23161576   TWO146001
```
```plaintext
---
- User Query：想看T54274625在IDR24C0243訂單的每個料號系列各買了多少錢，及購買總金額
- Filter：erp_id、po_no、part_series、購買總金額
- Processing Check：✅ / Processing Check：❌

-```markdown
# Denodo 透過 SQL Query 抓取的資料
-```

-```markdown
# DataFrame 分析完產出的結果
-```
```
