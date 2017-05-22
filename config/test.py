DB_USER = "location_tool"
DB_PASS = "password"
DB_HOST = "localhost"
DB_NAME = "location_tool_test"
DATABASE = "postgresql://{user}:{password}@{host}/{dbname}".format(
    user=DB_USER, password=DB_PASS, host=DB_HOST, dbname=DB_NAME
)
