from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int
    name: str
    phone: str
    gender: str


class UserOut(UserCreate):
    class Config:
        orm_mode = True


class AdminCreate(BaseModel):
    user_id: int


class AdminOut(AdminCreate):
    user: UserOut

    class Config:
        orm_mode = True
