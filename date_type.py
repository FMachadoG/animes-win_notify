class DateType:
    """
    :param
        - date: is datetime: %Y-%m-%d
        - datetime1: is date: format %Y-%m-%d %H:%M
        - datetime2: is date: format %Y-%m-%d %H:%M:%S
    """

    def __init__(self, date_type):
        self.date_type = date_type

    def __str__(self):
        return self.date_type


class DateFormat:
    """
    :param
        - date: is datetime: %Y-%m-%d
        - datetime1: is date: format %Y-%m-%d %H:%M
        - datetime2: is date: format %Y-%m-%d %H:%M:%S
    """
    def __init__(self, date_format):
        self.date_format = date_format

    def __str__(self):
        return self.date_format


Date = DateType('date')
Datetime1 = DateType('datetime1')
Datetime2 = DateType('datetime2')

Fdate = str(DateFormat('%Y-%m-%d'))
Fdatetime1 = str(DateFormat('%Y-%m-%d %H:%M'))
Fdatetime2 = str(DateFormat('%Y-%m-%d %H:%M:%S'))
