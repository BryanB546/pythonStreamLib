import streamlit as st
import pandas as pd
import numpy as np
import json
import requests
from datetime import date
from PIL import Image

st.set_page_config (
    page_title = "AnimeWatch",
    layout = "wide",
    menu_items = {
        'Get Help': 'https://docs.streamlit.io'
                     '/',
        'Report a bug' : 'https://www.Test.com',
        'About': '# Welcome To AnimeWatch The Place Where We Recommended Which Anime To Watch!'
    }
)
file = open("api_keys.json")
json_file = json.load(file)
api_key = json_file["anime_api"]
st.title("Anime Watch")

add_selectbox = st.sidebar.selectbox(
    "Select a Page",
    ["Homepage","Anime Facts", "Anime Ranking", "Anime Conventions", "Statistics", "About Us", "Survey"]
)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

def displayInfo(response):
    for data in response["data"]:
        expander = st.expander(data["node"]["title"])
        for info in data["node"]:
            val = data["node"][info]
            if info != "id" and info != "title" and (isinstance(val, str) or isinstance(val, int)):
                info_disp = info.replace("_", " ").replace("num", "number of").capitalize()
                val_disp = str(val).replace("_", " ").replace("[Written by MAL Rewrite]", "")
                expander.write(info_disp + " : " + val_disp)
            elif isinstance(val, list):
                expander.write("**" + info.capitalize() + "** : ")
                for member in val:
                    expander.write(member["name"].capitalize())
            elif info != "main_picture" and isinstance(val, dict):
                expander.write("**" + info.replace("_", " ").capitalize() + "** : ")
                for info2 in val:
                    val2 = val[info2]
                    if isinstance(val2, str) or isinstance(val2, int):
                        info_disp = info2.replace("_", " ").capitalize()
                        val_disp = str(val2).replace("_", " ").capitalize()
                        expander.write(info_disp + " : " + val_disp)
                    elif isinstance(val2, list):
                        expander.write(info2.capitalize() + " : " + ", ".join(val2))
        expander.image(data["node"]["main_picture"]["large"])

# Anime Facts Page
if add_selectbox == "Anime Facts":
    st.subheader("Search for information pertaining to an anime using the search bar below.")
    local_css("style.css")
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

    icon("search")
    selected = st.text_input("Enter an Anime Title:")
    button_clicked = st.button("IKUZO!")
    url = "https://api.myanimelist.net/v2/anime?q="+ selected +"&fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
    Headers = {"X-MAL-CLIENT-ID": api_key}
    response = requests.get(url, headers=Headers).json()
    if not("error" in response.keys()):
        displayInfo(response)
    elif selected != "":
        st.error('Please enter a longer name')

elif add_selectbox == "Anime Ranking":
    ranking_selectbox = st.sidebar.selectbox(
        "Ranking Type",
        ["All", "Airing", "Upcoming", "TV", "OVA", "Movie", "Special", "By Popularity", "Favorite"]
    )
    url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=" + ranking_selectbox.lower().replace(" ", "")
    Headers = {"X-MAL-CLIENT-ID": api_key}
    response = requests.get(url, headers=Headers).json()

    displayInfo(response)

# Anime Conventions Page
elif add_selectbox == "Anime Conventions":
    st.subheader("Conventions:")
    convention_map = st.checkbox("Click here for the names and dates of each convention located in Florida!")
    if convention_map:
        # Locations Of Anime Conventions by Name Date and Location that they'll be available
        st.write("Nakamacon 2022 November 18-20, 2022	Beachcomber By The Sea Panama City, Beach, FL")
        st.write("A Taste of Iwai 2022	November 20, 2022	Fort Lauderdale Marriott Coral Springs Hotel & Convention Center, Coral Springs, FL")
        st.write("Anime Town Pensacola 2022	December 3-4, 2022	Pensacola Interstate Fair Expo Hall, Pensacola, FL")
        st.write("Holiday Cosplay Tampa Bay 2022	December 10-11, 2022	Tampa Convention Center, Tampa, FL")
        st.write("Holiday Matsuri 2022	December 16-18, 2022	Orlando World Center Marriott, Orlando, FL")
        st.write("OtakuFest 2023	January 13-15, 2023	Miami Airport Convention Center, Miami, FL")
        st.write("SWFL-AnimeExpo 2023	February 12, 2023	Crowne Plaza Fort Myers at Bell Tower Shops, Fort Myers, FL")
        st.write("Pensacon 2023	February 24-26, 2023	Pensacola Bay Center, Pensacola, FL")
        st.write("Colossalcon Cruise 2023	February 24-27, 2023	Royal Caribbean's Independence of the Seas, Departing from Cape Canaveral, FL")
        st.write("My-Con 2023	March 18, 2023	Avanti Palms Resort and Conference Center, Orlando, FL")
        st.write("MegaCon Orlando 2023	March 30 - April 2, 2023	Orange County Convention Center, Orlando, FL")
        st.write("Mizucon 2023	May 26-28, 2023	Hilton Miami Airport Blue Lagoon, Miami, FL")
        st.write("Anime Iwai 2023	November 10-12, 2023	Fort Lauderdale Marriott Coral Springs Hotel & Convention Center, Coral Springs, FL")

