from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Get the standard DRF response first
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "error": str(exc),
            "details": response.data,
        }

    return response
