from pydantic import BaseModel, Field, field_validator


class IMEIValidator(BaseModel):
    imei: str = Field(...)

    @field_validator("imei")
    def validate_imei(cls, value):
        if not value.isdigit():
            raise ValueError("IMEI должен содержать только цифры.")

        if not 8 <= len(value) <= 15:
            raise ValueError("IMEI должен быть длиной от 8 до 15 символов.")

        return value
