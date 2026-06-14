import pandas as pd
import re


def preprocess(data, group_name="Unknown Group"):

    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?(?:am|pm)?)\s-\s([^:]+):\s(.*)'

    messages = re.findall(pattern, data, flags=re.IGNORECASE)

    df = pd.DataFrame(messages, columns=["Date", "User", "Message"])

    df['Date'] = pd.to_datetime(
        df['Date'],
        errors='coerce',
        dayfirst=True
    )

    df = df.dropna(subset=['Date'])

    df['year'] = df['Date'].dt.year
    df['month_num'] = df['Date'].dt.month
    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute
    df['day_name'] = df['Date'].dt.day_name()
    df['only_date'] = df['Date'].dt.date

    df['Message'] = df['Message'].replace('<Media omitted>', 'Media')
    df['Group'] = group_name

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
