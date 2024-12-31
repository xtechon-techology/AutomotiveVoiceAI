import json
import re
import logging

logger = logging.getLogger(__name__)


def fetch_filter_days(input_string):
    # Using regular expression to find 'filter: n' or 'filter: n days' in the input string
    match = re.search(r"filter:\s*(\d+)\s*(?:days)?", input_string, re.IGNORECASE)

    if match:
        # Extracting the value of 'n' from the matched group
        n_value = int(match.group(1))
        return n_value
    elif (
        "filter:ignore" in input_string.lower()
        or "filter: ignore" in input_string.lower()
    ):
        # Return 0 if the input string contains 'filter:ignore'
        return 0
    else:
        # Return None if no match is found
        return 7


# def create_fetch_kpi_prompt(tables, catalogue, partition_catalogue, user_prompt):
#     prompt = "You have access to a table named \n"
#     days = fetch_filter_days(user_prompt)
#     kpi_count = 4
#     for i in range(len(tables)):
#         prompt += "\"" + tables[i] + "\" with non-partitioned columns like \""
#         prompt += str(catalogue.get(tables[i]))
#         prompt += ", The partitioned columns are \""
#         prompt += str(partition_catalogue.get(tables[i]))
#
#     logger.info(f"####user_prompt::{user_prompt}####")
#     kpi_count = filter_kpi(kpi_count, user_prompt)
#
#     prompt += get_filtered_prompt(days, kpi_count, user_prompt, tables[0])
#     final_prompt = {"message": json.dumps(prompt)}
#     logger.debug("####prompt:kpi_name, query & chart_type####")
#     logger.debug(f"\t{prompt}")
#     logger.debug("###############################################")
#     return final_prompt


def filter_kpi(kpi_count, user_prompt):
    if str(user_prompt).__contains__("kpi_count:"):
        kpi_count_result = extract_kpi(user_prompt)
        if kpi_count_result is not None:
            logger.info(f"===overridden fields by user:: {kpi_count_result}")
            kpi_count = kpi_count_result
    return kpi_count


def extract_kpi_summary_from_describe_prompt(kpi, data):
    prompt = (
        "KPI:"
        + kpi
        + "\n"
        + str(data)
        + "\n"
        + "Based on data please share insights as detailed summary in pointers upto 120 words by "
        "extrapolating the above data. "
    )
    final_prompt = {"message": json.dumps(prompt)}
    logger.debug(f"####prompt for fetching KPI:{kpi} summary:{final_prompt} ####")
    return final_prompt


def extract_dynamic_chart_call(
    kpi, column_names, function_signature, visualisation_chart_name
):
    prompt = (
        "KPI:"
        + kpi
        + "\n Column_names: "
        + str(column_names)
        + "\n chart function signature:"
        + function_signature
        + "\nBased on the given contexts please "
        "provide us the valid function call "
        f"that helps us generate a {visualisation_chart_name} for "
        "the given KPI and suitable axis "
        "labels. Please return only the "
        "function prototype. DON'T ADD any "
        "extra EXPLANATION or NOTES or "
        "INTRODUCTORY TEXT or ANY OTHER HUMAN "
        "BEHAVIOURAL TEXT "
    )
    final_prompt = {"message": json.dumps(prompt)}
    logger.debug(
        f"####prompt for fetching KPI:{kpi} chart type & label:{final_prompt}####"
    )
    return final_prompt


