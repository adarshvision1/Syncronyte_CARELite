from db_interface import DBInterface

if __name__ == '__main__':
    db = DBInterface('carelite.db')
    db.init_tables()
    print("Database initialized.")
