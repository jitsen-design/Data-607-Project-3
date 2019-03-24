
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
# nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='whitegrid')


# references: https://www.learndatasci.com/tutorials/sentiment-analysis-reddit-headlines-pythons-nltk/

filepath = "/Users/euniceok/PycharmProjects/cuny/spring2019/Week8/Data-607-Project-3"
outputfilepath = '/Users/euniceok/PycharmProjects/cuny/spring2019/Week8/Data-607-Project-3/Eunice/output/'
filename = '/data/500_jobs.csv'
jddf = pd.read_csv(filepath + filename).drop('Unnamed: 0', axis=1)
jddf = jddf.drop_duplicates()

desc = jddf['job_description'].str.cat(sep=' ')

sia = SIA()
results = []

for jd in jddf['job_description']:
    pol_score = sia.polarity_scores(jd)
    pol_score['jd'] = jd
    results.append(pol_score)

df = pd.DataFrame.from_records(results)

full = pd.merge(df, jddf, how='left', left_on='jd', right_on='job_description').drop('job_description',axis=1)

full['label'] = 0
full.loc[full['compound'] > 0.2, 'label'] = 1
full.loc[full['compound'] < -0.2, 'label'] = -1

full['city'] = full['job_location'].apply(lambda x: x.split(',')[0].strip())
full['state'] = full['job_location'].apply(lambda x: x.split(',')[-1][:3].strip())

full.to_csv('/Users/euniceok/PycharmProjects/cuny/spring2019/Week8/Data-607-Project-3/Eunice/output/sent_scored.csv')


# read csv back in
ind = pd.read_excel(filepath + '/Eunice/sent_scored_industry.xlsx')

# shape data for plot of distribution of sentiments
sentiment = ind.label.value_counts(normalize=True) * 100
sentiment.loc[0] = 0
sentiment.loc[-1] = 0

fig, ax = plt.subplots(figsize=(8, 8))
counts = sentiment
sns.barplot(x=counts.index, y=counts, ax=ax, color = 'b')
ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_ylabel("Percentage")
ax.set_title('Overall Sentiment Distribution')
plt.savefig(outputfilepath + '/sentdistro.png')

# because the sentiments are all positive, let's take a look at how positive
mostpos = ind.sort_values('pos', ascending = False).head(10)
leastpos = ind.sort_values('pos', ascending = False).tail(10)
# see jd samples of the most and least positive

# bar plot of city by average pos sentiment
city = ind.groupby(['city'])['compound'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(4, 8))
counts = city
sns.barplot(x=counts, y=counts.index, ax=ax, color='b')
# ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("City")
ax.set_title('Distribution of Sentiment Across City')
#plt.xticks(rotation=90)
plt.savefig(outputfilepath + '/city.png',bbox_inches='tight')


# bar plot of state by average pos sentiment
state = ind.groupby(['state'])['compound'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(4, 8))
counts = state
sns.barplot(x=counts, y=counts.index, ax=ax, color='b')
# ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("State")
ax.set_title('Distribution of Sentiment Across State')
#plt.xticks(rotation=90)
plt.savefig(outputfilepath + '/state.png',bbox_inches='tight')


# bar plot of industry by average pos sentiment
industry = ind.groupby(['industry'])['compound'].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(8, 8))
counts = industry
sns.barplot(x=counts, y=counts.index, ax=ax, color='b')
# ax.set_xticklabels(['Negative', 'Neutral', 'Positive'])
ax.set_xlabel("Sentiment Score")
ax.set_ylabel("Industry")
ax.set_title('Distribution of Sentiment Across Industry')
#plt.xticks(rotation=90)
plt.savefig(outputfilepath + '/industry.png',bbox_inches='tight')