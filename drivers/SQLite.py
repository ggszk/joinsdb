import sqlite3

# Storage engine for SQLite
class SQLite :
    # initialize
    def __init__(self, param):
        self.driver = sqlite3.connect(param)

    # Execute cypher query
    def executeQuery(self, sql):
        result = []
        c = self.driver.cursor()
        for row in c.execute(sql):
            result.append(row)
        return result

    # Close connection
    def close(self) :
        self.driver.close()
