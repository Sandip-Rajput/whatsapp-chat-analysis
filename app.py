import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import helper
import seaborn as sns
import pandas as pd


st.sidebar.title("WhatsApp Chat Analyzer")

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

        temp_df = preprocessor.preprocess(data)

        # file name ko group name banaya
        temp_df["Group"] = uploaded_file.name.replace(".txt", "")

        all_dfs.append(temp_df)

    df = pd.concat(all_dfs, ignore_index=True)

    # Group selection
    group_list = df["Group"].unique().tolist()
    group_list.sort()
    group_list.insert(0, "All Groups")

    selected_group = st.sidebar.selectbox("Select Group", group_list)

    if selected_group != "All Groups":
        df = df[df["Group"] == selected_group]

    # fetch unique users
    user_list = df["User"].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis", user_list)

    if st.sidebar.button("Show Analysis"):

        csv= df.to_csv(index=False).encode('utf-8')
        st.download_button(
        label="📥 Download Chat Report",
        data=csv,
        file_name="whatsapp_chat_analysis.csv",
        mime="text/csv"
        )
        
    
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Mesg.")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Link Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")

        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")

        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        sns.heatmap(user_heatmap, ax=ax)
        st.pyplot(fig)

        # finding the busiest users in the group
        if selected_user == "Overall":
            st.title("Most Busy Users")

            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # wordcloud
        st.title("WordCloud")

        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # most common words
        st.title("Most Common Words")

        most_common_df = helper.most_common_words(selected_user, df)

        if most_common_df.empty:
            st.warning("No common words found.")
        else:
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1], color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)

        st.title("Emoji Analysis")

        if emoji_df.empty:
            st.warning("No emojis found in this chat.")
        else:
            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)

            with col2:
                fig, ax = plt.subplots()
                ax.pie(
                    emoji_df['Count'].head(),
                    labels=emoji_df['Emoji'].head(),
                    autopct="%0.2f"
                )
                st.pyplot(fig)

else:
    st.title("WhatsApp Chat Analyzer")
    st.info("Please upload one or more WhatsApp exported .txt chat files.")
