import json

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain

from response.sql_query_response import KPIResponse


def get_llm_kpi_response(kpi, df, column_names, query, function_signature, visualisation_chart_name):
    # Create prompt template for the KPI suggestions
    prompt_text = extract_dynamic_chart_call(kpi, df, column_names, function_signature, visualisation_chart_name)
    print(f"KPI prompt - {prompt_text}")

    # Create PromptTemplate object with the KPI prompt template
    prompt_template = PromptTemplate(
        input_variables=["sql_query", "format_instructions"],  # Add input variables if needed
        template=prompt_text
    )

    # Create LLM object with ChatOpenAI model
    llm = ChatOpenAI(temperature=0.5, model="gpt-4")

    # Create a chain of PromptTemplate and LLM objects with the user input
    runnable = LLMChain(llm=llm, prompt=prompt_template)

    parser = JsonOutputParser(pydantic_object=KPIResponse)
    format_instructions = parser.get_format_instructions()

    # Invoke the LLM chain
    response = runnable.invoke({
            "sql_query": query,
            "format_instructions": format_instructions
        })  # Use .run() or .invoke() depending on the version
    print(f"KPI llm response - {response}")

    return response

def extract_dynamic_chart_call(kpi, data, column_names, function_signature, visualisation_chart_name):
    prompt = (
        f"KPI: {kpi}\n"
        f"Data: {data}\n"
        f"Column_names: {column_names}\n"
        +"Query: {sql_query}\n"
        f"Chart function signature: {function_signature}\n"
        f"Based on the given context, please provide a valid function call "
        f"that helps generate a {visualisation_chart_name} for the given KPI and suitable axis labels. "
        "Format your output as JSON:\n{format_instructions}. Make sure x_column, y_column should be existing columns in column_names."
    )
    return prompt

def extract_dynamic_chart_call_v1(kpi, data, column_names, function_signature, visualisation_chart_name):
    prompt = (
        f"KPI: {kpi}\n"
        f"Data: {data}\n"
        f"Column_names: {column_names}\n"
        +"Query: {sql_query}\n"
        f"Chart function signature: {function_signature}\n"
        f"Based on the given context, please provide a valid function call "
        f"that helps generate a {visualisation_chart_name} for the given KPI and suitable axis labels. "
        "Return only two things first the function prototype and second function prototype as json for example json key & value - 'x_column':'Month', 'y_column':'TotalRevenue', 'title':'Total Revenue Last Three Months'. DO NOT add any extra explanation or notes"
    )
    return prompt

def get_llm_kpi_response_v0(kpi, df, column_names, query, function_signature, visualisation_chart_name):

    # Create prompt template for the KPI suggestions
    prompt = extract_dynamic_chart_call_v0(kpi, df,  column_names, query, function_signature, visualisation_chart_name)
    print(f"KPI prompt - {prompt}")
    # Create PromptTemplate object with the KPI prompt template
    prompt_template = PromptTemplate(template=prompt)
    # Create LLM object with ChatOpenAI model
    llm = ChatOpenAI(temperature=0.5, model="gpt-4o")
    # Create a chain of PromptTemplate and LLM objects with the user input
    runnable = LLMChain(llm=llm, prompt=prompt_template)
    # user_question = (
    #     "How many vehicles were serviced each month over the last three months?"
    # )
    # parser = JsonOutputParser(pydantic_object=SQLQueryResponse)
    # format_instructions = parser.get_format_instructions()
    # runnable = prompt | llm | parser
    response = runnable.invoke()
    return response

def extract_dynamic_chart_call_v0(
    kpi, data, column_names, query, function_signature, visualisation_chart_name
):
    prompt = (
        "KPI:"
        + kpi
        +"\nData:"
        + str(data)
        + "\n Column_names: "
        + str(column_names)
        + "\n Query:"
        + query
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
    print(f"prompt extract_dynamic_chart_call:: {prompt}")
    print(f"prompt extract_dynamic_chart_call :: json.dumps(prompt) {json.dumps(prompt)}")
    final_prompt = {"message": json.dumps(prompt)}
    print(f"####prompt for fetching KPI:{kpi} chart type & label:{final_prompt}####")
    return final_prompt


def extract_kpi_summary_prompt(kpi, data, chart_name):
        prompt = "KPI:" + kpi + "\n" + str(
            data) + "\n" + "Based on the available data, please provide a concise one-line summary of up to 40 words and " \
                           "a detailed summary of up to 100 words. Additionally, provide JavaScript code to create a " \
                           +chart_name +" using the Plotly 2.20.0 library, with the DOM node ID set as 'chartId.' The code should " \
                           "be in an escaped format to allow evaluation using eval(). Include the following layout " \
                           "JSON:\n\"{\n  paper_bgcolor: 'rgba(0,0,0,0)',\n  plot_bgcolor: 'rgba(0,0,0,0)',\n  width: " \
                           "350,\n  height: 300,\n  margin: {\n    l: 30,\n    r: 1,\n    t: 2,\n    b: 40\n  }\"\n} " \
                           "\nPresent the entire response in JSON format with two keys: 'labelText' and 'content.' In " \
                           "'labelText,' use the value 'KPI_name.' In 'content,' provide an object containing three " \
                           "sub-objects, each labeled 'Summary,' 'Query,' and 'Visualization,' respectively.\nReference " \
                           "the following sample response:\n\"{\n  \"labelText\": \"unique_users\",\n  \"content\": [\n   " \
                           " {\n      \"tab_name\": \"Summary\",\n      \"tab_content\": {\n        \"tag\": \"text\"," \
                           "\n        \"response\": \"Based on the data, there were a total of 30 unique users.\"\n      " \
                           "}\n    },\n    {\n      \"tab_name\": \"Query\",\n      \"tab_content\": {\n        \"tag\": " \
                           "\"code\",\n        \"response\": \"SELECT COUNT(DISTINCT user_guid) as unique_users FROM " \
                           "launch_events LIMIT 100\"\n      }\n    },\n    {\n      \"tab_name\": \"Visualization\"," \
                           "\n      \"tab_content\": {\n        \"tag\": \"script\",\n        \"response\": \"var data = " \
                           "[\\n{\\nvalues: [30],\\nlabels: ['Unique Users'],\\ntype: 'pie'\\n}\\n];\\n\\nvar layout = {" \
                           "\\npaper_bgcolor: 'rgba(0,0,0,0)',\\nplot_bgcolor: 'rgba(0,0,0,0)',\\nwidth: 350,\\nheight: " \
                           "300,\\nmargin: {\\nl: 30,\\nr: 1,\\nt: 2,\\nb: 40\\n}\\n};\\n\\nPlotly.newPlot('chartId', " \
                           "data, layout);\",\n        \"labelText\": \"unique_users\"\n      }\n    }\n  ]\n}\"\nEnsure " \
                           "strict adherence to these instructions, including no introductory text, no additional " \
                           "comments, no post notes, and no response explanations in the output. The output should " \
                           "consist solely of JSON data. Please verify for any errors and deliver only the JSON output. "
        final_prompt = {"message": json.dumps(prompt)}
        print(f"####prompt for fetching KPI:{kpi} summary sending with data####{final_prompt}")
        return final_prompt