import configparser
import pymysql
from pymysql.err import MySQLError

class ConnectionDB:
    """
    Singleton class for database connection using PyMySQL.
    Ensures only one connection instance exists throughout the application.
    """

    __instance = None  # Holds the singleton instance

    def __new__(cls):
        """
        Overrides __new__ to ensure only one instance is created.
        """
        if cls.__instance is None:
            cls.__instance = super(ConnectionDB, cls).__new__(cls)
            cls.__instance.__initialize()
        return cls.__instance

    def __initialize(self):
        """
        Initializes the database connection using db_config.ini
        """
        try:
            config = configparser.ConfigParser()
            config.read("db_config.ini")

            self.connection = pymysql.connect(
                host=config.get("mysql", "host"),
                user=config.get("mysql", "user"),
                password=config.get("mysql", "password"),
                database=config.get("mysql", "database"),
                cursorclass=pymysql.cursors.DictCursor
            )

            print("Connected to MySQL database successfully.")

        except MySQLError as e:
            print(f"Error connecting to MySQL: {e}")
            self.connection = None

    def get_connection(self):
        """
        Returns the established database connection instance.
        """
        return self.connection
