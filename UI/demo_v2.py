import json

import streamlit as st
from connectors.sqlserver_database_connector import SQLServerDatabaseConnector
from model.llm_kpi import get_llm_kpi_response
from model.llm_openai import get_llm_response
from utils.common_util import correct_json
from visualiser.chart_handlers import generate_plotly_figure_js
from dotenv import load_dotenv

from voiceai.speech_converter_v2 import recognize_speech_continuously_streamlit

# Page setup
st.set_page_config(
    page_title="Automotive Voice AI",
    layout="wide",
)

# Centered title and description
st.markdown(
    """
    <div style="text-align: center;">
        <h1>💬 Automotive Voice AI</h1>
        <p>Revolutionizing <b>Data Insights</b> through Voice Commands</p>
    </div>
    """,
    unsafe_allow_html=True,
)

load_dotenv()
# Enhanced Streamlit App Interface
st.title("Voice-Driven Business Intelligence Platform")
st.subheader("Revolutionizing Data Insights through Voice Commands")
st.markdown("**Turn your voice into actionable insights.**")

# Progress Bar
steps = ["Voice Translation", "Query Generation", "Query Validation", "Query Execution", "Chart Generation"]
st_progress = st.progress(0)



if st.button("Start Listening"):
    col1, col2 = st.columns(2)
    with col1:
        result = recognize_speech_continuously_streamlit()
        st.subheader("1- Voice Translation")
        st.write("Speak into your microphone. Say 'stop listening' to end.")
        st.write(f"Final Recognized Text: {result}")
        # Update progress using st_progress
        st_progress.progress(20)


    response = get_llm_response(result)

    sql_connector = SQLServerDatabaseConnector()

    # Print the response's each KPI, query, visualization chart name, and referenced columns
    print(f"Question: {response['question']}")
    print(f"Format Instructions: {response['format_instructions']}")
    for text in response["text"]:
        print(f"KPI Name: {text['kpi_name']}")
        print(f"Query: {text['query']}")
        with col2:
            st.subheader("2- Query Generation")
            st.write(f"Query: {text['query']}")
            st_progress.progress(40)  # Update progress

        col3, col4 = st.columns(2)
        print(f"Visualization Chart Name: {text['visualization_chart_name']}")
        print(f"Referenced Source Columns: {text['referenced_source_columns']}")
        query = text['query']
        with col3:
            summary, column_names, results, df = sql_connector.execute_query_with_summary(query)
            st.subheader("3- Query Execution & Validation")
            st.dataframe(df)
            st_progress.progress(60)  # Update progress
        print(f"Summary: {summary}")
        print(f"Column Names: {column_names}")
        print(f"Results: {results}")
        print(f"Dataframe: {df}")

        print(f"---------------------------------------------------------")

        kpi_response = get_llm_kpi_response(text['kpi_name'], df, column_names, text['query'],"generate_plotly_chart_js(df, x_column=, y_column=, title=)", text['visualization_chart_name'])
        print(f"KPI Response cli: {kpi_response}")
        # replace \ & \\ with empty string
        kpi_response["text"] = kpi_response["text"].replace("\\", "")

        # Parse the kpi_response
        try:
            kpi_response = json.loads(kpi_response["text"])
        except:
            clear_json = correct_json(kpi_response["text"])
            kpi_response = json.loads(clear_json)



        st_progress.progress(80)  # Update progress
        # Print sql_query
        print(kpi_response["sql_query"])

        # Print function_prototype
        print(kpi_response["function_prototype"])

        # Print function_prototype_json
        function_prototype_json = kpi_response["function_prototype_json"]
        print(kpi_response["function_prototype_json"])
        print(f"x_column: {function_prototype_json['x_column']}")
        print(f"y_column: {function_prototype_json['y_column']}")
        print(f"title: {function_prototype_json['title']}")
        # Display the chart details x_column, y_column, title, and visualization chart name
        st.write(f"x_column: {function_prototype_json['x_column']}, y_column: {function_prototype_json['y_column']}, title: {function_prototype_json['title']}, visualization_chart_name: {text['visualization_chart_name']}")
        print(f"---------------------------------------------------------")
        chart_result, chart_image_path = generate_plotly_figure_js(df, function_prototype_json['x_column'], function_prototype_json['y_column'],
                                                                   function_prototype_json['title'],
                                                                   text['visualization_chart_name'])

        # Display the chart image
        with col4:
            st.subheader("4- Chart Generation")
            st.image(chart_image_path)
            st_progress.progress(100)
        print(f"Chart Result: {chart_result}")

        # st.write(kpi_response)
    # st.write("\n**Final Recognized Text:**")
    # st.write(result)

