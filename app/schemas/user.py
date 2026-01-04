from pydantic import BaseModel, Emailstr, field_validator, model_validator
from typing_extensions import Self
from fastapi import HTTPException

# 260102 김광원
# User 모델 검증
class NewUserForm(BaseModel):
    email: str
    name: str
    password: str
    password_reapeat: str

    # 참조 : https://docs.pydantic.dev/latest/concepts/validators/#model-validators
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_reapeat:
            raise ValueError("Passwords do not match")
        return self