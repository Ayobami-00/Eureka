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
from src.utils.methods import data_mapper
from src.utils.custom_app_logger import CustomAppLogger

from . import constants as identity_pass_verification_service_constants

from src.utils import constants

logger = CustomAppLogger.setup_logger(log_name=__name__)


current_version = "v1"

BASEURL = identity_pass_verification_service_constants.IDENTITY_PASS_VERIFICATION_DETAILS_BASE_URL


class IdentityPassVerificationService():

    def bvn_verification(bvn: str):

        url = BASEURL + "/api/v2/biometrics/merchant/data/verification/bvn"

        payload = {
            "number": bvn
        }

        headers = {
            "Accept": "application/json",
            "Content-Type":  "application/json",
            "x-api-key": settings.IDPASS_LIVE_SECRET_KEY,
            "app-id": settings.IDPASS_APP_ID
        }

        api_helper = ApiHelper(headers=headers)

        response_code, response_data = api_helper.post(url=url, data=payload)

        if response_code == 200 and response_data.get("bvn_data") != None and response_data.get("status") != None:

            return response_data.get("status"), data_mapper(data=response_data.get("bvn_data"), mapping=identity_pass_verification_service_constants.BVN_DETAILS_DATA_MAPPING)

        else:

            return False, {}
