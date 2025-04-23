class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, APIException):
            return JsonResponse({
                'error': exception.detail,
                'status_code': exception.status_code
            }, status=exception.status_code)
        
        return JsonResponse({
            'error': 'Internal server error',
            'status_code': 500
        }, status=500)