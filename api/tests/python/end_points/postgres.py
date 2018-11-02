import os
import psycopg2

class Postgres(object):

    def __init__(self):
        self.database = os.environ['DATABASE_TEST_NAME']
        self.user = os.environ['DATABASE_TEST_USERNAME']
        self.password = os.environ['DATABASE_TEST_PASSWORD']

    def execute(self, sql, values=()):
        with psycopg2.connect(host='localhost',dbname=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, values)

    def selectFirst(self, sql):
        with psycopg2.connect(host='localhost',dbname=self.database, user=self.user, password=self.password) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()
