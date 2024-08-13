# error_handling.py

import sqlite3
def handle_errors(custom_info=None):
    def decotrator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.IntegrityError as e:
                print(f"Integrity Error in {custom_info}: {e}")
                return 1
            except sqlite3.OperationalError as e:
                print(f"Operational Error in {custom_info}: {e}")
                return 1
            except sqlite3.DatabaseError as e:
                print(f"Database Error in {custom_info}: {e}")
                return 1
            except Exception as e:
                print(f"Unexpected Error in {custom_info}: {e}")
                return 1
        return wrapper