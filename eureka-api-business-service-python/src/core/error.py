from typing import Any, Dict, Optional

from fastapi import HTTPException, status
import grpc


def duplicated_error(context: grpc.aio.ServicerContext, detail: Any = None):
    
    context.abort(grpc.StatusCode.ALREADY_EXISTS, detail)


def auth_error(context: grpc.aio.ServicerContext, detail: Any = None):

    context.abort(grpc.StatusCode.PERMISSION_DENIED, detail)


def not_found_error(context: grpc.aio.ServicerContext, detail: Any = None):

    context.abort(grpc.StatusCode.NOT_FOUND, detail)

def validation_error(context: grpc.aio.ServicerContext, detail: Any = None):

    context.abort(grpc.StatusCode.INVALID_ARGUMENT, detail)
