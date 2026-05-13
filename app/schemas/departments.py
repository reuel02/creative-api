from pydantic import BaseModel, ConfigDict

class DepartmentResponse(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)
