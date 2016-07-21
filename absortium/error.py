__author__ = 'andrew.shvv@gmail.com'


class AbsortiumError(Exception):
    """Base error class for all exceptions raised in this library.
    Will never be raised naked; more specific subclasses of this exception will
    be raised when appropriate."""


class APIError(AbsortiumError):
    """Raised for errors related to interacting with the Absortium API server."""

    def __init__(self, response, _id, message):
        self.status_code = response.status_code
        self.response = response
        self.id = _id
        self.message = message or ''
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'APIError(id=%s): %s' % (self.id, self.message)


class ValidationError(APIError): pass


class AuthenticationError(APIError): pass


class NotFoundError(APIError): pass


class InternalServerError(APIError): pass


class PermissionDeniedError(APIError): pass


class NotEnoughMoneyError(APIError): pass


class LockFailureError(APIError): pass


class UnlockFailureError(APIError): pass


class UpdateFailureError(APIError): pass


class AlreadyExistError(APIError): pass


class NotAllowedError(APIError): pass


def build_api_error(response):
    """Helper method for creating errors and attaching HTTP response/request
    details to them.
    """
    blob = response.json()
    error_id = blob.get('error_id', None)

    if error_id:
        error_message = blob.get('detail')
        error_class = _error_id_to_class.get(error_id)
        return error_class(response, error_id, error_message)
    else:
        return None


_error_id_to_class = {
    'not_found': NotFoundError,
    'internal_server_error': InternalServerError,
    'permission_denied': PermissionDeniedError,
    'not_enough_money': NotEnoughMoneyError,
    'lock_failure': LockFailureError,
    'unlock_failure': UnlockFailureError,
    'update_failure': UpdateFailureError,
    'already_exist': AlreadyExistError,
    'not_allowed': NotAllowedError,
    'validation_error': ValidationError,
    'authentication_error': AuthenticationError,
}