def extract_kpi(input_string):
    pattern = r"kpi_count:(\d+)"
    match = re.search(pattern, input_string)

    if match:
        kpi_value = int(match.group(1))
        return kpi_value
    else:
        return None

    # def modify_queries(input_data):
    #     # Regular expression pattern to match and remove WHERE clauses
    #     where_clause_pattern = re.compile(r'WHERE\s.*?(\bGROUP\sBY|$)')
    #
    #     # Modify each query in the input data
    #     modified_queries = []
    #     for item in input_data:
    #         # Remove WHERE clause from the query
    #         modified_query = where_clause_pattern.sub(r'\1', item["query"])
    #
    #         # Replace the "query" tag in the item
    #         item["query"] = modified_query
    #
    #         # Append the modified item to the list
    #         modified_queries.append(item)
    #
    #     return modified_queries

    # def extract_tables_prompt(input_msg, table_descriptions):
    #     logger.info(f"{input_msg}")
    #     prompt = f""" Please analyze the semantic descriptions of tables and rank them based on their relevance or
    #     similarity to a user context. user context: '{input_msg}'
    #     table descriptions: '{table_descriptions}'
    #
    #     Please provide the response in JSON format which should include the top 1 table based on rank: {{"tables": [
    #     "<table name>", "<table name>", ...]}} Make sure the output response should contain 1(SINGLE) table name The
    #     output should consist solely of JSON data. Please verify for any errors and deliver only the JSON output. """
    #     final_prompt = {"message": json.dumps(prompt)}
    #     return final_prompt

    # def extract_kpi_summary_prompt(kpi, data, chart_name):
    #     prompt = "KPI:" + kpi + "\n" + str(
    #         data) + "\n" + "Based on the available data, please provide a concise one-line summary of up to 40 words and " \
    #                        "a detailed summary of up to 100 words. Additionally, provide JavaScript code to create a Line " \
    #                        "Chart using the Plotly 2.20.0 library, with the DOM node ID set as 'chartId.' The code should " \
    #                        "be in an escaped format to allow evaluation using eval(). Include the following layout " \
    #                        "JSON:\n\"{\n  paper_bgcolor: 'rgba(0,0,0,0)',\n  plot_bgcolor: 'rgba(0,0,0,0)',\n  width: " \
    #                        "350,\n  height: 300,\n  margin: {\n    l: 30,\n    r: 1,\n    t: 2,\n    b: 40\n  }\"\n} " \
    #                        "\nPresent the entire response in JSON format with two keys: 'labelText' and 'content.' In " \
    #                        "'labelText,' use the value 'KPI_name.' In 'content,' provide an object containing three " \
    #                        "sub-objects, each labeled 'Summary,' 'Query,' and 'Visualization,' respectively.\nReference " \
    #                        "the following sample response:\n\"{\n  \"labelText\": \"unique_users\",\n  \"content\": [\n   " \
    #                        " {\n      \"tab_name\": \"Summary\",\n      \"tab_content\": {\n        \"tag\": \"text\"," \
    #                        "\n        \"response\": \"Based on the data, there were a total of 30 unique users.\"\n      " \
    #                        "}\n    },\n    {\n      \"tab_name\": \"Query\",\n      \"tab_content\": {\n        \"tag\": " \
    #                        "\"code\",\n        \"response\": \"SELECT COUNT(DISTINCT user_guid) as unique_users FROM " \
    #                        "launch_events LIMIT 100\"\n      }\n    },\n    {\n      \"tab_name\": \"Visualization\"," \
    #                        "\n      \"tab_content\": {\n        \"tag\": \"script\",\n        \"response\": \"var data = " \
    #                        "[\\n{\\nvalues: [30],\\nlabels: ['Unique Users'],\\ntype: 'pie'\\n}\\n];\\n\\nvar layout = {" \
    #                        "\\npaper_bgcolor: 'rgba(0,0,0,0)',\\nplot_bgcolor: 'rgba(0,0,0,0)',\\nwidth: 350,\\nheight: " \
    #                        "300,\\nmargin: {\\nl: 30,\\nr: 1,\\nt: 2,\\nb: 40\\n}\\n};\\n\\nPlotly.newPlot('chartId', " \
    #                        "data, layout);\",\n        \"labelText\": \"unique_users\"\n      }\n    }\n  ]\n}\"\nEnsure " \
    #                        "strict adherence to these instructions, including no introductory text, no additional " \
    #                        "comments, no post notes, and no response explanations in the output. The output should " \
    #                        "consist solely of JSON data. Please verify for any errors and deliver only the JSON output. "
    #     final_prompt = {"message": json.dumps(prompt)}
    #     logger.debug(f"####prompt for fetching KPI:{kpi} summary sending with data####{final_prompt}")
    #     return final_prompt

    # Example usage:
    # input_data = [
    #     {'kpi_name': 'Count of Nodes by Node Type', 'query': 'SELECT node_type, COUNT(*) as count FROM acpm_warehouse.storage_flat_table WHERE node_type IS NOT NULL GROUP BY node_type', 'visualisation_chart_name': 'Bar Chart'},
    #     {'kpi_name': 'Storage Consumption by Node Type', 'query': 'SELECT node_type, SUM(asset_head_storage) as storage_consumption FROM acpm_warehouse.storage_flat_table WHERE node_type IS NOT NULL GROUP BY node_type', 'visualisation_chart_name': 'Bar Chart'},
    #     {'kpi_name': 'Number of Renditions by Node Type', 'query': 'SELECT node_type, COUNT(DISTINCT components_head_renditions_count) as num_renditions FROM acpm_warehouse.storage_flat_table WHERE node_type IS NOT NULL GROUP BY node_type', 'visualisation_chart_name': 'Bar Chart'},
    #     {'kpi_name': 'Storage Consumption of Renditions by Node Type', 'query': 'SELECT node_type, SUM(components_head_renditions_storage) as storage_consumption FROM acpm_warehouse.storage_flat_table WHERE node_type IS NOT NULL GROUP BY node_type', 'visualisation_chart_name': 'Bar Chart'}
    # ]
    #
    # modified_output = modify_queries(input_data)
    # print(modified_output)


def generate_schema(catalogue: dict):
    tables = catalogue.keys()
    tables_schema_context = ""
    for key in tables:
        table_details = catalogue[key]
        cache_catalogue_data = table_details["cache_catalogue_data"]
        cache_extn_catalogue_data = table_details["cache_extn_catalogue_data"]
        non_part_columns = generate_column_schema(
            cache_catalogue_data["non_part_columns"], False
        )
        part_columns = generate_column_schema(
            cache_catalogue_data["part_columns"], True
        )
        tables_schema_context += (
            f"CREATE TABLE {key} (\n" + non_part_columns + part_columns + ")\n"
        )
        if len(tables) > 1:
            tables_schema_context += "\n"
    return tables_schema_context


def generate_column_schema(columns: list, is_part_column):
    column_schema = ""
    for column in columns:
        description = (
            " -- "
            + column["column_description"]
            + ("(partitioned column)" if is_part_column else "")
            + "\n"
        )
        column_schema = (
            column_schema
            + column["column_name"]
            + " "
            + column["data_type"]
            + ","
            + (
                description
                if (
                    column["column_description"]
                    and column["column_description"].strip()
                )
                else "\n"
            )
        )

    return column_schema
