from curryproxy.responses import error_response
from curryproxy.responses import metadata_response
from curryproxy.responses import multiple_response
from curryproxy.responses import single_response

# Hoist classes into the package namespace
ErrorResponse = error_response.ErrorResponse
MetadataResponse = metadata_response.MetadataResponse
MultipleResponse = multiple_response.MultipleResponse
SingleResponse = single_response.SingleResponse
