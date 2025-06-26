from langchain_core.tools import tool
from typing import Annotated, Any, Dict

# prepare_dict_answer
@tool
def prepare_dict_answer(
    customer_lead_answer: Annotated[str, "it is the response with json format in adaptive card from Customer_Lead_Agent."] = "",
    customer_profile_answer: Annotated[str, "it is the response from Customer_Profile_Agent."] = "",
    customer_order_answer: Annotated[str, "it is the response from Customer_Order_Agent."] = "",
    personalize_recommendation_answer: Annotated[str, "it is the response from Personalize_Recommendation_Agent."] = ""
) :
    """
    Tool to sort the response for Teams
    """ 

    answers = {
        "customer_lead_answer": f"{customer_lead_answer}",
        "customer_profile_answer": f"{customer_profile_answer}",
        "customer_order_answer": f"{customer_order_answer}",
        "personalize_recommendation_answer": f"{personalize_recommendation_answer}"
    }

    final_dict = {key: value for key, value in answers.items() if value != ""}

    return final_dict
