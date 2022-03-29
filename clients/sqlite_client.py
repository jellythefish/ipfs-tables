import sqlite3


class LocalSQLiteDatabaseClient(object):
    def __init__(self):
        self.conn = sqlite3.connect('meta.db')
        cursor = self.conn.cursor()
        create_query = '''
            CREATE TABLE IF NOT EXISTS metadata (
                hash TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                file_extension TEXT,
                media_format TEXT,
                upload_timestamp INTEGER NOT NULL,
                bytesize INT NOT NULL,
                tags TEXT,
                uploaded_by TEXT
            )
        '''
        cursor.execute(create_query)
        self.conn.commit()


    def add(self, meta):
        try:
            query = '''
                INSERT INTO metadata 
                (hash, name, type, file_extension, media_format, upload_timestamp, bytesize, tags, uploaded_by) 
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
            '''.format(meta["hash"], meta["name"], meta["type"], meta["file_extension"], meta["media_format"], 
                    meta["upload_timestamp"], meta["bytesize"], meta["tags"], meta["uploaded_by"])
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"error occured while appending to database: {e}")


    def get(self, key, value):
        try:
            query = "SELECT * FROM metadata WHERE {}='{}';".format(key, value)
            cursor = self.conn.cursor()
            result = cursor.execute(query).fetchall()
            self.conn.commit()
            cursor.close()
            return result
        except Exception as e:
            print(f"error occured while getting from database: {e}")
            

# def example():
#     client = LocalSQLiteDatabaseClient()
#     meta = {
#         "hash": "sdgf3iu4thgiudsfhnjk76lg",
#         "name": "test2.md",
#         "type": "file",
#         "file_extension": ".md",
#         "media_format": "notes",
#         "upload_timestamp": "32456342",
#         "bytesize": "4543",
#         "tags": "tag1,tag2",
#         "uploaded_by": "somebody",
#     }
#     client.add(meta)
#     print(client.get("upload_timestamp", "32456342"))


# if __name__ == '__main__':
#     example()
