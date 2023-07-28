from base64 import b64encode
import logging
from typing import Dict
import requests
import json
from src.utils import constants
from src.core.config import settings
from AesEverywhere import aes256

from src.utils.api_helper import ApiHelper
from src.utils.methods import generate_logcode, generate_spanid, is_production, number_sequence
from src.utils.distributed_tracing import sentry_span_trace
from src.utils.custom_app_logger import CustomAppLogger, CustomAppLoggerLogData


BASEURL = settings.BRIDGECARD_CREDIT_CLOUD_FUNCTION_HTTP_API_SERVICE_BASE_URL

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


class BridgecardCreditCloudFunctionHttpApiService:

    def api_helper(token: str):

        api_helper = ApiHelper(token=token)

        return api_helper
    

    @sentry_span_trace
    def employee_otp_verification(token: str, payload: Dict, traceid: str):

        url = BASEURL + constants.API_V1

        if not is_production():

            url += "/sandbox/email_service/employee-otp-verification"

        else:

            url += "/email_service/employee-otp-verification"

        
        employee_account_id = payload.get("employee_account_id")

        number_sequence_gen = number_sequence()

        #BCCFHAS0
        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="STARTED OPERATION TO PROCES EMAIL NOTIFICATION FOR EMPLOYEE OTP VERIFICATION MAIL TYPE", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCCFHAS", next_seq), logdata={
            "employee_account_id": employee_account_id,
            "payload": payload,
            "token": token,
            "url": url,
        }).dict())

        api_helper = BridgecardCreditCloudFunctionHttpApiService.api_helper(
            token=token)

        response_code, response_data = api_helper.post(url=url,data=payload)

        #BCCFHAS1
        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="COMPLETED OPERATION TO PROCES EMAIL NOTIFICATION FOR EMPLOYEE OTP VERIFICATION MAIL TYPE", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCCFHAS", next_seq), logdata={
            "employee_account_id": employee_account_id,
            "response_code": response_code,
            "response_data": response_data,
            "url": url,
        }).dict())

        if response_code == 200 and response_data.get("response") == "success":

            return True
        
        #BCCFHAS2
        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_error(logger, CustomAppLoggerLogData(message="ERROR WHILE PROCESSING EMAIL NOTIFICATION FOR EMPLOYEE OTP VERIFICATION MAIL TYPE", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCCFHAS", next_seq), logdata={
            "employee_account_id": employee_account_id,
            "response_code": response_code,
            "response_data": response_data,
            "url": url,
        }).dict())

        return False
    
    