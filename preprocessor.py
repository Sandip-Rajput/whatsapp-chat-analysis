import pandas as pd
import re

def preprocess(data):

    pattern = r'(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s?[ap]m)\s-\s([^:]+):\s(.*)'

    messages = re.findall(pattern, data, flags=re.IGNORECASE)

    df = pd.DataFrame(messages, columns=["Date", "User", "Message"])

    df['Date'] = pd.to_datetime(
        df['Date'],
        format='%d/%m/%y, %I:%M %p'
    )
    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    df['day_name'] = df['Date'].dt.day_name()
    df['only_date']= df['Date'].dt.date
    df['Message'] = df['Message'].replace(
        '<Media omitted>',
        'Media'
    )

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
