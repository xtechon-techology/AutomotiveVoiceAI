from pydantic import BaseModel, Field
from typing import List, Optional


class KpiDetails(BaseModel):
    kpi_name: str = Field(
        description="Key Performance Indicators (KPIs) with trends and relationships."
    )
    query: str = Field(description="SQL query generated")
    visualisation_chart_name: str = Field(
        description="Visualization chart names applicable for the query: Pie Chart, Bar Chart, Line Chart, Funnel Chart"
    )
    referenced_columns: List[str] = Field(
        description="Comma separated list of all the columns that are being referenced in the generated query"
    )
    referenced_tables: List[str] = Field(
        description="Comma separated list of all the tables that are being used in the generated query"
    )


class KpiResponse(BaseModel):
    sql_query: str = Field(description="Spark sql query generated for user question")
    kpi_list: List[KpiDetails] = Field(description="List of KPI details.")
