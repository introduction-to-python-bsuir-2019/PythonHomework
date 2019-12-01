def convert_date(date):
    '''Convert date to make a search in our local storage'''
    month = {'Jan': '1',
             'Feb': '2',
             'Mar': '3',
             'Apr': '4',
             'May': '5',
             'Jun': '6',
             'Jul': '7',
             'Aug': '8',
             'Sep': '9',
             'Oct': '10',
             'Nov': '11',
             'Dec': '12'}
    day = date[5:7]
    month_int = month[date[8:11]]
    year = date[12:16]

    return int(year+month_int+day)