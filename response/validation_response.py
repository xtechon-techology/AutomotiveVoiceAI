from pydantic import BaseModel, Field


class ValidationResponse(BaseModel):
    sql_query: str = Field(description="Corrected SQL query")
    explanation: str = Field(description="Verbose explanation of fixing query")
