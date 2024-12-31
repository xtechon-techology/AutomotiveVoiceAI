import json


def kpi_generator_prompt(days, kpi_count, user_query, schema_context, limit):
    instructions = f"""
    #In addition to generating SQL queries for user question, suggest up to {kpi_count} Key Performance Indicators (KPIs) with trends and relationships in the table contextually based on users questions.
    #Filter data for the last {days} days on the partition date column which is in this timestamp yyyy-MM-ddTHH:mm:ss.SSSZ format.
    #If multiple tables are in the schema then generate atleast 1 KPI using JOINS.
    #Check if GROUP BY clause can be used based on user question.
    #NEVER WRAP column names in double quotes (") for HANA queries.
    #You must perform a case-insensitive comparison in generated HANA SQL query.
    """
    if str(user_query).__contains__("filter:ignore"):
        instructions = f"""
        #In addition to generating SQL queries for user question, suggest up to {kpi_count} Key Performance Indicators (KPIs) with trends and relationships in the table contextually based on users questions.
        #Check if GROUP BY clause can be used based on user question.
        #If multiple tables are in the schema then generate atleast 1 KPI using JOINS.
        #NEVER WRAP column names in double quotes (") for HANA queries.
        #You must perform a case-insensitive comparison in generated HANA SQL query.
        """

    prompt = f"""Never query for all columns from a table. You must query only the columns that are needed to answer the question. Pay attention to use only the column names you can see in the tables below.
    `ORDER BY` clause should always be after `WHERE` clause. DO NOT add semicolon to the end of SQL. Pay attention to the column comments(text after --) in table schema.

    ALWAYS use the following table schema and columns given below and DO NOT query for columns apart from the one given below:
    {schema_context}

    Instructions:
    {instructions}

    Important Note: If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Based on the following pieces of information and instructions given above answer the below question.
    """

    return prompt


def kpi_generator_validation_prompt(
    kpi_json,
    table_name,
    table_partitioned_columns,
    table_non_partitioned_columns,
    user_query,
):

    prompt = f"""You are a sql semantic layer that validates and modifies the sql query associate with a KPI and 
    user query based on the table metadata provided to you. You have to maintain only 2 columns in the output of the 
    sql query. Also fix any issues in sql syntactically with adherence to spark sql. Sample example just for 
    reference: [\n  {{\n \"kpi_name\": \"Total Revenue\",\n    \"query\": \"SELECT SUM(Sales) FROM Transactions WHERE 
    Date > '2022-01-01'\", \n    \"visualisation_chart_name\": \"Bar Chart\"\n  }}] \n, output: [\n  {{\n    
    \"kpi_name\": \"Total Revenue\",\n    \"query\": \"SELECT SUM(revenue),date FROM Transactions WHERE Date > 
    '2022-01-01' group by date\", \n\"visualisation_chart_name\": \"Bar Chart\"\n }} \n\n Input JSON: {kpi_json} You 
    have access to a table named \"{table_name}\" with non-partitioned columns as \n\"{table_partitioned_columns}\", 
    The partitioned columns are \n\"{table_non_partitioned_columns}\"\nUser Query: {user_query}. Please re-analyse 
    and return the relevant queries only where applicable based on the above inputs. Return the same number of KPIs 
    as present in input. DO STRICTLY RETURN THE RESPONSE IN THE SAME JSON FORMAT AS OF THE INPUT JSON. Return only 
    the modified KPI json in the response. The format is a json array containing objects each having 3 keys: 
    kpi_name, query and visualisation_chart. \n\n Note: the sample example is just for reference, don't use it for 
    modifying the actual input queries """

    final_prompt = {"message": json.dumps(prompt)}
    return final_prompt


def query_generator_prompt(schema_context, days):
    instructions = f"""
    #Check if GROUP BY clause can be used based on user question.
    #Filter data for the last {days} days on the partition date column(check column comments for format of value). ALWAYS Pay attention to which column is in which table.
    #If no date column is present then do not apply date filter.
    #If multiple tables are in the schema then check if user question contextually requires JOINS in the query.
    #When multiple table schema are given, Pay attention to which column is in which table. 
    #SQL query generated should ALWAYS have case-insensitive value comparisons.
    """

    prompt = f"""Never query for all columns from a table. You must query only the columns that are needed to answer the question. Pay attention to use only the column names you can see in the tables below.
    `ORDER BY` clause should always be after `WHERE` clause. DO NOT add semicolon to the end of SQL. Pay attention to the column comments(text after --) in table schema. ALWAYS pay attention to which column is in which table.
    Pay attention that the query uses columns which is part of that create table schema ONLY and NOT of different table schema present in the schema.

    ALWAYS use the following table schema and columns given below and DO NOT query for columns apart from the one given below:
    \n{schema_context}

    Instructions:
    {instructions}

    Important Note: If you don't know the answer, just return empty string, don't try to make up an answer.

    Based on the following pieces of information and instructions given above answer the below question.
    """

    return prompt
