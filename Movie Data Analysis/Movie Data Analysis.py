#!/usr/bin/env python
# coding: utf-8

# # TMDB Movie Data Analysis and Visualization
# 
# What can we say about the success of a movie before it is released? <br>
# Are there certain companies (Pixar?) that have found a consistent formula? <br>
# Given that major films costing over $100 million to produce can still flop, 
# this question is more important than ever to the industry. Film aficionados might have different interests. <br>
# Can we predict which films will be highly rated, whether or not they are a commercial success?

# In[2]:


# Importing the required packages here
import numpy as np
import pandas as pd
import seaborn as sns
import ast, json

from datetime import datetime
import matplotlib.pyplot as plt


# In[3]:


# Let's load the dataset and create their dataframes
credits_df = pd.read_csv('tmdb_5000_credits.csv')
movies_df = pd.read_csv('tmdb_5000_movies.csv')


# # Looking at this dataset, we need to define a set of questions.
# 
# Defining the primary questions here:
# 1. Which are the 5 most expensive movies? Comparison between the extremes.
# 2. Top 5 most profitable movies? Comparison between the min and max profits.
# 3. Most talked about Movies?
# 4. Average runtime of movies?
# 5. Movies which are rated above 7 by the critics?
# 6. Which year did we have the most profitable movies?
# 
# Then there will be a set of seconday questions related to the questions above
# 1. Most successful genre.
# 2. Frequent Cast in movies.
# 3. Average budget of the profitable movies.
# 4. Average duration of the most profitable movies.
# 5. Language of the most profitable movies."""

# In[5]:


# merging the two files
movies_df = pd.merge(movies_df,credits_df,left_on='id',right_on='movie_id', how='left', suffixes=('', '_y'))
movies_df.columns


# Data Cleaning Process
# After observing the dataset and proposed questions for the analysis,<br> we will be keeping only relevent data deleting the unsued data so that we can make our calculation easy and understandable.
# 
# Steps to be taken to clean the data:-
# 
# <ul style="list-style-type:disc;">
# <li>We need to remove unused column such as id, imdb_id, vote_count, production_company, keywords, homepage etc.</li>
# <li>Removing the duplicacy in the rows(if any).</li>
# <li>Some movies in the database have zero budget or zero revenue, that is there value has not been recorded so we will be discarding such entries.</li>
# <li>Changing release date column into date format.</li>
#  <li>Replacing zero with NAN in runtime column.</li>
# <li>Changing format of budget and revenue column.</li>
# </ul>   

# In[6]:


# First step is to clean the data and see which are the redundant or unnecessary cols
del_col_list = ['keywords', 'homepage', 'status', 'tagline', 'original_language', 'homepage', 
                'overview', 'production_companies', 'original_title', 'title_y']

movies_df = movies_df.drop(del_col_list, axis=1)


# How to handle the Json in Dataset?
# The main problem with this dataset is the .json format. <br>Many columns in the dataset are in json format, 
# therefore cleaning the dataset was the main challenge. <br>For people who don't know about JSON(JavaScript Object Notation),
# it is basically a syntax for storing and exchanging data between two computers. It is mainly in a key:value format, 
# and is embedded into a string.

# In[7]:


# we see that there are columns which are in json format,
# let's flatten these json data into easyily interpretable lists
def parse_col_json(column, key):
    """
    Args:
        column: string
            name of the column to be processed.
        key: string
            name of the dictionary key which needs to be extracted
    """
    for index,i in zip(movies_df.index,movies_df[column].apply(json.loads)):
        list1=[]
        for j in range(len(i)):
            list1.append((i[j][key]))# the key 'name' contains the name of the genre
        movies_df.loc[index,column]=str(list1)
    
parse_col_json('genres', 'name')
parse_col_json('spoken_languages', 'name')
parse_col_json('cast', 'name')
parse_col_json('production_countries', 'name')


# In[8]:


movies_df.head()


# In[9]:


#  dropping the duplicates from the dataset.
print(movies_df.shape)
movies_df = movies_df.drop_duplicates(keep='first')
print(movies_df.shape)


