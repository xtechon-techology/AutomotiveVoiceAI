from pydantic import BaseModel, Field
from typing import List, Optional


class SQLQueryResponse(BaseModel):
    sql_query: str = Field(
        description="Sql query generated for user question. This is empty if you cannot generate the SQL query"
    )
    explanation: str = Field(
        description="Short explanation for generating or not generating the sql query, include table names in the explanation."
    )
    visualisation_chart_name: str = Field(
        description="Visualization chart names applicable for the query: Pie Chart, Bar Chart, Line Chart, Funnel Chart"
    )
    title: str = Field(description="title for the chart")
