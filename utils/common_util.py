import re
import json

import re
import json


def correct_json(json_text):
    """
    Corrects common JSON formatting issues to make it valid for parsing.

    Args:
        json_text (str): The JSON-like string to correct.

    Returns:
        str: The corrected JSON string.
    """
    if not json_text or not isinstance(json_text, str):
        raise ValueError("Input must be a non-empty string")

    # Remove triple backticks and surrounding whitespace
    json_text = re.sub(r"```", "", json_text).strip()

    # Replace single quotes with double quotes for JSON compliance
    json_text = re.sub(r"(?<!\\)'", '"', json_text)

    # Fix missing commas by adding them between closing braces/brackets and subsequent strings
    json_text = re.sub(r'([}\]])\s*([{\["])', r'\1,\2', json_text)

    # Escape unescaped backslashes
    json_text = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', json_text)

    # Validate the corrected JSON
    try:
        json.loads(json_text)  # Test if it's valid JSON
    except json.JSONDecodeError as e:
        print(f"Corrected JSON so far: {json_text}")  # For debugging
        raise ValueError(f"JSON correction failed: {e}")

    return json_text


# Example input JSON-like string with issues
kpi_response = {"text":"```\n{\n  \"sql_query\": \"SELECT (CAST(SUM(CASE WHEN VehicleType = \\'EV\\' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*)) * 100 AS EVJobsPercentage FROM ServiceJobs WHERE ServiceDate >= DATEADD(MONTH, -3, GETDATE())\",\n  \"function_prototype\": \"generate_plotly_chart_js(df, x_column, y_column, title)\",\n  \"function_prototype_json\": {\n    \"x_column\": null,\n    \"y_column\": \"EVJobsPercentage\",\n    \"title\": \"Percentage of Service Jobs for EVs in the Last 3 Months\"\n  }\n}\n```"
}

# Correct and parse JSON
try:
    corrected_json_text = correct_json(kpi_response["text"])
    parsed_response = json.loads(corrected_json_text)
    print("Parsed JSON:", parsed_response)
except ValueError as e:
    print("Error:", e)



