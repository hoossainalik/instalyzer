"""
Module: Sentiment Analysis
Author: Hussain Ali Khan
Version: 1.0.0
Last Modified: 29/11/2018 (Thursday)
"""


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import re
import os
from emoji import UNICODE_EMOJI
import matplotlib.pyplot as plt
import seaborn as sns


class ResultData:
    def __init__(self, data=[], scores=[]):
        self.data = data
        self.scores = scores

    def get_data(self):
        return self.data

    def get_scores(self):
        return self.scores


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.dataset = None
        self.opened_dataset = None

    def load_dataset(self, dir_name):
        files_list = os.listdir(dir_name)

        print("Please Select The DataSet That You Want To Open: ")

        for i in range(len(files_list)):
            print(i+1, ". ", files_list[i])

        choice = int(input("Choice: "))

        self.opened_dataset = files_list[choice-1]
        self.dataset = pd.read_csv(dir_name + "/" + self.opened_dataset)

    def sentiment_analyzer_scores(self, data):
        score = self.analyzer.polarity_scores(data)
        print("{:-<40} {}".format(data, str(score)))

    def process_descriptions(self):
        descriptions = self.dataset["description"]
        scores = []
        c_descriptions = []
        for desc in descriptions:
            desc = str(desc)
            c_descriptions.append(desc[1:-1])

        cleaned_descriptions = clean_list(c_descriptions)

        # print("<----Post Descriptions Sentiment Scores---->")

        for c_d in cleaned_descriptions:
            scores.append(self.analyzer.polarity_scores(c_d))
            # self.print_sentiment_scores(c_d)

        # print("<------------------------------------------>")

        rd = ResultData(cleaned_descriptions, scores)
        return rd

    def print_sentiment_scores(self, text):
        txt = self.analyzer.polarity_scores(text)
        print("{:-<40} {}".format(text, str(txt)))

    def process_comments(self):
        comments_lists = sa.dataset["comments"]
        scores = []
        all_comments = []

        for c in comments_lists:
            c = str(c).replace('[', '')
            c = str(c).replace(']', '')
            c = c.split(', ')
            c = [comment.replace("'", "") for comment in c]
            c = c[1::2]

            for each_c in c:
                all_comments.append(each_c)

        cleaned_comments = clean_list(all_comments)

        # print("<----Post Comments Sentiment Scores---->")

        for c_c in cleaned_comments:
            scores.append(self.analyzer.polarity_scores(c_c))
            # self.print_sentiment_scores(c_c)

        # print("<-------------------------------------->\n")

        rd = ResultData(cleaned_comments, scores)

        return rd


def save_results_as_csv(results, fn, c_name):
    results_df = pd.DataFrame(results.get_scores())

    results_df['class'] = results_df[['pos', 'neg', 'neu']].idxmax(axis=1)

    results_df['class'] = results_df['class'].map({'pos': 'Positive', 'neg': 'Negative', 'neu': 'Neutral'})

    text_df = pd.DataFrame(results.get_data(), columns=[c_name])
    final_df = text_df.join(results_df)
    print(final_df)
    print(final_df.describe())

    pie_plot_title = "Pie Plot For Sentiments Of " + c_name + " In dataset <" + fn + ">"

    final_df["class"].value_counts().plot(kind="pie", autopct='%.1f%%', figsize=(8, 8), title=pie_plot_title)

    pp = sns.pairplot(final_df, hue="class", height=3)
    pp.fig.suptitle("Pair Plot For Sentiments Of "+c_name+" In dataset <"+fn+">")
    plt.show()
    final_df.to_csv("SentimentAnalysisResults/" + fn + ".csv")


# search your emoji
def is_emoji(s):
    return s in UNICODE_EMOJI


# add space near your emoji
def add_space(text):
    return ''.join(' ' + char if is_emoji(char) else char for char in text).strip()


def clean_text(text):
    text = filter_mentions(text)
    text = text.replace('#', '')
    text = text.replace('/', ' ')
    text = text.replace('_', ' ')
    text = text.replace('❤', ' Love ')
    text = text.replace('-', ' ')
    text = re.sub(' +', ' ', text).strip()
    text = re.sub(r'https?:/\/\S+', ' ', text).strip()  # remove links
    text = re.sub('[^A-Za-z0-9]+', ' ', text).strip()
    text = add_space(text)
    return text


def filter_mentions(text):
    return " ".join(filter(lambda x: x[0] != '@', text.split()))


def clean_list(_list):
    cleaned_list = []
    for l in _list:
        cleaned = clean_text(l)
        if len(cleaned) > 0:
            cleaned_list.append(cleaned)
    return cleaned_list


def main():

    sa = SentimentAnalyzer()
    sa.load_dataset("Posts")

    print("<---Sentiment Analysis Results On Post Descriptions--->")
    description_results = sa.process_descriptions()
    save_results_as_csv(description_results, sa.opened_dataset + "_descriptions_sa_results", "descriptions")
    print("<----------------------------------------------------->")

    print("<---Sentiment Analysis Results On All Post Comments--->")
    comments_results = sa.process_comments()
    save_results_as_csv(comments_results, sa.opened_dataset + "_comments_sa_results", "comments")
    print("<----------------------------------------------------->")






if __name__ == "__main__":
    main()