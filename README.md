# WhatsApp Chat Analyzer using Python & Streamlit

## Project Overview

WhatsApp Chat Analyzer is an interactive data analytics web application built using Python and Streamlit. The application allows users to upload exported WhatsApp chat files and generate meaningful insights from both Individual Chats and Group Chats.

The project performs message analysis, user activity analysis, emoji analysis, word frequency analysis, timeline tracking, and visual reporting through interactive charts and dashboards.

---

## Problem Statement

WhatsApp conversations contain a large amount of information, but manually identifying communication patterns, active users, popular words, and chat trends is difficult.

This project helps users automatically analyze WhatsApp chat data and generate meaningful visual insights.

---

## Key Features

### Message Statistics

* Total Messages
* Total Words
* Total Media Shared
* Total Links Shared

### Timeline Analysis

* Monthly Timeline
* Daily Timeline

### Activity Analysis

* Most Active Day
* Most Active Month
* Weekly Activity Heatmap

### User Analysis

* Most Active Users
* User Contribution Percentage

### Text Analysis

* Word Cloud Generation
* Most Common Words Analysis

### Emoji Analysis

* Most Frequently Used Emojis
* Emoji Distribution Pie Chart

---

## Technologies Used

* Python
* Streamlit
* Pandas
* Matplotlib
* Seaborn
* WordCloud
* URLExtract
* Emoji
* Regular Expressions (Regex)

---

## Dataset

Input data is an exported WhatsApp chat text file (.txt).

The application supports:

* Individual Chat Analysis
* Group Chat Analysis

---

## Project Workflow

### 1. Data Collection

Export WhatsApp chat as a .txt file.

### 2. Data Preprocessing

Using Regex:

* Extract Date
* Extract Time
* Extract User Name
* Extract Message

Additional Features:

* Year
* Month
* Day
* Hour
* Minute
* Day Name
* Time Period

### 3. Data Cleaning

* Handle media messages
* Remove unnecessary text
* Convert dates into datetime format

### 4. Text Processing

A custom stop-word file (stop_hinglish.txt) is used to remove common Hindi-English words such as:

* hai
* tha
* kar
* kya
* the
* is
* and

This improves the quality of:

* Word Cloud
* Common Word Analysis

### 5. Analytics Generation

The application calculates:

* Message Statistics
* User Activity
* Chat Trends
* Emoji Usage
* Common Words

### 6. Visualization

Generated charts include:

* Line Charts
* Bar Charts
* Pie Charts
* Heatmaps
* Word Clouds

---

## Project Structure

WhatsApp-Chat-Analyzer/

│

├── app.py

├── helper.py

├── preprocessor.py

├── stop_hinglish.txt

├── requirements.txt

├── README.md

│

└── Sample Chat.txt

---

## Libraries Used

streamlit

pandas

matplotlib

seaborn

wordcloud

emoji

urlextract

re

collections

---

## How To Run

### Install Libraries

pip install -r requirements.txt

### Run Project

streamlit run app.py

---

## Skills Demonstrated

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Text Analytics
* Data Visualization
* Dashboard Development
* Python Programming
* Streamlit Application Development
* Regular Expressions (Regex)

---

## Future Improvements

* Sentiment Analysis
* AI-based Chat Summarization
* User Personality Insights
* Topic Modeling
* Chat Prediction
* Deployment on Streamlit Cloud

---

## Author

Sandip Rajput

B.Tech Computer Engineering

Data Analyst | Python Developer | AI/ML Enthusiast
