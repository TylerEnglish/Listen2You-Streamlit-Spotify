#Import Libraries for Feature plot
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

SPOTIPY_CLIENT_ID = '82c6296b242d475891de0b4248f702f3'
SPOTIPY_CLIENT_SECRET = 'e83cbc3e019e466abb62e0f42e5e38fb'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,)
sp = spotipy.Spotify(auth_manager=auth_manager)

def feature_plot(features):
    

    labels= list(features)[:]
    stats= features.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (18,18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "Features", color= 'gray')
    ax.fill(angles, stats, alpha=0.25, facecolor='gray')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)


    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
    plt.ylim(0,1)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

    st.pyplot(plt)

def feature_plot2(features1,features2):
    
    labels= list(features1)[:]
    stats= features1.mean().tolist()
    stats2 = features2.mean().tolist()

    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats=np.concatenate((stats,[stats[0]]))
    stats2 =np.concatenate((stats2,[stats2[0]])) 
    angles=np.concatenate((angles,[angles[0]]))

    #Size of the figure
    fig=plt.figure(figsize = (18,18))

    ax = fig.add_subplot(221, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2, label = "Features 1", color= 'gray')
    ax.fill(angles, stats, alpha=0.25, facecolor='blue')
    ax.set_thetagrids(angles[0:7] * 180/np.pi, labels , fontsize = 13)

    ax.set_rlabel_position(250)
    plt.yticks([0.2 , 0.4 , 0.6 , 0.8  ], ["0.2",'0.4', "0.6", "0.8"], color="grey", size=12)
    plt.ylim(0,1)

    ax.plot(angles, stats2, 'o-', linewidth=2, label = "Features 2", color = 'm')
    ax.fill(angles, stats2, alpha=0.25, facecolor='m' )
    ax.set_title('Mean Values of the audio features')
    ax.grid(True)

    plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

    st.pyplot(plt)

def get_features(track_id):
    track_features_x = sp.audio_features(track_id)
    dfx = pd.DataFrame(track_features_x, index=[0])
    dfx_features = dfx.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
    return dfx_features