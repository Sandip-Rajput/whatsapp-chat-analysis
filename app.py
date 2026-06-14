import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns
import pandas as pd


st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)


st.sidebar.title("💬 WhatsApp Chat Analyzer")

dark_mode = st.sidebar.toggle("🌙 Dark Mode")


if dark_mode:
    st.markdown("""
    <style>
    .stApp {background-color:#111827; color:white;}
    h1,h2,h3,p,label {color:white !important;}
    [data-testid="stSidebar"] {background-color:#075E54;}
    [data-testid="stSidebar"] * {color:white;}
    .metric-card {
        background:#1f2937;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0px 4px 15px rgba(255,255,255,0.1);
    }
    .metric-title {font-size:18px; color:#d1d5db;}
    .metric-value {font-size:35px; font-weight:bold; color:#25D366;}
    input {color:black !important;}
    [data-baseweb="select"] * {color:black !important;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    .stApp {background-color:#f5f7fa;}
    [data-testid="stSidebar"] {background-color:#075E54;}
    [data-testid="stSidebar"] * {color:white;}
    .metric-card {
        background:white;
        padding:20px;
        border-radius:15px;
        text-align:center;
        box-shadow:0px 4px 15px rgba(0,0,0,0.1);
    }
    .metric-title {font-size:18px; color:#555;}
    .metric-value {font-size:35px; font-weight:bold; color:#128C7E;}
    input {color:black !important;}
    [data-baseweb="select"] * {color:black !important;}
    </style>
    """, unsafe_allow_html=True)


st.markdown("""
<h1 style='text-align:center; color:#128C7E;'>
💬 WhatsApp Chat Analyzer Dashboard
</h1>
<p style='text-align:center; font-size:18px;'>
Analyze Messages • Groups • Users • Emojis • Media • Links • Sentiment
</p>
""", unsafe_allow_html=True)


uploaded_files = st.sidebar.file_uploader(
    "Choose WhatsApp chat files",
    type=["txt"],
    accept_multiple_files=True
)


