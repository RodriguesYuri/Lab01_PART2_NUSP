from io import StringIO

def get_info(df):
    buffer = StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()

def get_nulls(df):
    return df.isnull().sum()

def get_describe(df):
    return df.describe(include='all')