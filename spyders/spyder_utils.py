from datetime import datetime
import pytz

def parse_datetime_jiji(datetime_string):
    input_datetime_str = datetime_string
    parsed_datetime = datetime.strptime(input_datetime_str, "%a, %d %b %Y %H:%M:%S %Z")
    parsed_datetime_utc = parsed_datetime.astimezone(pytz.UTC)
    iso8601_datetime_str = parsed_datetime_utc.strftime("%Y-%m-%dT%H:%M:%S.%f%z").replace("+0000", "+00:00")
    return iso8601_datetime_str

parse_datetime("Mon, 02 Oct 2023 07:05:54 GMT")
