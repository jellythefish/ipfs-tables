import psycopg2

class DatabaseClient(object):
    def __init__(self, name, user, password, host, port):
        try:
            self.conn = psycopg2.connect(dbname=name, user=user, password=password, host=host, port=port,
                                     connection_timeout=10)
        except Exception as e:
            print(f"error occured while connecting to the database: {e}")
            self.conn = None


    def add(self, meta):
        try:
            if self.conn is None:
                raise Exception("Connection to remote metadata database was not initialized.")
            query = '''INSERT INTO metadata (hash, name, type, file_extension, media_format, upload_timestamp, bytesize, tags, uploaded_by) VALUES (%s, %s, %s, %s, %s, TO_TIMESTAMP(%s), %s, %s, %s);'''
            cursor = self.conn.cursor()
            cursor.execute(query, (meta["hash"], meta["name"], meta["type"], meta["file_extension"], meta["media_format"], meta["upload_timestamp"], meta["bytesize"], meta["tags"], meta["uploaded_by"]))
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"error occured while appending to database: {e}")