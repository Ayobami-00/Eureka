from typing import Dict
import uuid
import src.utils.constants as constants
from src.core.config import settings
from src.schema.base import EnvironmentEnum
import src.core.error as errors
import requests
import base64
import json
import logging
from datetime import datetime
import re

from src.utils.api_helper import ApiHelper
from src.utils.methods import generateRandomId
from src.utils.custom_app_logger import CustomAppLogger

from . import constants as bridgecard_issuing_service_constants

from . import methods as bridgecard_issuing_service_methods

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


BASEURL = bridgecard_issuing_service_constants.BRIDGECARD_ISSUING_SERVICE_BASE_URL


class BridgecardIssuingService():

    def check_virtual_account_balance(

        environment: EnvironmentEnum,
        cardholder_id: str,
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/check_account_balance?cardholder_id={cardholder_id}"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/check_account_balance?cardholder_id={cardholder_id}"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.get(
                url=url, )

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to fetch naira account balance, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to fetch naira account balance, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to fetch naira account balance, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def get_naira_account_transactions(

        environment: EnvironmentEnum,
        cardholder_id: str,
        page: int
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/get_naira_account_transactions?cardholder_id={cardholder_id}&page={page}"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/get_naira_account_transactions?cardholder_id={cardholder_id}&page={page}"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.get(
                url=url)

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to fetch naira account transactions, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to fetch naira account transactions, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to fetch naira account transactions, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def freeze_card(

        environment: EnvironmentEnum,
        card_id: str,
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/cards/freeze_card?card_id={card_id}"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/cards/freeze_card?card_id={card_id}"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.patch(
                url=url)

            if response_code == 200:

                return {}, True

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to freeze card, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), False

            else:
                error_message = (
                    "Failed to freeze card, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), False

        except Exception as e:
            error_message = (
                "Failed to freeze card, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), False

    def unfreeze_card(

        environment: EnvironmentEnum,
        card_id: str,
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/cards/unfreeze_card?card_id={card_id}"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/cards/unfreeze_card?card_id={card_id}"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.patch(
                url=url)

            if response_code == 200:

                return {}, True

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to unfreeze card, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), False

            else:
                error_message = (
                    "Failed to unfreeze card, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), False

        except Exception as e:
            error_message = (
                "Failed to unfreeze card, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), False

    def get_all_bank_codes(

        environment: EnvironmentEnum,
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/get_all_bank_codes"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/get_all_bank_codes"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.get(
                url=url)

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to fetch naira account transactions, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to fetch naira account transactions, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to fetch naira account transactions, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def verify_account_number(

        environment: EnvironmentEnum,
        account_number: str,
        bank_code: str,
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/verify_account_number?account_number={account_number}&bank_code={bank_code}"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/verify_account_number?account_number={account_number}&bank_code={bank_code}"

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.get(
                url=url)

            if response_code == 200 and response_data["data"]["is_verified"] != False:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to verify account number, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to verify account number, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to verify account number, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def virtual_account_third_party_transfer(

        environment: EnvironmentEnum,
        beneficiary_account_name: str,
        transaction_amount: str,
        narration: str,
        beneficiary_account_number: str,
        beneficiary_bank_code: str,
        cardholder_id: str
    ):

        try:

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/third_party_transfer"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/third_party_transfer"

                response_code = 201

                response_data = {
                    "status": "success",
                    "message": "Virtual account was created successfully",
                    "data": {
                        "transaction_reference": generateRandomId()
                    }
                }

                return {}, response_data["data"]

            payload = {
                "beneficiary_account_name": beneficiary_account_name,
                "transaction_amount": transaction_amount,
                "narration": narration,
                "beneficiary_account_number": beneficiary_account_number,
                "beneficiary_bank_code": beneficiary_bank_code,
                "cardholder_id": cardholder_id
            }

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.post(
                url=url, data=payload)

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to perform virtual account third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to perform virtual account third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to perform virtual account third party transfer, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def providus_account_transfer(

        environment: EnvironmentEnum,
        credit_account: str,
        transaction_amount: str,
        narration: str,
        cardholder_id: str
    ):

        try:

            # response_code = 201

            # response_data = {
            #     "status": "success",
            #     "message": "Virtual account was created successfully",
            #     "data": {
            #         "account_nuban": "1234567890",
            #         "account_name": "JOHN DOE",
            #         "bank_code": "010101"
            #     }
            # }

            # return {}, response_data["data"]

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/providus_account_transfer"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/providus_account_transfer"
                
                response_code = 201

                response_data = {
                    "status": "success",
                    "message": "Virtual account was created successfully",
                    "data": {
                        "transaction_reference": generateRandomId()
                    }
                }

                return {}, response_data["data"]

            payload = {
                "credit_account": credit_account,
                "transaction_amount": transaction_amount,
                "narration": narration,
                "cardholder_id": cardholder_id
            }

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.post(
                url=url, data=payload)

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to perform virtual account third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to perform virtual account third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to perform virtual account third party transfer, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}

    def company_providus_account_transfer(

        environment: EnvironmentEnum,
        beneficiary_account_name: str,
        transaction_amount: str,
        narration: str,
        beneficiary_account_number: str,
        beneficiary_bank_code: str,
        company_name: str
    ):

        try:

            # response_code = 201

            # response_data = {
            #     "status": "success",
            #     "message": "Virtual account was created successfully",
            #     "data": {
            #         "account_nuban": "1234567890",
            #         "account_name": "JOHN DOE",
            #         "bank_code": "010101"
            #     }
            # }

            # return {}, response_data["data"]

            url = ""

            if environment == EnvironmentEnum.production:

                url = BASEURL + \
                    f"/v1/issuing/naira_cards/company_providus_account_transfer"

            else:

                url = BASEURL + \
                    f"/v1/issuing/{environment.value}/naira_cards/company_providus_account_transfer"

            payload = {
                "credit_account": beneficiary_account_number,
                "transaction_amount": transaction_amount,
                "narration": narration,
                "company_name": company_name
            }

            headers = {
                "Content-Type": "application/json",
                "token": f"Bearer {settings.BRIDGECARD_ISSUING_LIVE_AUTHORIZATION_TOKEN if environment == EnvironmentEnum.production else settings.BRIDGECARD_ISSUING_TEST_AUTHORIZATION_TOKEN}",
            }

            api_helper = ApiHelper(headers=headers)

            response_code, response_data = api_helper.post(
                url=url, data=payload)

            if response_code == 200:

                return {}, response_data["data"]

            elif response_code == 400:

                error_message = (
                    response_data["message"]
                    or "Failed to perform company third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

            else:
                error_message = (
                    "Failed to perform company third party transfer, please check your details and try again"
                )

                return errors.generic_error_response(400, error_message), {}

        except Exception as e:
            error_message = (
                "Failed to perform company third party transfer, please check your details and try again"
            )

            return errors.generic_error_response(400, error_message), {}