# In[10]:


# replacing all the zeros from revenue and budget cols.
cols = ['budget', 'revenue']
movies_df[cols] = movies_df[cols].replace(0, np.nan)


# In[11]:


# dropping all the rows with na in the columns mentioned above in the list.
movies_df.dropna(subset=cols, inplace=True)
movies_df.shape


# In[12]:


movies_df.release_date = pd.to_datetime(movies_df['release_date'])


# In[13]:


movies_df['release_year'] = movies_df['release_date'].dt.year


# In[14]:


change_cols=['budget', 'revenue']
#changing data type
movies_df[change_cols]=movies_df[change_cols].applymap(np.int64)
movies_df.dtypes


# In[15]:


# Answer to question #1.
# To find out the most expensive movies, we need to look at the budget set for them which is an indicator of expense.

expensive_movies_df = movies_df.sort_values(by ='budget', ascending=False).head()
expensive_movies_df

# below are the 5 most expensive movies in descending order.


# In[16]:


expensive_movies_df = movies_df.sort_values(by = 'budget', ascending=False).head()
expensive_movies_df


# In[17]:


"""Since we need to compare the minimums and maximums in 3 questions, we can write a generi function to do that for us. 
It will remove all the redundancy in code for such questions."""
def find_min_max_in(col):
    """
    The function takes in a column and returns the top 5
    and bottom 5 movies dataframe in that column.
    
    args:
        col: string - column name
    return:
        info_df: dataframe - final 5 movies dataframe
    """
    
    top = movies_df[col].idxmax()
    top_df = pd.DataFrame(movies_df.loc[top])
    
    bottom = movies_df[col].idxmin()
    bottom_df = pd.DataFrame(movies_df.loc[bottom])
    
    info_df = pd.concat([top_df, bottom_df], axis=1)
    return info_df

find_min_max_in('budget')


# In[18]:


#ans to Q2
# to find the most profitable movies, we need to find who made the most 
# amount after deducting the budget from the revenue generated.
movies_df['profit'] = movies_df['revenue'] - movies_df['budget']
cols = ['budget',
         'profit',
         'revenue',
         'genres',
         'id',
         'popularity',
         'production_countries',
        'release_date',
        'release_year',
         'runtime',
         'spoken_languages',
         'title',
        'cast',
         'vote_average',
         'vote_count']
movies_df = movies_df[cols]
movies_df.sort_values(by = ['profit'], ascending=False).head()


# In[19]:


# Comparison between min and max profits
find_min_max_in('profit')


# In[20]:


# to find the most talked about movies, we can sort the dataframe on the popularity column
popular_movies_df = movies_df.sort_values(by ='budget', ascending=False).head()
popular_movies_df.head()


# In[21]:


# in terms of popularity score
find_min_max_in('popularity')


# In[22]:


# ans to Q3
# in terms of runtime
find_min_max_in('runtime')


# In[23]:


# Average runtime of movies 
movies_df['runtime'].mean()


# In[24]:


# ans to Q4
# movies rated above 7 
movies_df[movies_df['vote_average'] >= 7.0]


# In[25]:


# ans to Q5
# Year we had the most number of profitable movies.
# we'll first have to define a profitable movies

#plotting a histogram of runtime of movies

#giving the figure size(width, height)
plt.figure(figsize=(9,5), dpi = 100)

#On x-axis 
plt.xlabel('Runtime of the Movies', fontsize = 15)
#On y-axis 
plt.ylabel('Nos.of Movies in the Dataset', fontsize=15)
#Name of the graph
plt.title('Runtime of all the movies', fontsize=15)

#giving a histogram plot
plt.hist(movies_df['runtime'], rwidth = 0.9, bins =35)
#displays the plot
plt.show()


# In[26]:


profits_year = movies_df.groupby('release_year')['profit'].sum()

#figure size(width, height)
plt.figure(figsize=(12,6), dpi = 130)

#on x-axis
plt.xlabel('Release Year of Movies in the data set', fontsize = 12)
#on y-axis
plt.ylabel('Profits earned by Movies', fontsize = 12)
#title of the line plot
plt.title('Representing Total Profits earned by all movies Vs Year of their release.')

