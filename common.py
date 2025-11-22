from database.local_database import Database as LocalDatabase
from database.remote_database import RemoteDatabase
import os

def create_database_connection():
    sqlite_db = os.getenv("SQLITE_DB")
    if sqlite_db is None or sqlite_db == "":
        return LocalDatabase("news.db")
    elif sqlite_db.endswith(".db"):
        return LocalDatabase(sqlite_db)
    else:
        auth_token = os.getenv("REMOTE_AUTH_TOKEN")
        if not auth_token:
            raise RuntimeError("Remote DB was specified but no auth token was provided")
        return RemoteDatabase(url=sqlite_db, auth_token=auth_token)
