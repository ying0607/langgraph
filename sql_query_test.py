import os
import pandas as pd
from utils.AI_SaaS_utils.ai_saas_denodo_api import APIClient

from dotenv import load_dotenv
load_dotenv("LangGraph\.env")

ai_saas_client = APIClient()

denodoserver_name = os.getenv("DENODOSERVER_DATABASE")

sql = ("""
SELECT DISTINCT customername, orderno
FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full
WHERE region = 'Taiwan'  
ORDER BY RAND() 
LIMIT 10
""")

# sql = ("""
# SELECT
#     ymd,
#     customer as erp_id,
#     customername,
#     orderno as po_no,
#     part,
#     us_amt,
#     qty
# FROM (
#     SELECT
#         ymd,
#         "Tran_Type",
#         customer,
#         customername,
#         orderno,
#         part,
#         us_amt,
#         qty
#     FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full
#     WHERE region = 'Taiwan'
# )
# WHERE "Tran_Type" = 'Shipment' AND customername LIKE '%羅技%' AND orderno = 'OITW049372'
# """)

# SELECT
#     salesname,
#     ymd,
#     customer as erp_id,
#     customername,
#     orderno as po_no,
#     part,
#     SUM(us_amt),
#     SUM(qty)
# FROM (
#     SELECT
#         salesname,
#         ymd,
#         "Tran_Type", 
#         customer,
#         customername,
#         orderno,
#         part,
#         us_amt,
#         qty
#     FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full
#     WHERE region = 'Taiwan'
# )
# WHERE "Tran_Type" = 'Shipment' AND customer = 'T12795763' AND orderno = 'ATWO001766'
# GROUP BY
#     ymd,
#     customer,
#     customername,
#     orderno,
#     part


# SELECT
#     ymd,
#     customer as erp_id,
#     customername,
#     orderno as po_no,
#     part,
#     us_amt,
#     qty
# FROM (
#     SELECT
#         "Tran_Type",
#         MIN(salesname) AS salesname,      
#         ymd,
#         customer AS erp_id,
#         customername,
#         orderno AS po_no,
#         part,
#         SUM(us_amt) AS us_amt,         
#         SUM(qty) AS qty                
#     FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full
#     GROUP BY 
#         ymd,
#         customer,
#         customername,
#         orderno,
#         part
# )
# WHERE 
  

data = ai_saas_client.query_database(denodoserver_name, sql)
# print(data)
df = pd.DataFrame(data['data'])
# df.to_csv("LangGraph\Data\check_with_groupby.csv", index=False, encoding='utf-8-sig')

print(df)

