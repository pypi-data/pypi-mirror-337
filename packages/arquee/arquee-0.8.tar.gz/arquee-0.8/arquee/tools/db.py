import json
from json.decoder import JSONDecodeError
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def get_db_url(variable_name: str):
    expected_keys = ["host", "port", "user", "pwd", "db_name"]
    try:
        db_variable = getenv(variable_name)
        values = json.loads(db_variable)
        missing_keys = [key for key in expected_keys if key not in list(values.keys())]

        if missing_keys:
            raise ValueError(missing_keys)

        host = values["host"]
        db_name = values["db_name"]
        user = values["user"]
        pwd = values["pwd"]
        port = values["port"]

        url = f"jdbc:sqlserver://{host}:{port};databaseName={db_name};user={user};password={pwd};encrypt=false;"

        return url

    except ValueError as e:
        print(f"Missing {list(e.args)[0]} keys on JSON object")

    except JSONDecodeError:
        print(f"Error reading {variable_name} variable, variable must be a JSON object")
