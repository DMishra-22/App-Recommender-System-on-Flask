# -*- coding: utf-8 -*-
"""RecommenderSystem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FD7UiSpSQYE18KRP-9VHA5HMfyejfrpm
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd

AppleStore = pd.read_csv('AppleStore.csv')
reviews = pd.read_csv('appleStore_description.csv')

Store = pd.merge(AppleStore, reviews, on='id')

Combine_AppleStore_df = Store.drop(columns=['track_name_y', 'size_bytes_y', 'rating_count_ver', 'user_rating_ver', 'vpp_lic', 'currency', 'cont_rating', 'ipadSc_urls.num'])

Combine_AppleStore_df = Combine_AppleStore_df.rename(columns = {'id': 'ID','track_name_x': 'TRACK NAME', 'size_bytes_x':'SIZE',
                                    'rating_count_tot':'TOTAL VOTES', 'user_rating':'RATING', 'ver':'VERSION', 'prime_genre': 'GENRE',  
                                    'sup_devices.num':'DEVICE SUPPORTED', 'lang.num':'LANGUAGE SUPPORTED', 'app_desc':'DESCRIPTION','price': 'PRICE'})

v=Combine_AppleStore_df['TOTAL VOTES']
R=Combine_AppleStore_df['RATING']
C=Combine_AppleStore_df['RATING'].mean()
m=Combine_AppleStore_df['TOTAL VOTES'].quantile(0.70)

Combine_AppleStore_df['WEIGHTED AVERAGE']=((R*v)+ (C*m))/(v+m)

AppleStore_sorted_ranking=Combine_AppleStore_df.sort_values('WEIGHTED AVERAGE',ascending=False)

AppleStore_sorted_ranking1=Combine_AppleStore_df.sort_values('TOTAL VOTES',ascending=False)

from sklearn.preprocessing import MinMaxScaler

scaling=MinMaxScaler()
AppleStore_scaled_df=scaling.fit_transform(Combine_AppleStore_df[['WEIGHTED AVERAGE','TOTAL VOTES']])
AppleStore_normalized_df=pd.DataFrame(Combine_AppleStore_df,columns=['WEIGHTED AVERAGE','TOTAL VOTES'])

Combine_AppleStore_df[['normalized_weight_average','normalized_total_votes']]= AppleStore_normalized_df

Combine_AppleStore_df['SCORE'] = Combine_AppleStore_df['normalized_weight_average'] * 0.5 + Combine_AppleStore_df['normalized_total_votes'] * 0.5
AppleStore_scored_df = Combine_AppleStore_df.sort_values(['SCORE'], ascending=False)

from sklearn.feature_extraction.text import TfidfVectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
Combine_AppleStore_df['DESCRIPTION'] = Combine_AppleStore_df['DESCRIPTION'].fillna('')

tfv_matrix = tfv.fit_transform(Combine_AppleStore_df['DESCRIPTION'])

from sklearn.metrics.pairwise import sigmoid_kernel

# Compute the sigmoid kernel
sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

indices = pd.Series(Combine_AppleStore_df.index, index=Combine_AppleStore_df['TRACK NAME']).drop_duplicates()

def get_rec(title, sig=sig):
    # Get the index corresponding to original_title
    idx = indices[title]

    # Get the pairwsie similarity scores 
    sig_scores = list(enumerate(sig[idx]))

    # Sort the movies 
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

    # Scores of the 10 most similar movies
    sig_scores = sig_scores[1:11]

    # Movie indices
    movie_indices = [i[0] for i in sig_scores]

    # Top 10 most similar movies
    return Combine_AppleStore_df['TRACK NAME'].iloc[movie_indices]