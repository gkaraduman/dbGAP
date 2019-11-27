import psycopg2

class DatabaseOperations:
    def __init__(self):
        self.conn = None
        self.connect()

    def __del__(self):
        self.conn.close()
        print('Database connection closed.')

    def connect(self):
        if(self.conn is None):
            try:
                print('Connecting to the PostgreSQL database...')
                self.conn = psycopg2.connect(host="localhost", database="gulsah", user="postgres", password="postgres")
                print('Connection established')
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

    def executeQuery(self, query, parameters):
        if (self.conn is not None):
            try:
                cur = self.conn.cursor()
                cur.execute(query, parameters)
                cur.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print('Exception occurred during insert:' + str(error))

    def commit(self):
        self.conn.commit()

