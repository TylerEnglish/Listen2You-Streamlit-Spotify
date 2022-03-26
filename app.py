from numpy import append
import streamlit as st
import pandas as pd

#Connecting to spotify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


import polarplot
import songrecommandation

SPOTIPY_CLIENT_ID = '82c6296b242d475891de0b4248f702f3'
SPOTIPY_CLIENT_SECRET = 'e83cbc3e019e466abb62e0f42e5e38fb'

auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.header('Listen 2 You')

search_choices = ['Song/Track', 'Artist', 'Album']
search_selected = st.sidebar.selectbox("Your search choice please", search_choices)


search_keyword = st.text_input(" (Keyword Search)")
button_clicked = st.button("Search")

if search_selected == 'Song/Track':        
    search_keyword2 = st.text_input(" (Keyword Search 2)")
    button_clicked2 = st.button("Search 2")
    search_results2 = []
    selected_track = None
    selected_track2 = None


search_results = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    if search_selected == 'Song/Track':

        st.write("Start song/track search for person 1")
        tracks = sp.search(q='track:'+search_keyword,type='track', limit=20)

        tracks_list = tracks['tracks']['items']
        if len(tracks_list) > 0:
            for track in tracks_list:
                # st.write(track['name'] + " - By - " + track['artists'][0]['name'])
                search_results.append(track['name'] + " - By - " + track['artists'][0]['name'])
        if search_selected == 'Song/Track':
            selected_track = st.selectbox("Select your Song/Track: ", search_results)

        st.write("Start song/track search for person 2")
        tracks2 = sp.search(q='track:'+search_keyword2,type='track', limit=20)

        tracks_list2 = tracks2['tracks']['items']
        if len(tracks_list2) > 0:
            for track in tracks_list2:
                # st.write(track['name'] + " - By - " + track['artists'][0]['name'])
                search_results2.append(track['name'] + " - By - " + track['artists'][0]['name'])
        if search_selected == 'Song/Track':
            selected_track2 = st.selectbox("Select your Song/Track: ", search_results2)
        
        

    elif search_selected == 'Artist':
        st.write("Start artist search")
        artists = sp.search(q='artist:'+search_keyword,type='artist', limit=20)

        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                # st.write(artist['name'] + " - By - " + artist['artists'][0]['name'])
                search_results.append(artist['name'])

    elif search_selected == 'Album':
        st.write("Start album search")
        albums = sp.search(q='album:'+search_keyword,type='album', limit=20)

        albums_list = albums['albums']['items']
        if len(albums_list) > 0:
            for album in albums_list:
                # st.write(album['name'] + " - By - " + album['artists'][0]['name'])
                search_results.append(album['name'] + " - By - " + album['artists'][0]['name'])
                
if search_selected == 'Song/Track':
    selected_album = None
    selected_artist = None
else:
    selected_album = None
    selected_artist = None
    selected_track = None
    selected_track2 = None


# if search_selected == 'Song/Track':
#     selected_track = st.selectbox("Select your Song/Track: ", search_results)
#     selected_track2 = st.selectbox("Select your Song/Track: ", search_results2)

if search_selected == 'Artist':
    selected_artist = st.selectbox("Select your Artist: ", search_results)

elif search_selected == 'Album':
    selected_album = st.selectbox("Select your Album: ", search_results)


if selected_track is not None and len(tracks) > 0:
    
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']
                #songrecommandation.save_album_image(img_album, track_id)
    
    tracks_list2 = tracks2['tracks']['items']
    track_id2 = None
    if len(tracks_list2) > 0:
        for track in tracks_list2:
            str_temp2 = track['name'] + " - By - " + track['artists'][0]['name']
            if str_temp2 == selected_track2:
                track_id2 = track['id']
                track_album2 = track['album']['name']
                img_album2 = track['album']['images'][1]['url']
    
    selected_track_choice = None
    selected_track_choice2 = None
    if track_id is not None and track_id2 is not None: 
        # st.write(img_album)
        st.image(img_album)
        st.image(img_album2)
        #mg = songrecommandation.get_album_mage(track_id)
        #image = songrecommandation.get_album_mage(track_id)
        #st.image(img)

        track_choices = ['Song Features', 'Similar Song Recommandation']
        selected_track_choice = st.sidebar.selectbox('Please select track choice: ', track_choices)

        if selected_track_choice == 'Song Features':

            track_feat = sp.audio_features(track_id)
            df = pd.DataFrame(track_feat, index=[0])
            df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            st.dataframe(df_features)


            track_feat2 = sp.audio_features(track_id2)
            df2 = pd.DataFrame(track_feat2, index=[0])
            df_2 = df2.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
            st.dataframe(df_2)
            polarplot.feature_plot2(df_features,df_2)

        elif selected_track_choice == 'Similar Song Recommandation':
            token = songrecommandation.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
            
            similar_songs_json = songrecommandation.get_track_recommendations(track_id, token)
            recommendation_list = similar_songs_json['tracks']
            recommendation_list_df = pd.DataFrame(recommendation_list)
            #st.dataframe(recommendation_list_df)
            recommendation_df = recommendation_list_df[['name','explicit','duration_ms','popularity']]

            

            similar_songs_json2 = songrecommandation.get_track_recommendations(track_id2, token)
            recommendation_list2 = similar_songs_json2['tracks']
            recommendation_list_df2 = pd.DataFrame(recommendation_list2)
            #st.dataframe(recommendation_list_df)
            recommendation_df2 = recommendation_list_df2[['name','explicit','duration_ms','popularity']]

            final_recommendation_list_df = pd.concat([recommendation_df,recommendation_df2], axis=0,join='inner')
            
            final_recommendation_list_df = final_recommendation_list_df.drop_duplicates()
            st.dataframe(final_recommendation_list_df)

            songrecommandation.song_recommendation_vis(final_recommendation_list_df)
            # st.write(track_id)

    else:
        st.write("Please select a track from the list!")

