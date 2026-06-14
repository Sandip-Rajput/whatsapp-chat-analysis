from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['Message']:
        words.extend(str(message).split())

    num_media_messages = df[df["Message"] == 'Media'].shape[0]

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(str(message)))

    return num_messages, len(words), num_media_messages, len(links)


def deleted_message_count(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    deleted_count = df[
        df['Message'].str.contains(
            'deleted|This message was deleted|You deleted this message',
            case=False,
            na=False
        )
    ].shape[0]

    return deleted_count


def most_busy_users(df):

    x = df['User'].value_counts().head(10)

    new_df = round(
        (df['User'].value_counts() / df.shape[0]) * 100,
        2
    ).reset_index()

    new_df.columns = ['User', 'Percent']

    return x, new_df


def create_wordcloud(selected_user, df):

    try:
        f = open('stop_hinglish.txt', 'r', encoding='utf-8')
        stop_words = f.read()
    except:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['Message'] != 'Media'].copy()

    def remove_stopwords(message):
        y = []
        for word in str(message).lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(
        width=500,
        height=500,
        min_font_size=2,
        background_color='white'
    )

    temp['Message'] = temp['Message'].apply(remove_stopwords)

    text = temp['Message'].str.cat(sep=" ")

    if text.strip() == "":
        text = "No Words Found"

    df_wc = wc.generate(text)

    return df_wc


def most_common_words(selected_user, df):

    try:
        f = open('stop_hinglish.txt', 'r', encoding='utf-8')
        stop_words = f.read()
    except:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['Message'] != 'Media']

    words = []

    for message in temp['Message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis = []

    for message in df['Message']:
        emojis.extend([c for c in str(message) if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(
        Counter(emojis).most_common(),
        columns=['Emoji', 'Count']
    )

    return emoji_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    timeline = df.groupby(
        ['year', 'month_num', 'month']
    ).count()['Message'].reset_index()

    timeline = timeline.sort_values(['year', 'month_num'])

    time = []

    for i in range(timeline.shape[0]):
        time.append(
            timeline['month'].iloc[i] + "-" + str(timeline['year'].iloc[i])
        )

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline


def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()


def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['month'].value_counts()


def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(
        index='day_name',
        columns='period',
        values='Message',
        aggfunc='count'
    ).fillna(0)

    return user_heatmap


def group_comparison(df):

    return df.groupby('Group')['Message'].count().sort_values(ascending=False)


def group_ranking_table(df):

    ranking = df.groupby('Group').agg(
        Total_Messages=('Message', 'count'),
        Total_Users=('User', 'nunique'),
        Media_Shared=('Message', lambda x: (x == 'Media').sum())
    ).reset_index()

    ranking = ranking.sort_values(
        by='Total_Messages',
        ascending=False
    )

    return ranking


def sentiment_analysis(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    positive_words = [
        'good', 'great', 'awesome', 'best',
        'happy', 'love', 'excellent',
        'nice', 'amazing', 'thank',
        'thanks', 'mast', 'badhiya',
        'acha', 'accha'
    ]

    negative_words = [
        'bad', 'hate', 'sad', 'problem',
        'issue', 'error', 'worst',
        'angry', 'bekar', 'gussa',
        'wrong', 'fail'
    ]

    positive = 0
    negative = 0
    neutral = 0

    for msg in df['Message']:

        msg = str(msg).lower()

        if any(word in msg for word in positive_words):
            positive += 1
        elif any(word in msg for word in negative_words):
            negative += 1
        else:
            neutral += 1

    sentiment_df = pd.DataFrame({
        'Sentiment': ['Positive', 'Negative', 'Neutral'],
        'Count': [positive, negative, neutral]
    })

    return sentiment_df


def chat_insights(df):

    insights = {
        "top_group": df['Group'].value_counts().idxmax(),
        "top_user": df['User'].value_counts().idxmax(),
        "top_day": df['day_name'].value_counts().idxmax(),
        "top_month": df['month'].value_counts().idxmax()
    }

    return insights