#Locations of Conventions in Florida via map
    map_data = pd.DataFrame(
        np.array([
            [30.221993, -85.889214],
            [26.309751, -80.283117],
            [30.474410, -87.308748],
            [27.941444, -82.456423],
            [28.361179, -81.510704],
            [25.779068, -80.309438],
            [26.551319, -81.868595],
            [30.416366, -87.208964],
            [28.408424, -80.611633],
            [28.458815, -81.470912],
            [28.424807, -81.469610],
            [25.782086, -80.278745],
            [26.309751, -80.283117]]),
        columns=['lat', 'lon'])
    st.map(map_data)
    st.write("Further conventions will be added at a later date!")

# Statistics Page
elif add_selectbox == "Statistics":
    st.subheader("Data:")
    plt.rcParams["figure.figsize"] = [7.50, 7.50]
    plt.rcParams["figure.autolayout"] = True
    headers = ['Name', 'Genre', 'Type', 'Episodes', 'Ratings', 'Views']
    df = pd.read_csv('data.csv', names=headers)
    fd = pd.read_csv('anime.csv', names=headers)
    basic_dataframe = st.checkbox("Interactive Table")
    if basic_dataframe:
        st.dataframe(fd)

# Bar Graph Code
    basic_plots = st.checkbox("Bar Graph")
    if basic_plots:
        st.title("Bar graph representing the amount of views of top 18")
        x = df['Name'].astype(str)
        y = df['Views'].astype(str)
        plt.xticks(rotation=90)
        plt.bar(x, y)
        plt.savefig("mybargraph.png")
        image = Image.open('mybargraph.png')
        st.image(image)

# Graph via ratings
    headers = ['Name', 'Genre', 'Type', 'Episodes', 'Ratings', 'Views']
    ax = pd.read_csv('data.csv', names=headers)
    line_plots = st.checkbox("Line Graph")
    if line_plots:
        ax = df.plot(x='Name', y='Ratings')
        plt.xticks(rotation=90)
        ax.set_ylabel("Ratings")
        st.write(ax)
        plt.savefig("linegraph.png")
        image1 = Image.open("linegraph.png")
        st.image(image1)
        plt.show()

# About us page
elif add_selectbox == "About Us":
    st.header("Creation of AnimeWatch")
    st.subheader("Who are AnimeWatch creators ?")
    txt = st.text('AnimeWatch was created by two individuals named Bryan Bravo and Lisa Shrestha.')
    st.write("goal of anime watch was to provide individuals with a way to search for certain anime")
    st.write("user may want to watch or research. Furthermore, there is a variety of other things such as conventions.")
    st.write(" Aside from the anime's and conventions")
    st.write("provide users with data that illustrates which anime is popular")
    st.write("the amount of users that view said anime.")
    img = st.checkbox("Creators Images")
    if img:
        st.balloons()
        st.image('Bryan.jpg', width=400)
        st.write("Bryan Bravo")
        st.image('Lisa.jpg', width=400)
        st.write("Lisa Shrestha")




elif add_selectbox == "Survey":
    st.subheader("Please Complete the survey provided below!")
    date_started = st.date_input("Date:")
    today = date.today().year
    first_name = st.text_input('Username:')
    last_name = st.text_input('Email:')
    Genre = st.radio('Please Select a Genre:',
                     ["Action", "Adventure", "Comedy", "Drama", "Slice of Life", "Fantasy", "Magic", "Supernatural",
                      "Horror", "Mystery", "Psychological", "Romance", "Sci-Fi"])

    subgenre = st.multiselect("Please Choose your favorite Subgenre's: ",
                              ["Game", "Ecchi", "Demons", "Harem", "Josei", "Martial Arts", "Historical", "Military",
                               "Seinen", "Shoujo", "Tragedy", "Sport", "Shounen"])
    st.write("You Selected", len(subgenre), 'Subgenres')

    if first_name and last_name and Genre and subgenre and date_started:
        st.write("Hi, ", first_name, "! You have selected", subgenre, " as subgenre's and", Genre, "for genre.")
        st.write("To confirm selection please press the button below to submit the survey!")
        button = st.button("Submit")
        if button:
            st.success("Survey has been submitted!")
            st.image("Thanks.gif")
            st.write("We look forward to reading your submission.")




else:
    st.header("Where We Provide an array of Anime's to watch and search!")
    st.subheader("What is AnimeWatch ?")
    txt = st.text('AnimeWatch is a website dedicated for the general and anime enthusiasts where you can find'
                  ' which anime the user would like to watch')

    st.subheader("Features we provide")
    st.text('We provide features such as Anime summaries, conventions, charts, etc. All of these features can be found on the sidebar'
            '. Users have the option of selecting which page they desire to explore.')
    st.write("Below is an example of such a feature the page Anime Facts provided for the Anime Naruto")
    st.image("Search.png")

# Animation for turkey on screen!.
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

# Load Animation
animation_symbol = "🦃"

st.markdown(
    f"""
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    <div class="snowflake">{animation_symbol}</div>
    """,
    unsafe_allow_html=True,
)
