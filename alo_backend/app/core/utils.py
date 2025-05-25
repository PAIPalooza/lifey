from typing import Any, Dict, Optional, Union

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


def get_error_response(
    status_code: int, message: str, errors: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Generate a standardized error response."""
    return {
        "status_code": status_code,
        "message": message,
        "errors": errors or {},
    }


def handle_http_exception(
    exc: HTTPException,
) -> Dict[str, Any]:
    """Handle HTTP exceptions and return a standardized error response."""
    return get_error_response(
        status_code=exc.status_code,
        message=exc.detail,
        errors=getattr(exc, "errors", None),
    )


def validate_request(
    data: Union[BaseModel, Dict[str, Any]], model: type
) -> BaseModel:
    """Validate request data against a Pydantic model."""
    if isinstance(data, dict):
        try:
            return model(**data)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=jsonable_encoder(e.errors()),
            )
    return data


def get_pagination_links(
    url: str, skip: int, limit: int, total: int
) -> Dict[str, Optional[str]]:
    """Generate pagination links for list responses."""
    base_url = f"{url}?"
    if skip + limit < total:
        next_url = f"{base_url}skip={skip + limit}&limit={limit}"
    else:
        next_url = None
    
    if skip > 0:
        prev_skip = max(0, skip - limit)
        prev_url = f"{base_url}skip={prev_skip}&limit={limit}"
    else:
        prev_url = None
    
    return {"next": next_url, "prev": prev_url}
