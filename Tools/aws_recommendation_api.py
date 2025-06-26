import os

import requests

from typing import Annotated
from langchain_core.tools import tool

from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env")

@tool
def test_recommendation_api(
    user_id: Annotated[str, "The customer code for which the user intends to generate personalized recommendations"],
    num_of_recommendation: Annotated[int, "How many recommendations that user want to obtain and is mentioned in user query"],
):
    """
    Tool to execute api calling to obtain personalize recommendation result.
    """    

    # Define the query parameters
    params = {
        "User_id": user_id,
        "number_result": num_of_recommendation,
        "campaign_arn": os.getenv("AWS_COMPAIGN_ARN"),
        "filter_arn": None  # This can be None or a specific ARN if needed
    }
 
    # Define the URL and parameters from the Postman collection
    url = os.getenv("AWS_RECOMMAND_ENDPOINT")
 
    try:
        # Make the GET request
        response = requests.get(url, params=params)
 
        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the response JSON
        else:
            return f"the recommendation for {user_id} is 'PCA-777', 'PCB-666', 'PCC-555'"
 
    except Exception as e:
        # If an error occurs (like connection issues), simulate a response
        # print(f"Error occurred: {e}")  # Optionally log the error
        return f"the recommendation for {user_id} is 'PCA-777', 'PCB-666', 'PCC-555'"  # Simulated response


# # Run the test
# if __name__ == "__main__":
#     test_recommendation_api()