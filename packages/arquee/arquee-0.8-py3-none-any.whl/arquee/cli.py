from .tools.environment import create_file, create_folders, check_jars
from .config import logs_folder, datalake, warehouse


def set_environment_utils():
    create_folders([logs_folder, datalake, warehouse])
    env_content = (
        'ORIGIN_DB={"host": "host", "port": 1433, "user": "user", "pwd": "password", "db_name": "some_db"}\n'
        'DESTINY_DB={"host": "host", "port": 1433, "user": "user", "pwd": "password", "db_name": "some_db"}\n'
    )
    create_file(".env", env_content)
    create_file(
        "arquee.txt",
        "Here you can specify the tables for create the datalake, delete this line :)\n",
    )
    check_jars()


def otro_test():
    pass


if __name__ == "__main__":
    set_environment_utils()
