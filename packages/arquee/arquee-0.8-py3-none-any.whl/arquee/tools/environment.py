from dotenv import load_dotenv
from os import makedirs
from os.path import exists, join
from shutil import move
import urllib.request
from urllib.error import URLError
from platform import system

load_dotenv()


def create_folders(folders):
    for folder in folders:
        try:
            makedirs(folder, exist_ok=True)
        except Exception as e:
            print(f"Error creating folder {folder}: {e}")


def create_file(filename, content):
    if not exists(filename):
        try:
            with open(filename, "w") as file:
                file.write(content)
            print(f"File {filename} created successfully")
        except Exception as e:
            print(f"Error creating file {filename}: {e}")
    else:
        print(f"{filename} already exist, skipping creation")


def download_mssql_driver(jars_folder):
    try:
        file = "mssql-jdbc-12.8.1.jre11.jar"
        complete_jars_path = join(jars_folder, file)
        if exists(complete_jars_path):
            print("JDBC mssql driver is alredy downloaded")
            return
        url = "https://repo1.maven.org/maven2/com/microsoft/sqlserver/mssql-jdbc/12.8.1.jre11/mssql-jdbc-12.8.1.jre11.jar"
        urllib.request.urlretrieve(url, file)
        move(file, jars_folder)
        print("Download of JDBC mssql driver is done")
    except URLError:
        print(
            "Error downloading the MSSQL JDBC driver. Please check your internet connection."
        )


def check_jars():
    platform = system().lower()
    if platform == "windows":
        jars_folder = join(".venv", "Lib", "site-packages", "pyspark", "jars")
    else:
        jars_folder = join(
            ".venv", "lib", "python3.9", "site-packages", "pyspark", "jars"
        )
    download_mssql_driver(jars_folder)
