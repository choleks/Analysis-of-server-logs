import pandas as pd
import matplotlib.pyplot as plt
from re import search


def create_frame():
    """Create DataFrame
    """

    with open('access.log') as file:
        access_log = file.read().split('\n')

    rows = []

    for string in access_log:
        if not len(string):
            continue

        row = []
        row.append(string[:string.find(' ')])
        row.append(string[string[:-1].rfind('"') + 1:-1])
        row.append(search(r'\[.{26}\]', string).group()[1:-7])

        try:
            row.append(search(r'\"http[^\"]*', string).group()[1:])

        except AttributeError:
            row.append('-')

        row.append(search(r'\" \d{3} ', string).group()[2:-1])
        rows.append(row)

    df = pd.DataFrame(rows, columns=['ip', 'user_agent', 'time', 'referer', 'status'])
    df['status'] = df['status'].astype('int')
    df['time'] = pd.to_datetime(df['time'], format='%d/%b/%Y:%H:%M:%S')
    df.to_csv('data.csv', index=False)


def show_freq(df):
    date_range = pd.date_range(start=df['time'].min().date(), end=df['time'].max().date()).to_series().dt.date
    frequencies = [df[df['time'].dt.date == date].shape[0] for date in date_range]
    plt.plot(date_range, frequencies)
    plt.show()


df = pd.read_csv('data.csv')
df['time'] = pd.to_datetime(df['time'])
show_freq(df)
