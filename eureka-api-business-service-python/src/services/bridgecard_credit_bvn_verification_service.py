from base64 import b64encode
import logging
from typing import Dict
import requests
import json
from src.core.error import generic_error_response
from src.schema.verification import VerifiedBVNDetails
from src.schema.employee import EmployeeOutInternal
from src.services.external.identity_pass_verification_service import IdentityPassVerificationService
from src.utils import constants
from src.core.config import settings
from AesEverywhere import aes256

from src.utils.api_helper import ApiHelper
from src.utils.methods import generateRandomEmail, is_production, number_sequence
from src.utils.verification import verify_bvn_match_with_employee_names
from src.utils.methods import generate_logcode, generate_spanid, generate_traceid, getCurrentTimestamp, getTimestampAfterMinutesFromNow, number_sequence
from src.utils.generate_token import generate_internal_api_token
from src.utils.verification import generateOtp
from src.utils.custom_app_logger import CustomAppLogger, CustomAppLoggerLogData
from src.utils.distributed_tracing import sentry_span_trace

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"


class BridgecardCreditBvnVerificationiService:

    def api_helper(token: str):

        api_helper = ApiHelper(token=token)

        return api_helper

    @sentry_span_trace
    def verify_bvn(bvn: str, employee_data: EmployeeOutInternal, employee_account_id: str, traceid: str):

        number_sequence_gen = number_sequence()

        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="STARTED OPERATION ON `BridgecardCreditBvnVerificationiService` TO `verify_bvn`", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
            "bvn": bvn,
            "employee_data": employee_data.dict(),
            "employee_account_id": employee_account_id
        }).dict())

        is_env_production = is_production()

        if not is_env_production:

            verified_bvn_details = VerifiedBVNDetails(
                **constants.DUMMY_BVN_DETAILS)

            error_response = {}

            next_seq = next(number_sequence_gen)
            CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="COMPLETED OPERATION TO VERIFY BVN IN SANDBOX", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
                traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
                "response_data": verified_bvn_details.dict(),
                "error_response": error_response,
            }).dict())

            return error_response, verified_bvn_details

        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="MAKING CALL TO `IdentityPassVerificationService` TO DO `bvn_verification`", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
            "bvn": bvn,
        }).dict())

        bvn_verification_status, bvn_verification_result = IdentityPassVerificationService.bvn_verification(
            bvn=bvn)

        bvn_verification_result = VerifiedBVNDetails(**bvn_verification_result)

        if bvn_verification_status == False:

            error_response = "Employee BVN could not be verified, please check input and try again."

            response_data = {}

            CustomAppLogger.log_error(logger, CustomAppLoggerLogData(message="ERROR AFTER MAKING CALL TO `IdentityPassVerificationService` TO DO `bvn_verification",
                                      callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
                                          traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
                                          "error_response": error_response,
                                      }).dict(),)

            return generic_error_response(status_code=400, message=error_response), response_data

        next_seq = next(number_sequence_gen)
        CustomAppLogger.log_info(logger, CustomAppLoggerLogData(message="COMPLETED CALL TO `IdentityPassVerificationService` TO DO `bvn_verification`", callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
            traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
            "bvn_verification_status": bvn_verification_status,
            "bvn_verification_result": bvn_verification_result
        }).dict())

        if bvn_verification_result.watch_listed == "YES":

            error_response = "Oops.. your BVN might have been associated with some fraud or bad record recently so we couldn't enroll you. please contact your bank."

            response_data = {}

            CustomAppLogger.log_error(logger, CustomAppLoggerLogData(message="ERROR AFTER MAKING CALL TO `IdentityPassVerificationService` TO DO `bvn_verification",
                                      callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
                                          traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
                                          "error_response": error_response,
                                      }).dict(),)

            return generic_error_response(status_code=403, message=error_response), response_data

        if verify_bvn_match_with_employee_names(bvn_result=bvn_verification_result, employee_data=employee_data) is False:

            error_response = "Employee's name doesn't match the name on the bvn provided"

            response_data = {}

            CustomAppLogger.log_error(logger, CustomAppLoggerLogData(message="ERROR AFTER MAKING CALL TO `IdentityPassVerificationService` TO DO `bvn_verification",
                                      callerid=employee_account_id, traceid=traceid, spanid=generate_spanid(
                                          traceid, next_seq), logcode=generate_logcode("BCBVS-VB", next_seq), logdata={
                                          "error_response": error_response,
                                      }).dict(),)

            return generic_error_response(status_code=400, message=error_response), response_data

        return {}, bvn_verification_result,
