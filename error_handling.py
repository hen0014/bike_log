# error_handling.py

import sqlite3
from log_config import LogConfig
log_config = LogConfig()
logger = log_config.get_logger()

def handle_errors(custom_info=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except sqlite3.IntegrityError as e:
                logger.error(f"Integrity Error in {custom_info}: {e}")
                return 1
            except sqlite3.OperationalError as e:
                logger.error(f"Operational Error in {custom_info}: {e}")
                return 1
            except sqlite3.DatabaseError as e:
                logger.error(f"Database Error in {custom_info}: {e}")
                return 1
            except Exception as e:
                logger.error(f"Unexpected Error in {custom_info}: {e}")
                return 1
        return wrapper
    return decorator