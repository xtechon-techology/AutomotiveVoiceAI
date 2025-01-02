import logging

log_level = logging.DEBUG

common_conf = {"api_host_address": "127.0.0.1", "api_host_port": 8005}
sql_server_conf = {
    "host": "voicepocsqlserver.database.windows.net",
    "port": 1433,
    "user": "voicepoc",
    "password": "Officenoida@24dec",
}
azure_congnitive_services_conf = {
    "speech_service_key": "COhUF6rW70pSarwYKQr12oorTPpWNzOkWAsPUW4yPIyosYM96QlEJQQJ99ALACYeBjFXJ3w3AAAYACOGLUN5",
    "speech_service_region": "eastus",
    "speech_service_endpoint": "https://eastus.api.cognitive.microsoft.com/",
    "blob_service_connection_string": "DefaultEndpointsProtocol=https;AccountName=automotivestorage;AccountKey=OIKjIkzgC/c+sPLrUappeuJO8/felfUV2YTuiiX1s0nlTUH9IuhEjnhnlbw9DyJmU+KNjzsLxlWD+AStLINdqA==;EndpointSuffix=core.windows.net",
    "blob_container_name": "audiocontainer"
}
openai_conf = {
    "openai_api_key": "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"
}



# working but quota finished
# "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"
