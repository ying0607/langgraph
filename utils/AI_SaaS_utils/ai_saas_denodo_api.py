import os
import requests
import pandas as pd

from requests.auth import HTTPBasicAuth

from dotenv import load_dotenv
load_dotenv("LangGraph/.env")

class APIClient:
    def __init__(self):
        self.api_key = os.getenv(
            "AI_SAAS_API_KEY", "http://127.0.0.1:8000"
        )
        self.base_url = os.getenv("AI_SAAS_HOST", "http://127.0.0.1:8000")
        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
        }

    def query_database(self, db_name, query_str, timeout=150):
        data = {
            "server_uri": os.environ["DENODOSERVER_NAME"],
            "db_name": db_name,
            "query_str": query_str,
        }

        response = requests.post(
            os.environ["S2S_HOST"],
            json=data,
            auth=HTTPBasicAuth(
                os.environ["DENODOSERVER_UID"],
                os.environ["DENODOSERVER_PWD"],
            ),
            timeout=timeout
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise requests.exceptions.HTTPError(
                f"Error {response.status_code}: {response.text}"
            )

    def _raise_for_status(self, response):
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                f"Error {response.status_code}: {response.text}"
            )
        

        
# # ai_saas 測試
# if __name__ == "__main__":
#     load_dotenv("LangGraph/.env")
#     print(os.getenv("DENODOSERVER_NAME"))
#     client = APIClient()

#     # aggregate_query = "SELECT * FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full WHERE region = 'Taiwan' LIMIT 1"
#     # aggregate_query = """
#     # SELECT COLUMN_NAME 
#     # FROM dx_management.rv_eai_acldw_shipmentbacklog_bomexpand_fa_full
#     # WHERE region = 'Taiwan'
#     # """

#     aggregate_query =  """
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
# WHERE "Tran_Type" = 'Shipment' AND part LIKE '%AIW%'
# """

# AND orderno = 'ATWO001766'

# GROUP BY
#     year_id, month_id, erp_id, customername, part, part_series, pd
# HAVING
#     SUM(qty) > 50
# ORDER BY
#     year_id, month_id, erp_id, customername, part, part_series, pd
#     """
    

    # print(client.query_database(os.getenv("DENODOSERVER_DATABASE"), aggregate_query))

    # # save the query result to a variable
    # result = client.query_database(os.getenv("DENODOSERVER_DATABASE"), aggregate_query)
    # # 轉換為 DataFrame
    # df = pd.DataFrame(result['data'])
    # df.to_csv("./customer_order_test1.csv", index=False)

