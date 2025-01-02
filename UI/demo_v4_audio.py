import json
import streamlit as st
from connectors.sqlserver_database_connector import SQLServerDatabaseConnector
from model.llm_kpi import get_llm_kpi_response
from model.llm_openai import get_llm_response
from model.llm_openai_reprocessed import get_llm_response_reprocessed
from utils.common_util import correct_json
from utils.storage_util import save_streamlit_audio_to_local_file, upload_to_azure, get_downloaded_blob_file
from visualiser.chart_handlers import generate_plotly_figure_js
from dotenv import load_dotenv

from voiceai.speech_converted_by_audio_file import get_audio_translation_from_file
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

# st.subheader("Voice / Query Interface")
# text_mode = st.toggle("Text Query Mode", False)

col_voice, col_text = st.columns(2)


# Progress Bar
steps = ["Voice Translation", "Query Generation", "Query Validation", "Query Execution", "Chart Generation"]
st_progress = st.progress(0)

# Voice Mode
with col_voice:
    st.subheader("Voice Mode")
    st.write("Speak into your microphone. Say 'stop listening' to end.")
    # voice_button = st.button("Start Listening")
    audio_value = st.audio_input("Record a voice message")
    blob_url = None
    file_path = None
    if audio_value:
        st.audio(audio_value)
with col_text:
    st.subheader("Query Mode")
    text_input = st.text_area("Enter your query here")
    query_submit = st.button("Submit Query")

if audio_value or (query_submit and text_input):
    col1, col2 = st.columns(2)
    with col1:
        if (query_submit and text_input):
            result = text_input
            st.subheader("1- Text Query")
        elif audio_value:
            st.audio(audio_value)
            # result = recognize_speech_continuously_streamlit()
            file_path = save_streamlit_audio_to_local_file(audio_value)
            st.write("File saved at:", file_path)
            cloud_file_path = upload_to_azure(file_path)
            st.write("File successfully uploaded and accessible at:", cloud_file_path)
            downloaded_file_name = get_downloaded_blob_file(file_path)
            st.write("File downloaded successfully:", downloaded_file_name)
            result = get_audio_translation_from_file(downloaded_file_name)
            st.subheader("1- Voice Translation")


        st.write(f"Final Recognized Text: {result}")
        st_progress.progress(20)

    response = get_llm_response(result)
    sql_connector = SQLServerDatabaseConnector()

    is_query_iteration = True
    while is_query_iteration:
        print(f"Question: {response['question']}")
        print(f"Format Instructions: {response['format_instructions']}")
        for text in response["text"]:
            print(f"KPI Name: {text['kpi_name']}")
            print(f"Query: {text['query']}")
            with col2:
                st.subheader("2- Query Generation")
                st.write(f"Query: {text['query']}")
                st_progress.progress(40)

            col3, col4 = st.columns(2)
            query = text['query']
            success = False
            attempts = 0

            summary, column_names, results, df = None, None, None, None
            while not success and attempts < 3:
                try:
                    summary, column_names, results, df = sql_connector.execute_query_with_summary(query)
                    with col3:
                        st.subheader("3- Query Execution & Validation")
                        st.dataframe(df)
                        success = True
                        st_progress.progress(60)
                    print(f"Summary: {summary}")
                    print(f"Column Names: {column_names}")
                    print(f"Results: {results}")
                    print(f"Dataframe: {df}")
                except Exception as e:
                    str_error = str(e)
                    st.error(f"Attempt {attempts + 1}: Failed to process the query. Error: {str_error}")
                    response = get_llm_response_reprocessed(result, query, str_error)
                    query = response['text'][0]['query']  # Update query for the next attempt
                    attempts += 1

            if not success:
                st.error("Query execution failed after 3 attempts.")
                is_query_iteration = False
                break

            kpi_response = get_llm_kpi_response(
                text['kpi_name'], df, column_names, text['query'],
                "generate_plotly_chart_js(df, x_column=, y_column=, title=)",
                text['visualization_chart_name']
            )
            print(f"KPI Response CLI: {kpi_response}")

            # Replace \ & \\ with an empty string
            kpi_response["text"] = kpi_response["text"].replace("\\", "")

            # Parse the kpi_response
            try:
                kpi_response = json.loads(kpi_response["text"])
            except:
                clear_json = correct_json(kpi_response["text"])
                kpi_response = json.loads(clear_json)

            st_progress.progress(80)
            function_prototype_json = kpi_response["function_prototype_json"]

            # Display chart details and generate the chart
            chart_result, chart_image_path = generate_plotly_figure_js(
                df,
                function_prototype_json['x_column'],
                function_prototype_json['y_column'],
                function_prototype_json['title'],
                text['visualization_chart_name']
            )

            with col4:
                st.subheader("4- Chart Generation")
                st.image(chart_image_path)
                st_progress.progress(100)

            print(f"Chart Result: {chart_result}")

        is_query_iteration = False
