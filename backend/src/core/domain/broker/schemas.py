from typing import Dict

from pydantic import BaseModel


class MessageSchema(BaseModel):
    payload: Dict
    queue_name: str
