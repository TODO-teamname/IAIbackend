from rest_framework.exceptions import APIException

class ServiceUnavailable(APIException):
    status_code=503
    default_detail= 'Service unavailable, check your url or try again later.'
    default_code = 'service_unavailable'

class ProxyAuthenticationRequired(APIException):
    status_code=407
    default_detail= 'Invalid credentials for external server, check your token'
    default_code = 'proxy_autnehtication_required'

class ExternalResourceNotFound(APIException):
    status_code=404
    default_detail = 'External Resource unavailable'
    default_code = 'external_resource_not_found'
