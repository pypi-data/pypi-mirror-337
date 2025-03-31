from typing import Union
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()
prefix = __name__.split('.')[-2]
prefix = '_'.join(prefix.split('_')[2:])
dependencies = []
DEFAULT_CONFIG = {}

def init(config):
    """Initialize the router with the given configuration.

    You can initialize database connection and pass other configuration in module.

    Args:
        config: A configparser.ConfigParser object containing the configuration.

    Returns:
        The initialized APIRouter object.
    """
    return router

tags_metadata = [
    {
        "name": "User",
        "description": "Operations related to the authenticated user",
    }
]

class UserResponseMessage(BaseModel):
    id: int
    email: str
    role: str

class ResponseMessage(BaseModel):
    detail: Union[str,
                  UserResponseMessage]
    error: str | None = None
    message: str | None = None
    status_code: int = 200

@router.get("/")
    async def get_testroute():
        """This is a test route."""
        return ResponseMessage(detail="OK")

@router.get("/user", tags=["User"], response_model=ResponseMessage)
async def get_user_route():
    """This endpoint returns information about the currently authenticated user."""
    return ResponseMessage(
        message="User information",
        detail=UserResponseMessage(
            id=0,
            email='user@example.com',
            role='user'
        )
    )
