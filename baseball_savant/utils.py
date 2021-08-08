from datetime import date, datetime, timedelta


#Yesterday as the request date for the client
def get_request_date():
    dt = datetime.today() - timedelta(days=1)
    return dt.strftime('%Y-%m-%d')