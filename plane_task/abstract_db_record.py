

class AbstractDbObject:
    def __init__(self, oid, table):
        self.oid = oid
        self.table = table

    # This must be overridden to work
    def __save_and_regenerate_with_id(self, db_wrapper):
        pass

    def get_max_id(self, db_wrapper):
        db_wrapper.cursor.execute(f"SELECT MAX({self.table}_id) FROM {self.table}")
        return db_wrapper.cursor.fetchone()[0]

    def delete_from_db(self, db_wrapper):
        db_wrapper.cursor.execute(f"DELETE FROM {self.table} WHERE {self.table}_id = {self.oid}")
        db_wrapper.connection.commit()
