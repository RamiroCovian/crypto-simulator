import sqlite3


class DBManager:
    def __init__(self, path):
        self.path = path

    def connect(self):
        connection = sqlite3.connect(self.path)
        cursor = connection.cursor()
        return connection, cursor

    def disconnect(self, connection):
        connection.close()

    def consultSQL(self, consult):
        connection, cursor = self.connect()
        cursor.execute(consult)
        data = cursor.fetchall()

        self.records = []
        col_names = []
        for col in cursor.description:
            col_names.append(col[0])
        for fact in data:
            movement = {}
            index = 0
            for name in col_names:
                movement[name] = fact[index]
                index += 1
            self.records.append(movement)

        self.disconnect(connection)
        return self.records
