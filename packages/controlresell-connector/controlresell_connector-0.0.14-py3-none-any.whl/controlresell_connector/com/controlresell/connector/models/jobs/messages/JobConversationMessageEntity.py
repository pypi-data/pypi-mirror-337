from pydantic import BaseModel

class JobConversationMessageEntitySchema(BaseModel):
    body: str | None
    photos: list[str]
    userId: str
    sentViaMobile: bool | None
    id: str
    isHidden: bool | None
