MSG_ADX_AUTHENTICATION_FAILED = "ADX Authentication failed. Please re-login."
MSG_ADX_SERVICE_AUTHENTICATION_FAILED = "ADX Service Authentication failed. Please reach out to Copilot Insight team at copilot-insight-engineering@adobe.com"
MSG_PROFILE_ERROR = "You don't have a connection profile created on Copilot, please create one using ADX to start generating insights"
MSG_GENERIC_ERROR = "Some issue has occurred, please retry after sometime or reach out to Copilot Insight team at " \
                       "copilot-insight-engineering@adobe.com"
MSG_NO_LRU_CON = "No available LRU connection in insight-gen"
MSG_QUERY_FAILURE = "Some Error has occured while running query on databricks, please validate generated query in query Section."
MSG_CUSTOM = "please check query shown & change your query accordingly"
MSG_NO_ONBOARDING = "Look like given table(s) is(are) not onboarded, please onboard your asset in copilot-insight!"
MSG_NO_VALID_KPI = "NO valid KPI generated, please change your query accordingly"
MSG_SLACK_CHAR_LIMIT_ERR = "Due to character limit in slack, Query result in tabular form is only visible in ADX Copilot-Insights UI."
MSG_NO_DATA_FOUND = "Query could not generate any result"
# MSG_NO_TEAM_SOURCE_ROOM_ONBOARDED = "Hi Team, it appears that no table has been onboarded in the '{room}' room under the '{type}' source type for the '{team_name}' team. Please reach out to Copilot Insight team at copilot-insight-engineering@adobe.com"
MSG_NO_TEAM_SOURCE_ROOM_ONBOARDED = """Hi Team, no onboarding has been found for the following details:
Room Name: {room}
Team Name: {team_name}
Source Type: {type}
Kindly onboard your assets using the Insight Gen Onboarding form."""
MSG_TABLE_NOT_ONBOARDED = "Looks like given table(s) {table_names} is(are) not onboarded. Please reach out to Copilot Insight team at copilot-insight-engineering@adobe.com"
TABLE_OR_VIEW_NOT_FOUND = "Looks like table {table_name} is not present in the database. Please check the connection profile and the database you are connecting to and make sure the tables are present."
NO_ACCESS_ON_DATABRICKS_TABLE = (
    "You do not have sufficient privileges on table {table_name}"
)

MSG_NO_VALID_SQL = "NO valid SQL can be generated, please change your query accordingly"
# Error Codes
ERROR_400 = 400
ERROR_401 = 401
ERROR_200 = 200
ERROR_404 = 404
ERROR_405 = 405
ERROR_410 = 410
ERROR_415 = 415
ERROR_421 = 421
ERROR_420 = 420
ERROR_422 = 422
TABLE_OR_VIEW_NOT_FOUND_ERROR_CODE = 4041
CUSTOM_ERROR_CODE = 4001


CODE_200 = 200
# Status
STATUS_SUCCESS = "SUCCESS"

SOURCE_HANA = "hana"
SOURCE_DATABRICKS = "databricks"
SOURCE_SQL_SERVER = "sqlserver"

VALIDATION_RETRY_COUNT = 1

KPI_COUNT = 1
DEFAULT_NO_OF_DAYS = 7
copilot_insight_env_label = "copilot_insight_env"
