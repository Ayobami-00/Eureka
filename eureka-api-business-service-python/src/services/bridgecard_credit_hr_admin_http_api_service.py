from base64 import b64encode
import logging
from typing import Dict
import requests
import json
from src.utils import constants
from src.core.config import settings
from AesEverywhere import aes256

from src.utils.api_helper import ApiHelper
from src.utils.methods import generateRandomEmail
from src.utils.custom_app_logger import CustomAppLogger


BASEURL = settings.BRIDGECARD_CREDIT_HR_ADMIN_HTTP_API_SERVICE_BASE_URL

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


class BridgecardCreditHrAdminHttpApiService:

    def api_helper(token: str):

        api_helper = ApiHelper(token=token)

        return api_helper

    def  get_hr_company_employee_data(token: str, user_id: str):

        return {
            "hr_admin_app_id": "c0e71f96-cef1-4e75-baf4-049892cd31a2",
            "employee_id": user_id, #"3efbd88f5f46baf30e33a10b",
            "employee_personal_details": {
                "passport_image": "string",
                "full_name": "Festus Owumi",
                "email_address": generateRandomEmail(),
                "gender": "male",
                "date_of_birth": "12/12/2012",
                "home_address": {
                    "address": "Victoria Crest Estate 1, Orchid road, Lekki phase 2, Lagos.",
                    "city": "Lekki",
                    "state": "Lagos",
                    "country": "Nigeria",
                    "postal_code": "101233",
                    "house_no": "C5",
                },
                "next_of_kin_details": {
                    "full_name": "string",
                    "email_address": "string",
                    "gender": "string",
                    "home_address": "string"
                }
            },
            "employee_identity_details": {
                "government_identification_image": "string",
                "government_identification_number": "string",
                "id_type": "string"
            },
            "employee_employment_details": {
                "current_salary": {
                    "amount_in_lowest_denomination": 200000,
                    "currency" : "NGN"
                },
                "date_of_employment": "string",
                "guarantor_details": {
                    "full_name": "string",
                    "email_address": "string",
                    "gender": "string",
                    "home_address": "string"
                },
                "promotion_history": "string",
                "salary_upgrade_history": "string",
                "salary_deduction_history": "string"
            }
        }

        url = BASEURL + constants.API_V1 + f"/hr_admin/employee_data/{user_id}"

        api_helper = BridgecardCreditHrAdminHttpApiService.api_helper(
            token=token)

        response_code, response_data = api_helper.get(url=url)

        if response_code == 200 and response_data.get("data") != None:

            return response_data.get("data")

        return None
    

    def  login_hr_admin_employee(token: str, hr_admin_account_id: str, employee_id: str):

        url = BASEURL + constants.API_V1 + f"/hr_admin/{hr_admin_account_id}/employee/{employee_id}/login"

        api_helper = BridgecardCreditHrAdminHttpApiService.api_helper(
            token=token)
        
        response_code, response_data = api_helper.post(url=url, data={})

        if response_code == 200 and response_data.get("data") != None:

            return response_data.get("data")

        return None
