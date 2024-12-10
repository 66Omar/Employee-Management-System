from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework import exceptions
import logging

logger = logging.getLogger(__name__)


def global_exception_handler(exc, context):
    """
    Custom global exception handler with improved error reporting
    """

    response = exception_handler(exc, context)

    view_name = (
        context.get("view", None).__class__.__name__
        if context.get("view")
        else "UnknownView"
    )

    # Log the exception with additional context
    logger.error(
        f"Exception occurred in {view_name}.",
        exc_info=True,
        extra={
            "exception_type": exc.__class__.__name__,
            "exception_details": str(exc),
            "context": context,
        },
    )

    # Handle ValidationError more specifically
    if isinstance(exc, exceptions.ValidationError):
        # Extract detailed validation errors
        if hasattr(exc, "detail"):
            error_details = {}

            # Handle different types of validation error structures
            if isinstance(exc.detail, dict):
                for field, errors in exc.detail.items():
                    # Ensure errors is a list
                    errors = errors if isinstance(errors, list) else [errors]
                    error_details[field] = [
                        (
                            str(error)
                            if not isinstance(error, dict)
                            else error.get("message", str(error))
                        )
                        for error in errors
                    ]
            elif isinstance(exc.detail, list):
                error_details["non_field_errors"] = [str(error) for error in exc.detail]

            response = Response(
                {
                    "success": False,
                    "error": {
                        "type": exc.__class__.__name__,
                        "detail": error_details,
                        "status_code": status.HTTP_400_BAD_REQUEST,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    elif response is not None:
        response.data = {
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "detail": (
                    response.data.get("detail")
                    if isinstance(response.data, dict)
                    else response.data
                ),
                "status_code": response.status_code,
            },
        }
    else:
        response = Response(
            {
                "success": False,
                "error": {
                    "type": exc.__class__.__name__,
                    "detail": str(exc),
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                },
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
