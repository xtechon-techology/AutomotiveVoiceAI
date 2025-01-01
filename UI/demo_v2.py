import json

import streamlit as st
import azure.cognitiveservices.speech as speechsdk
from configs.config import azure_congnitive_services_config
from connectors.sqlserver_database_connector import SQLServerDatabaseConnector
from model.llm_kpi import get_llm_kpi_response
from model.llm_openai import get_llm_response
from visualiser.chart_handlers import generate_plotly_figure_js
from dotenv import load_dotenv

from voiceai.speech_converter_v2 import recognize_speech_continuously_streamlit

load_dotenv()

# def recognize_speech_continuously_streamlit():
#     """
#     Continuously listens to the microphone and returns recognized speech as text.
#     """
#     # Configure speech settings
#     speech_config = speechsdk.SpeechConfig(
#         subscription=azure_congnitive_services_config["speech_service_key"],
#         region=azure_congnitive_services_config["speech_service_region"],
#     )
#     speech_config.speech_recognition_language = "en-US"
#
#     audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
#     speech_recognizer = speechsdk.SpeechRecognizer(
#         speech_config=speech_config, audio_config=audio_config
#     )
#
#     recognized_text = []
#     is_listening = True
#
#     def handle_recognized(evt):
#         nonlocal is_listening
#         st.write(f"Recognized: {evt.result.text}")
#         recognized_text.append(evt.result.text)
#
#         # Stop listening if a specific phrase is recognized
#         if "stop listening" in evt.result.text.lower():
#             st.write("Stop command recognized. Ending recognition.")
#             is_listening = False
#             speech_recognizer.stop_continuous_recognition()
#
#     def handle_canceled(evt):
#         st.write(
#             f"Speech recognition canceled: {evt.result.cancellation_details.reason}"
#         )
#         if evt.result.cancellation_details.error_details:
#             st.write(f"Error details: {evt.result.cancellation_details.error_details}")
#         nonlocal is_listening
#         is_listening = False
#
#     # Connect event handlers
#     speech_recognizer.recognized.connect(handle_recognized)
#     speech_recognizer.canceled.connect(handle_canceled)
#
#     # Start continuous recognition
#     speech_recognizer.start_continuous_recognition()
#
#     try:
#         while is_listening:
#             pass  # Keeps the script running until recognition stops
#     except KeyboardInterrupt:
#         st.write("\nManual interruption received, stopping recognition.")
#         speech_recognizer.stop_continuous_recognition()
#
#     return " ".join(recognized_text)


# Streamlit App Interface
st.title("Azure Speech-to-Text Streamlit App")

if st.button("Start Listening"):
    st.write("Speak into your microphone. Say 'stop listening' to end.")
    result = recognize_speech_continuously_streamlit()
    st.write(f"Final Recognized Text: {result}")
    response = get_llm_response(result)

    sql_connector = SQLServerDatabaseConnector()

    # Print the response's each KPI, query, visualization chart name, and referenced columns
    print(f"Question: {response['question']}")
    print(f"Format Instructions: {response['format_instructions']}")
    for text in response["text"]:
        print(f"KPI Name: {text['kpi_name']}")
        print(f"Query: {text['query']}")
        st.write(f"Query: {text['query']}")
        print(f"Visualization Chart Name: {text['visualization_chart_name']}")
        print(f"Referenced Source Columns: {text['referenced_source_columns']}")
        query = text['query']
        summary, column_names, results, df = sql_connector.execute_query_with_summary(query)
        st.dataframe(df)
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
        kpi_response = json.loads(kpi_response["text"])

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
        st.image(chart_image_path)
        print(f"Chart Result: {chart_result}")

        st.write(kpi_response)
    # st.write("\n**Final Recognized Text:**")
    # st.write(result)

