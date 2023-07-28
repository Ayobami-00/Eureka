from base64 import b64encode
import logging
from typing import Dict
import requests
import json
from src.schema.employee_virtual_account import CompanyProvidusAccountTransferCreate, EmployeeProvidusAccountTransferCreate, EmployeeVirtualAccountTransaction, EmployeeVirtualAccountTransferCreate
from src.schema.base import Currency, EmployeeVirtualAccountTransactionStatusEnum, EnvironmentEnum
from src.services.external.bridgecard_issuing_service import BridgecardIssuingService
from src.core.error import generic_error_response
from src.schema.employee import EmployeeOutInternal
from src.utils import constants
from src.core.config import settings
from src.core import error as errors
from AesEverywhere import aes256

from src.utils.api_helper import ApiHelper
from src.utils.methods import format_date, is_production, format_time
from src.utils.custom_app_logger import CustomAppLogger

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


class BridgecardCreditIssuingService:

    def api_helper(token: str):

        api_helper = ApiHelper(token=token)

        return api_helper

    def get_virtual_account_balance(environment: EnvironmentEnum, employee_data: EmployeeOutInternal, cardholder_id: str):

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN:

            get_virtual_account_balance_error, get_virtual_account_balance_result = BridgecardIssuingService.check_virtual_account_balance(
                environment=environment,
                cardholder_id=cardholder_id,
            )

            if get_virtual_account_balance_error:

                return get_virtual_account_balance_error, {}

            return {}, get_virtual_account_balance_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def get_virtual_account_transactions(environment: EnvironmentEnum, employee_data: EmployeeOutInternal, page: int, cardholder_id: str):

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN:

            get_naira_account_transactions_error, get_naira_account_transactions_result = BridgecardIssuingService.get_naira_account_transactions(
                environment=environment,
                cardholder_id=cardholder_id,
                page=page,
            )

            if get_naira_account_transactions_error:

                return get_naira_account_transactions_error, {}

            transactions = get_naira_account_transactions_result.get(
                "transactions")

            refactored_transaction_list = []

            for transaction in transactions:

                transaction_amount = transaction.get("amount")
                transaction_date_string = format_date(
                    transaction.get("transaction_date"))
                transaction_time_string = format_time(
                    transaction.get("transaction_date"))
                transaction_status = EmployeeVirtualAccountTransactionStatusEnum.SUCCESSFUL.value
                transaction_reference = transaction.get(
                    "transaction_reference")
                transaction_currency = employee_salary_currency.value
                transaction_narration = transaction.get("description")
                transaction_type = transaction.get("card_transaction_type")

                transaction = EmployeeVirtualAccountTransaction(transaction_amount=transaction_amount, transaction_date_string=transaction_date_string,
                                                                transaction_time_string=transaction_time_string, transaction_status=transaction_status, transaction_reference=transaction_reference,
                                                                transaction_currency=transaction_currency, transaction_narration=transaction_narration, transaction_type=transaction_type)

                refactored_transaction_list.append(transaction)

                get_naira_account_transactions_result["transactions"] = refactored_transaction_list

            return {}, get_naira_account_transactions_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def freeze_card(employee_data: EmployeeOutInternal):

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN:

            freeze_card_error, freeze_card_result = BridgecardIssuingService.freeze_card(
                environment=environment,
                card_id=employee_data.employee_card_details.card_id,
            )

            if freeze_card_error:

                return freeze_card_error, {}

            return {}, freeze_card_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def unfreeze_card(employee_data: EmployeeOutInternal):

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN:

            unfreeze_card_error, unfreeze_card_result = BridgecardIssuingService.unfreeze_card(
                environment=environment,
                card_id=employee_data.employee_card_details.card_id,
            )

            if unfreeze_card_error:

                return unfreeze_card_error, {}

            return {}, unfreeze_card_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def get_ngn_bank_codes(environment: EnvironmentEnum, employee_data: EmployeeOutInternal):

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN:

            get_all_bank_codes_error, get_all_bank_codes_result = BridgecardIssuingService.get_all_bank_codes(
                environment=environment,
            )

            if get_all_bank_codes_error:

                return get_all_bank_codes_error, {}

            banks = get_all_bank_codes_result.get("banks")

            data_list = []

            for data in banks:

                bankName = data.get("bankName")

                bankCode = data.get("bankCode")

                data_list.append({"label": bankName, "value": bankCode})

            return {}, {"banks": data_list}

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def verify_account_number(account_number: str,
                              bank_code: str, employee_data: EmployeeOutInternal
                              ):

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        if employee_salary_currency == Currency.NGN.value:

            verify_account_number_error, verify_account_number_result = BridgecardIssuingService.verify_account_number(
                environment=environment,
                account_number=account_number,
                bank_code=bank_code
            )

            if verify_account_number_error:

                return verify_account_number_error, {}

            return {}, verify_account_number_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def third_party_transfer(transfer_create: EmployeeVirtualAccountTransferCreate, employee_data: EmployeeOutInternal,
                             ):

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        if employee_salary_currency == Currency.NGN.value:

            third_party_transfer_error, third_party_transfer_result = BridgecardIssuingService.virtual_account_third_party_transfer(
                environment=environment,
                beneficiary_account_name=transfer_create.transfer_recipient_account_name,
                transaction_amount=transfer_create.transfer_amount,
                narration=transfer_create.transfer_narration,
                beneficiary_account_number=transfer_create.transfer_recipient_account_number,
                beneficiary_bank_code=transfer_create.transfer_recipient_bank_code,
                cardholder_id=employee_data.employee_cardholder_details.cardholder_id
            )

            if third_party_transfer_error:

                return third_party_transfer_error, {}

            return {}, third_party_transfer_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def providus_account_transfer(transfer_create: EmployeeProvidusAccountTransferCreate, employee_data: EmployeeOutInternal,
                                  ):

        employee_salary_currency = employee_data.employee_employment_details.current_salary.currency

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        if employee_salary_currency == Currency.NGN.value:

            providus_account_transfer_error, providus_account_transfer_result = BridgecardIssuingService.providus_account_transfer(
                environment=environment,
                credit_account=transfer_create.transfer_recipient_account_number,
                transaction_amount=transfer_create.transfer_amount,
                narration=transfer_create.transfer_narration,
                cardholder_id=employee_data.employee_cardholder_details.cardholder_id
            )

            if providus_account_transfer_error:

                return providus_account_transfer_error, {}

            return {}, providus_account_transfer_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}

    def company_third_party_transfer(data: CompanyProvidusAccountTransferCreate, employee_salary_currency: str
                                     ):

        environment = EnvironmentEnum.production if is_production() else EnvironmentEnum.sandbox

        if employee_salary_currency == Currency.NGN.value:

            company_providus_account_transfer_error, company_providus_account_transfer_result = BridgecardIssuingService.company_providus_account_transfer(
                environment=environment,
                beneficiary_account_name=data.transfer_recipient_account_name,
                transaction_amount=data.transfer_amount,
                narration=data.transfer_narration,
                beneficiary_account_number=data.transfer_recipient_account_number,
                beneficiary_bank_code=data.transfer_recipient_bank_code,
                company_name=data.company_name
            )

            if company_providus_account_transfer_error:

                return company_providus_account_transfer_error, {}

            return {}, company_providus_account_transfer_result

        else:

            return errors.generic_error_response(400, "Your Salary Account is not currently supported, please contact support."), {}
