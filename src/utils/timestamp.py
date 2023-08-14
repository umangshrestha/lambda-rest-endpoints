from datetime import datetime

def get_date_string():
    strformat = "%d/%m/%Y %H:%M:%S"
    return datetime.now().strftime(strformat)
