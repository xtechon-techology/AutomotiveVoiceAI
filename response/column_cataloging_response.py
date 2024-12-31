from pydantic import BaseModel, Field
from typing import List, Optional


class ColumnDescription(BaseModel):
    column_name: str = Field(description="column name")
    description: str = Field(
        description="Verbose description for the column and is a mandatory field."
    )


class ColumnCatalogingResponse(BaseModel):
    column_descriptions: List[ColumnDescription]
