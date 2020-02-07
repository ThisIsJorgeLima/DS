
""" **Part 1 - Load and Validate the Data**
*  Load the data as a pandas data frame.
*  Validate that it has the appropriate number of observations (checking the raw file, and also read the dataset description from Kaggle.com [Spotify](https://www.kaggle.com/tomigelo/spotify-audio-features) ).
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from sklearn.neighbors import KNeighborsRegressor
import re
import sys
import time
import pandas
import numpy as np
import pandas as pd
import scipy.stats
import seaborn as sb
import matplotlib as mpl
import matplotlib.pyplot as plt
# import Evaluation as Evaluation
# import Recommenders as Recommenders
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
# from sklearn.cross_validation import train_test_split

sb.set(color_codes=True)
sb.set_palette("muted")
pd.set_option('display.float_format', lambda x: '%.3f' % x)
np.random.seed(sum(map(ord, "regression")))

# If you're on Colab:
# Read data
if 'google.colab' in sys.modules:
    df = 'https://raw.githubusercontent.com/ThisIsJorgeLima/Spotify/master/SpotifyAudioFeaturesApril2019.csv'


# If you're working locally:
# else:
DATA_PATH = '../data/'

df = pd.read_csv(df)
# check data shape
assert df.shape == (130663, 17)

print('df: ', df.shape[0], 'Rows', df.shape[1], 'Features')

df.head(3)

df.tail(3)

""" **Part II - Data Exploration**"""

df.dtypes
"""
Here we can see the breakdown of the count, mean, std, min, and percentile by 25%,50%,75%
"""
df.describe()

# A great way to get an overview of our data:
df.info()

# Checking to see if they're are any duplicate track id's:
df['artist_name']

# more indepth evaluation:
titles = df['track_name'].value_counts().iloc[0:4].keys()
df[df['track_name'].isin(titles)]

# By doing the value counts. In this specific column 'popularity'
# The breakdown from acceding to descending
df.popularity.value_counts()

# nulls as missing values.
# We'll subset our data by choosing ALL the rows that have missing values.

print('The number of rows with Missing Values are: ')
df.isnull().any(axis=1).sum()


def DuplicatedFunction(data, column):
    result = data[column].duplicated().sum()
    return result


print('Duplicate Values:', DuplicatedFunction(df, 'track_id'))
print('Duplicate Values:', DuplicatedFunction(df, 'artist_name'))

df = df.drop_duplicates(keep="first").reset_index(drop=True)
print(df.shape)
df.head()

# double checking to see if all duplicates were removed.
# Everything seems to be at 130663:
df.info()

SpeechinessMusic = df[['instrumentalness', 'speechiness']]
Energetic = df[['danceability', 'energy']]
MusicAttribute = df[['tempo', 'mode', 'key', 'time_signature']]
Environment = df[['acousticness', 'liveness', 'loudness']]

print(SpeechinessMusic.head(2))
print(Energetic.head(2))
print(MusicAttribute.head(2))
print(Environment.head(2))

df.describe()

df.describe(include='O')

df = df.dropna(axis=0, how='any')

song_grouped = df.groupby(['track_name']).agg({'popularity': 'count'}).reset_index()
grouped_sum = song_grouped['popularity'].sum()
song_grouped['tempo'] = song_grouped['popularity'].div(grouped_sum)*100
song_grouped.sort_values(['popularity', 'track_name'], ascending=[0, 1])

songs = df['track_name'].unique()

train_data, test_data = train_test_split(df, test_size=0.20, random_state=0)
print(train_data.head(5))

train_data, test_data = train_test_split(df, test_size=0.20, random_state=0)

df[df['artist_name'] == 'Coldplay']

""" **Part III - Visualizations** """

x = "tempo"
y = "valence"

plt.style.use('fivethirtyeight')

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=False, sharex=False, figsize=(10, 5))
fig.suptitle("Histograms")
h = ax2.hist2d(df[x], df[y], bins=20)
ax1.hist(df["energy"])

ax2.set_xlabel(x)
ax2.set_ylabel(y)

ax1.set_xlabel("energy")

plt.colorbar(h[3], ax=ax2)

plt.show()

# Setting FiveThirtyEight style
plt.style.use('fivethirtyeight')

f, ax = plt.subplots(figsize=(15, 15))  # the size of the heat map
# annot: values, fmt: decimal points of values
sns.heatmap(df.corr(), annot=True, fmt='.2g', cmap='Greens', ax=ax)
sns.set(font_scale=0.75)  # the font size of the value in the heat map
plt.xlabel('Features')
plt.show()

df.columns

# Subplot of scatterplots
plt.style.use('fivethirtyeight')

splot = df[['acousticness', 'danceability',
            'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness',
            'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'popularity']]

ax1 = plt.figure()
sns.pairplot(splot)
plt.title("Pairplot of Song Attributes", size=15)
plt.show("Pairplot of Song Attributes")

train.describe(exclude='number').T.sort_values(by='unique')

features = ['acousticness', 'danceability',
            'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness',
            'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'popularity']

target = 'artist_name'

model = KNeighborsRegressor(n_neighbors=2)

model.fit(train[features], train[target])
plt.style.use('fivethirtyeight')

plt.figure(figsize=(10, 10))
wordcloud = WordCloud(max_font_size=500, max_words=1000, background_color="white",
                      width=2000,
                      height=1000).generate(" ".join(df['artist_name']))

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

# Sub-setting dataframe
Release_Date_Success = df2[['Won', 'q1_release',	'q2_release',	'q3_release',	'q4_release']]
y = Release_Date_Success[(Release_Date_Success['Won'] == 1)]
sns.set_context('paper')  # Everything is smaller
plt.style.use('fivethirtyeight')

fig, (ax1, ax2, ax3, ax4) = plt.subplots(figsize=(10, 7), ncols=4, sharey=True)
sns.set(style="darkgrid")
sns.countplot(x="q1_release", data=y, ax=ax1)
sns.countplot(x="q2_release", data=y, ax=ax2)
sns.countplot(x="q3_release", data=y, ax=ax3)
sns.countplot(x="q4_release", data=y, ax=ax4)

plt.show()

ax = sns.countplot

df['artist_name']
