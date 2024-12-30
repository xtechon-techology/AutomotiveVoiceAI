import logging

log_level = logging.DEBUG

common_conf = {"api_host_address": "127.0.0.1", "api_host_port": 8005}
sql_server_conf = {
    "host": "voicepocsqlserver.database.windows.net",
    "port": 1433,
    "user": "voicepoc",
    "password": "Officenoida@24dec"
}
azure_congnitive_services_conf = {
    "speech_service_key": "COhUF6rW70pSarwYKQr12oorTPpWNzOkWAsPUW4yPIyosYM96QlEJQQJ99ALACYeBjFXJ3w3AAAYACOGLUN5",
    "speech_service_region": "eastus",
    "speech_service_endpoint": "https://eastus.api.cognitive.microsoft.com/"
}

