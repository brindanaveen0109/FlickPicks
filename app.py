import streamlit as st
import pickle
import os
import zstandard as zstd

# Load Data and Decompress
def decompress_with_zstd(file_path):
    with open(file_path, 'rb') as f:
        compressed_data = f.read()
    # Decompress using Zstandard
    dc = zstd.ZstdDecompressor()
    decompressed_data = dc.decompress(compressed_data)
    # Load the model from the decompressed data
    loaded_model = pickle.loads(decompressed_data)
    return loaded_model

movies_df = decompress_with_zstd('data/pkl_data/movies_df.zstd')
similarity = decompress_with_zstd('data/pkl_data/similarity.zstd')


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:16]
    
    recommended_movies = []
    for movie in movies_list:
        id = movies_df.iloc[movie[0]].movie_id
        recommended_movies.append(movies_df.iloc[movie[0]].title)
    return recommended_movies

# Web App
def main():
    
    # Streamlit Config
    st.set_page_config(page_title="FlickPick", page_icon=":camera:", layout="wide")
    
    # Hide default styles
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"] {visibility: hidden;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    
    # Web Components
    st.title('FlickPick Recommendation System')
    selected_movie = st.selectbox(
        label="Select a movie",
        options=movies_df['title'],
        placeholder = "Choose a movie",
        index=None)

    if st.button('Recommend'): 
        # No movies selected 
        if selected_movie == None:
            st.error("No movies selected. Please select a movie!")
            exit()   
                     
        try:    
            names = recommend(selected_movie)
            print(names)
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.text(names[0])
                
                st.text(names[5])
                
                st.text(names[10])
                
            with col2:
                st.text(names[1])

                st.text(names[6])
                
                st.text(names[11])
                             
            with col3:
                st.text(names[2])
                
                st.text(names[7])
                
                st.text(names[12])
                
            with col4:
                st.text(names[3])
                
                st.text(names[8])
                
                st.text(names[13])
                
            with col5:
                st.text(names[4])
                
                st.text(names[9])
                
                st.text(names[14])
       
        except IndexError:
            st.error("Currently we don't have any information about this movie.")
            
if __name__=="__main__": 
    main()