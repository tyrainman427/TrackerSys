import pandas as pd


def get_data(request):
    df=pd.read_csv(filepath_or_buffer = 'film.csv')
    return df