#plotting the graph
plt.plot(profits_year)

#displaying the line plot
plt.show()


# In[27]:


# Most profitable year from the given dataset.
profits_year.idxmax()


# In[28]:


#selecting the movies having profit $50M or more
profit_data = movies_df[movies_df['profit'] >= 50000000]

#reindexing new data
profit_data.index = range(len(profit_data))

#we will start from 1 instead of 0
profit_data.index = profit_data.index + 1

#printing the changed dataset
profit_data.head(10)


# In[29]:


# ans to secondary Q1
# formatting the data in the genres columns.
profit_data['genres']=profit_data['genres'].str.strip('[]').str.replace(' ','').str.replace("'",'')

profit_data['genres']=profit_data['genres'].str.split(',')

profit_data.head()


# In[30]:


# plt.subplots(figsize=(12,10))
list1=[]

# extending the list of genres to collect all the genres of all the profitable movies
for i in profit_data['genres']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(
    width=0.9,
    color=sns.color_palette('summer_r',10))
ax


# In[31]:


plt.subplots(figsize=(12,10))
list1=[]

# extending the list of genres to collect all the genres of all the profitable movies
for i in profit_data['genres']:
    list1.extend(i)
    
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(
    width=0.9,
    color=sns.color_palette('summer_r',10))

for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values): 
    ax.text(.8, i, v,fontsize=12,color='white',weight='bold')
ax.patches[9].set_facecolor('r')
plt.title('Top Genres')
plt.show()


# In[32]:


"""Most frequent cast
Let's try to find out the most frequent cast in the movies based on which we can tell about the success factor of the cast."""
profit_data['cast']=profit_data['cast'].str.strip('[]').str.replace(' ','').str.replace("'",'')
profit_data['cast']=profit_data['cast'].str.split(',')

plt.subplots(figsize=(12,10))
list1=[]
for i in profit_data['cast']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('summer_r',10))
for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values): 
    ax.text(.8, i, v,fontsize=12,color='white',weight='bold')
ax.patches[9].set_facecolor('r')
plt.title('Top Cast')
plt.show()


# In[33]:


# ans to Q3
profit_data['profit'].mean()
profit_data['revenue'].mean()


# In[34]:


# ans to Q4
profit_data['runtime'].mean()


# In[35]:


# ans to Q5
profit_data['budget'].mean()


# In[36]:


# ans to Q6
profit_data['spoken_languages']=profit_data['spoken_languages'].str.strip('[]').str.replace(' ','').str.replace("'",'')
profit_data['spoken_languages']=profit_data['spoken_languages'].str.split(',')

plt.subplots(figsize=(12,10))
list1=[]
for i in profit_data['spoken_languages']:
    list1.extend(i)
ax = pd.Series(list1).value_counts()[:10].sort_values(ascending=True).plot.barh(width=0.9,color=sns.color_palette('summer_r',10))
for i, v in enumerate(pd.Series(list1).value_counts()[:10].sort_values(ascending=True).values): 
    ax.text(.8, i, v,fontsize=12,color='white',weight='bold')
ax.patches[9].set_facecolor('r')
plt.title('Frequency of language used!')
plt.show()


# <h2> CONCLUSION </h2>
# This was a very interesting data analysis. We came out with some very interesting facts about movies. 
# After this analysis we can conclude following:
# 
# For a Movie to be in successful criteria
# <ul>
#     <li><u>Average Budget</u> must be around <u>63 millon dollar</u></li>
#     <li><u>Average duration</u> of the movie must be <u>114 minutes</u> </li>
#     <li>Any one of these should be in the <u>cast</u> : Samuel Jackson, Robert De Neiro, Morgan Freeman, Bruce Willis </li>
#     <li><u>Genre</u> must be : Action, Adventure, Thriller, Comedy, Drama. </li>
# </ul>
# By doing all this the movie might be one of the hits and hence can earn an average revenue of around 262 million dollar.

# In[ ]:




