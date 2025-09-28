from sqlmodel import SQLModel, Field,Relationship


class Users(SQLModel,table=True):
    id: int = Field(default=None,primary_key=True)
    username: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)