elif selected_artist is not None and len(artists) > 0:
    artists_list = artists['artists']['items']
    artist_id = None
    artist_uri = None
    selected_artist_choice = None
    if len(artists_list) > 0:
        for artist in artists_list:
            if selected_artist == artist['name']:
                artist_id = artist['id']
                artist_uri = artist['uri']
            
    if artist_id is not None:
        artist_choice = ['Albums', 'Top Songs']
        selected_artist_choice = st.sidebar.selectbox('Select artist choice', artist_choice)

    if selected_artist_choice is not None:
        if selected_artist_choice == 'Albums':
            artist_uri = 'spotify:artist:' + artist_id
            album_result = sp.artist_albums(artist_uri, album_type='album')
            all_albums = album_result['items']
            col1,col2,col3 = st.columns((6,4,2))
            for album in all_albums:
                col1.write(album['name'])
                col2.write(album['release_date'])
                col3.write(album['total_tracks'])

        elif selected_artist_choice == 'Top Songs':
            artist_uri = 'spotify:artist:' + artist_id
            top_songs_result = sp.artist_top_tracks(artist_uri)
            for track in top_songs_result['tracks']:
                with st.container():
                    col1,col2,col3,col4 = st.columns((4,4,1,1))
                    col11,col12 = st.columns((8,2))
                    col21, col22 = st.columns((11,1))
                    col31,col32 = st.columns((11,1))
                    col1.write(track['id'])
                    col2.write(track['name'])
                    col3.write(track['duration_ms'])
                    col4.write(track['popularity'])
                    if track['preview_url'] is not None:
                        col11.write(track['preview_url'])
                        with col12:
                            st.audio(track['preview_url'], format="audio/mp3")
                    
                    with col3:
                        def feature_requested():
                            track_feat = sp.audio_features(track['id'])
                            df = pd.DataFrame(track_feat, index=[0])
                            df_features = df.loc[: ,['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']]
                            with col21:
                                st.dataframe(df_features)
                            with col22:
                                polarplot.feature_plot(df_features)

                        feature_button_state = st.button('Track Audio Features', key= track['id'], on_click=feature_requested)
                    with col4:
                        def simular_songs_requested():
                            token = songrecommandation.get_token(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
                            similar_songs_json = songrecommandation.get_track_recommendations(track['id'], token)
                            recommendation_list = similar_songs_json['tracks']
                            recommendation_list_df = pd.DataFrame(recommendation_list)
                            #st.dataframe(recommendation_list_df)
                            recommendation_df = recommendation_list_df[['name','explicit','duration_ms','popularity']]
                            with col21:
                                st.dataframe(recommendation_df)
                            with col22:
                                songrecommandation.song_recommendation_vis(recommendation_df)

                        simular_songs_state = st.button('Simular Songs', key= track['id'], on_click=simular_songs_requested)

                    st.write('------')



elif selected_album is not None and len(albums) > 0:
    albums_list = albums['albums']['items']
    album_id = None
    album_uri = None
    album_name = None
    if len(albums_list) > 0:
        for album in albums_list:
            str_temp = album['name'] + " - By - " + album['artists'][0]['name']
            if selected_album == str_temp:
                album_id = album['id']
                album_uri = album['uri']
                album_name = album['name']

    if album_id is not None and album_uri is not None:
        st.write('Collecting all the tracks for the album: ' + album_name)
        album_tracks = sp.album_tracks(album_id)
        df_album_tracks = pd.DataFrame(album_tracks['items'])
        #st.dataframe(df_album_tracks)
        df_tracks_min = df_album_tracks.loc[:,
                        ['id', 'name','duration_ms','explicit', 'preview_url']]
        # st.dataframe(df_tracks_min)
        
        for i in df_tracks_min.index:
            with st.container():
                col1,col2,col3,col4 = st.columns((4,4,1,1))
                col11,col12 = st.columns((8,2))
                col1.write(df_tracks_min['id'][i])
                col2.write(df_tracks_min['name'][i])
                col3.write(df_tracks_min['duration_ms'][i])
                col4.write(df_tracks_min['explicit'][i])
                if df_tracks_min['preview_url'][i] is not None:
                    col11.write(df_tracks_min['preview_url'][i])
                    with col12:
                        st.audio(df_tracks_min['preview_url'][i], format="audio/mp3")
