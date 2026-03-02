#  conn.py → DB connection (renamed from db.py)

import os
import urllib.parse
from sqlalchemy import create_engine
from utils.vault_utils import get_vault_client, get_db_config


def get_engine():
    try:
        if (os.getenv("DB_USER") and os.getenv("DB_PASSWORD") and
                os.getenv("DB_HOST") and os.getenv("DB_DATABASE")):
            client = None
        else:
            client = get_vault_client()

        db_config = get_db_config(client)

        user = db_config.get('user')
        password = urllib.parse.quote_plus(db_config.get('password'))
        host = db_config.get('host')
        port = db_config.get('port', 3306)
        database = db_config.get('database')

        connection_string = (
            f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        )

        return create_engine(connection_string)

    except Exception as e:
        raise Exception(f"Database connection failed: {e}")