from SQLiteDB.api_key_db import APIKey


api = APIKey()
api.connect()
api.issue()
print(api.fetch_all())