import sqlite3

class Index:
    def __init__(self):
        self.db_file = "index.db"
        self.tableIndexes = '''CREATE TABLE IF NOT EXISTS indexes
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     path TEXT,
                     name VARCHAR(255),
                     objects TEXT,
                     type VARCHAR(50),
                     ocr_text TEXT,
                     caption TEXT DEFAULT NULL)'''
        self.create_init_tables()

    def create_init_tables(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(self.tableIndexes)
        conn.commit()
        conn.close()

    def get_index(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes")
        data = c.fetchall()
        conn.close()
        return data
    
    def get_image(self, path):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes WHERE path = '%s'" % path)
        data = c.fetchone()
        conn.close()
        return data

    def add_index(self, name, path, objects=None, type=None, ocr_text=None, caption=None):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("INSERT INTO indexes (name, path, objects, type, ocr_text, caption) VALUES (?, ?, ?, ?, ?, ?)", (name, path, objects, type, ocr_text, caption))
        conn.commit()
        conn.close()
        
    def reset_index(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("DELETE FROM indexes")
        conn.commit()
        conn.close()
        
    def get_unique_objects(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT objects FROM indexes")
        data = c.fetchall()
        conn.close()

        unique_objects = set()
        for row in data:
            objects = eval(row[0])
            unique_objects.update(objects)

        return list(unique_objects)
    
    def get_unique_folders(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT path FROM indexes")
        data = c.fetchall()
        conn.close()

        unique_folders = set()
        for row in data:
            unique_folders.add(row[0])

        return list(unique_folders)
    
    def get_unique_types(self):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT type FROM indexes")
        data = c.fetchall()
        conn.close()

        unique_types = set()
        for row in data:
            unique_types.add(row[0])

        return list(unique_types)
    
    def get_object_members(self, object):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes WHERE objects LIKE ?", ('%'+object+'%',))
        data = c.fetchall()
        conn.close()
        return data

    def get_type_members(self, type):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes WHERE type = '%s'" % type)
        data = c.fetchall()
        conn.close()
        return data
    
    def get_folder_members(self, folder):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes WHERE path LIKE ?", ('%'+folder+'%',))
        data = c.fetchall()
        conn.close()
        return data
    
    def get_ocr_members(self, text):
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT * FROM indexes WHERE ocr_text LIKE ?", ('%'+text+'%',))
        data = c.fetchall()
        conn.close()
        return data