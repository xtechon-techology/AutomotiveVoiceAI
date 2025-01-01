response = {
   "sql_query":"SELECT SUM(PartsCost) AS TotalPartsRevenue, FORMAT(ServiceDate, 'yyyy-MM') AS ServiceMonth FROM ServiceJobs WHERE ServiceDate >= DATEADD(MONTH, -3, GETDATE()) GROUP BY FORMAT(ServiceDate, 'yyyy-MM') ORDER BY ServiceMonth",
   "format_instructions":"The output should be formatted as a JSON instance that conforms to the JSON schema below.\n\nAs an example, for the schema {\"properties\": {\"foo\": {\"title\": \"Foo\", \"description\": \"a list of strings\", \"type\": \"array\", \"items\": {\"type\": \"string\"}}}, \"required\": [\"foo\"]}\nthe object {\"foo\": [\"bar\", \"baz\"]} is a well-formatted instance of the schema. The object {\"properties\": {\"foo\": [\"bar\", \"baz\"]}} is not well-formatted.\n\nHere is the output schema:\n```\n{\"properties\": {\"sql_query\": {\"description\": \"The SQL query generated for the user question.\", \"title\": \"Sql Query\", \"type\": \"string\"}, \"function_prototype\": {\"description\": \"The function prototype for generating a visualization.\", \"title\": \"Function Prototype\", \"type\": \"string\"}, \"function_prototype_json\": {\"description\": \"The function prototype in JSON format, including x_column, y_column, and title.\", \"title\": \"Function Prototype Json\", \"type\": \"object\"}}, \"required\": [\"sql_query\", \"function_prototype\", \"function_prototype_json\"]}\n```",
   "text":"{\"sql_query\": \"SELECT SUM(PartsCost) AS TotalPartsRevenue, FORMAT(ServiceDate, \\'yyyy-MM\\') AS ServiceMonth FROM ServiceJobs WHERE ServiceDate >= DATEADD(MONTH, -3, GETDATE()) GROUP BY FORMAT(ServiceDate, \\'yyyy-MM\\') ORDER BY ServiceMonth\", \"function_prototype\": \"generate_plotly_chart_js(df, x_column=, y_column=, title=)\", \"function_prototype_json\": {\"x_column\": \"ServiceMonth\", \"y_column\": \"TotalPartsRevenue\", \"title\": \"Total Parts Revenue in the Last 3 Months\"}}"
}

import json

# replace \ & \\ with empty string
response["text"] = response["text"].replace("\\", "")

# Parse the response
response = json.loads(response["text"])

# Print sql_query
print(response["sql_query"])

# Print function_prototype
print(response["function_prototype"])

# Print function_prototype_json
function_prototype_json = response["function_prototype_json"]
print(response["function_prototype_json"])
print(f"x_column: {function_prototype_json['x_column']}")
print(f"y_column: {function_prototype_json['y_column']}")
print(f"title: {function_prototype_json['title']}")

