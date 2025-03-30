"""
Types checking functionality
"""

from functools import wraps

from pydantic import BaseModel as BaseType, ValidationError

from .errors import ErrorSpecified, ErrorType


def _strip(data):
    """Remove extra indentation"""

    if not isinstance(data, dict):
        return

    for field in set(data):
        if isinstance(data[field], str):
            data[field] = data[field].strip()
            continue

        if isinstance(data[field], dict):
            _strip(data[field])
            continue

        if isinstance(data[field], (list, tuple, set)):
            for el in data[field]:
                _strip(el)


def _check(data, filters):
    """Convert the parameters to the required object"""

    try:
        return filters(**data)

    except ValidationError as e:
        field = e.errors()[0]["loc"][0]

        if field in data:
            raise ErrorType(field) from e

        raise ErrorSpecified(field) from e


def validate(filters):
    """Validation of function parameters"""

    def decorator(f):
        @wraps(f)
        def wrapper(request, data):
            _strip(data)
            data = _check(data, filters)
            return f(request, data)

        return wrapper

    return decorator


__all__ = (
    "BaseType",
    "validate",
)
