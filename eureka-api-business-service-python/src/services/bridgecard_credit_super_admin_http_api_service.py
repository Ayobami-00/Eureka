from base64 import b64encode
import logging
from typing import Dict
import requests
import json
from src.schema.base import Currency
from src.utils import constants
from src.core.config import settings
from AesEverywhere import aes256

from src.utils.api_helper import ApiHelper
from src.utils.methods import generateRandomEmail
from src.utils.custom_app_logger import CustomAppLogger


BASEURL = settings.BRIDGECARD_CREDIT_SUPER_ADMIN_HTTP_API_SERVICE_BASE_URL

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


class BridgecardCreditSuperAdminHttpApiService:

    def api_helper(token: str):

        api_helper = ApiHelper(token=token)

        return api_helper

    def update_employee_loan_history(token: str, loan_id: str, data: Dict):

        url = BASEURL + constants.API_V1 + f"/loan_history/{loan_id}"

        api_helper = BridgecardCreditSuperAdminHttpApiService.api_helper(
            token=token)

        response_code, response_data = api_helper.patch(url=url, data=data)

        if response_code == 200 and response_data.get("data") != None:

            return response_data.get("data")

        return None

    def get_settlement_account(token: str, account_currency: Currency, account_type: str):

        url = BASEURL + constants.API_V1 + \
            f"/misc/settlement-account?account_currency={account_currency.value}&account_type={account_type}"

        api_helper = BridgecardCreditSuperAdminHttpApiService.api_helper(
            token=token)

        response_code, response_data = api_helper.get(url=url)

        if response_code == 200 and response_data.get("data") != None:

            return response_data.get("data")["data"]

        return None

    def credit_employee(token: str, employee_account_id: str, hr_admin_account_id: str, amount_to_be_sent: int):

        url = BASEURL + constants.API_V1 + \
            f"/superadmin/employee/credit"

        api_helper = BridgecardCreditSuperAdminHttpApiService.api_helper(
            token=token)

        response_code, response_data = api_helper.post(url=url, data={
            "amount_to_be_sent": amount_to_be_sent,
            "employee_account_id": employee_account_id,
            "hr_admin_account_id": hr_admin_account_id
        })

        if response_code == 201 and response_data.get("status") == "success":

            return True

        return None
