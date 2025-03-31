from pydantic import BaseModel

class JobConversationMessageEntitySchema(BaseModel):
    body: str | None
    photos: str
    userId: str
    sentViaMobile: bool | None
    id: str
    isHidden: bool | None
