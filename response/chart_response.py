from pydantic import BaseModel, Field
from typing import List, Optional


class AxisDetails(BaseModel):
    x_axis: str = Field(description="dict key name from resultset to be used as x axis")
    y_axis: str = Field(description="dict key name from resultset to be used as y axis")
    x_axis_missing_key: str = Field(
        description="dict key name missing in resultset to be used as x axis"
    )
    x_axis_missing_data: str = Field(description="value of missing key from resultset")
    y_axis_missing_key: str = Field(
        description="dict key name missing in resultset to be used as y axis"
    )
    y_axis_missing_data: str = Field(description="value of missing key from resultset")


class ChartResponse(BaseModel):
    chart_type: str = Field(description="type of chart to be used")
    title: str = Field(description="title for the chart")
    axis_details: AxisDetails = Field(
        description="X axis and Y axis key names from the query resultset"
    )