if uploaded_files:

    all_dfs = []

    for uploaded_file in uploaded_files:

        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")

        group_name = uploaded_file.name.replace(".txt", "")

        temp_df = preprocessor.preprocess(data, group_name)

        all_dfs.append(temp_df)

    df = pd.concat(all_dfs, ignore_index=True)

    if df.empty:
        st.error("Chat data read nahi ho raha. Export format check karo.")
        st.stop()

    st.sidebar.subheader("📅 Date Filter")

    min_date = df['only_date'].min()
    max_date = df['only_date'].max()

    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)

    df = df[
        (df['only_date'] >= start_date) &
        (df['only_date'] <= end_date)
    ]

    if df.empty:
        st.warning("Selected date range me data nahi hai.")
        st.stop()

    group_list = df["Group"].unique().tolist()
    group_list.sort()
    group_list.insert(0, "All Groups")

    selected_group = st.sidebar.selectbox("Select Group", group_list)

    if selected_group != "All Groups":
        df = df[df["Group"] == selected_group]

    user_list = df["User"].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user,
            df
        )

        deleted_count = helper.deleted_message_count(
            selected_user,
            df
        )

        st.title("📊 Top Statistics")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Messages</div>
                <div class="metric-value">{num_messages}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Words</div>
                <div class="metric-value">{words}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Media</div>
                <div class="metric-value">{num_media_messages}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Links</div>
                <div class="metric-value">{num_links}</div>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Deleted Msg</div>
                <div class="metric-value">{deleted_count}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.title("💡 Chat Insights")

        insights = helper.chat_insights(df)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.info(f"🏆 Top Group: {insights['top_group']}")

        with c2:
            st.info(f"👤 Top User: {insights['top_user']}")

        with c3:
            st.info(f"📅 Busy Day: {insights['top_day']}")

        with c4:
            st.info(f"🗓️ Busy Month: {insights['top_month']}")

        st.markdown("---")

        emoji_df = helper.emoji_helper(selected_user, df)

        c1, c2 = st.columns(2)

        with c1:
            st.title("😀 Top Emoji Card")

            if emoji_df.empty:
                st.warning("No emojis found.")
            else:
                top_emoji = emoji_df.iloc[0]['Emoji']
                top_emoji_count = emoji_df.iloc[0]['Count']
                st.success(
                    f"Most Used Emoji: {top_emoji} | Count: {top_emoji_count}"
                )

        with c2:
            st.title("👑 Top Active User Card")

            if df.empty:
                st.warning("No data found.")
            else:
                top_user = df['User'].value_counts().idxmax()
                top_user_count = df['User'].value_counts().max()
                st.success(
                    f"Top User: {top_user} | Messages: {top_user_count}"
                )

        st.markdown("---")

        st.title("📌 Group Comparison")

        group_comparison = helper.group_comparison(df)

        if group_comparison.empty:
            st.warning("No group comparison data found.")
        else:
            fig, ax = plt.subplots()
            ax.bar(group_comparison.index, group_comparison.values, color='green')
            plt.xticks(rotation='vertical')
            ax.set_ylabel("Total Messages")
            st.pyplot(fig)

        st.title("🏅 Group Ranking Table")

        group_rank = helper.group_ranking_table(df)
        st.dataframe(group_rank)

        st.markdown("---")

        st.title("😊 Sentiment Analysis")

        sentiment_df = helper.sentiment_analysis(selected_user, df)

        c1, c2 = st.columns(2)

        with c1:
            st.dataframe(sentiment_df)

        with c2:
            fig, ax = plt.subplots()
            ax.pie(
                sentiment_df['Count'],
                labels=sentiment_df['Sentiment'],
                autopct="%0.2f%%"
            )
            st.pyplot(fig)

        st.markdown("---")

        st.title("📆 Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, df)

        if timeline.empty:
            st.warning("No monthly data found.")
        else:
            fig, ax = plt.subplots()
            ax.plot(timeline['time'], timeline['Message'], color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("📅 Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)

        if daily_timeline.empty:
            st.warning("No daily data found.")
        else:
            fig, ax = plt.subplots()
            ax.plot(
                daily_timeline['only_date'],
                daily_timeline['Message'],
                color='black'
            )
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("🔥 Activity Map")

        c1, c2 = st.columns(2)

        with c1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with c2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("🕒 Weekly Activity Map")

        user_heatmap = helper.activity_heatmap(selected_user, df)

        if user_heatmap.empty:
            st.warning("No heatmap data found.")
        else:
            fig, ax = plt.subplots()
            sns.heatmap(user_heatmap, ax=ax)
            st.pyplot(fig)

        if selected_user == "Overall":

            st.title("👥 Most Busy Users")

            x, new_df = helper.most_busy_users(df)

            c1, c2 = st.columns(2)

            with c1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with c2:
                st.dataframe(new_df)

        st.title("☁️ WordCloud")

        df_wc = helper.create_wordcloud(selected_user, df)

        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        st.title("📝 Most Common Words")

        most_common_df = helper.most_common_words(selected_user, df)

        if most_common_df.empty:
            st.warning("No common words found.")
        else:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("😀 Emoji Analysis")

        if emoji_df.empty:
            st.warning("No emojis found in this chat.")
        else:
            c1, c2 = st.columns(2)

            with c1:
                st.dataframe(emoji_df)

            with c2:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df['Count'].head(),
                    labels=emoji_df['Emoji'].head(),
                    autopct="%0.2f%%"
                )
                st.pyplot(fig)

        st.markdown("---")

        st.title("📥 Download CSV Report")

        csv = df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Chat Report CSV",
            data=csv,
            file_name="whatsapp_chat_analysis.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload one or more WhatsApp exported .txt chat files.")
