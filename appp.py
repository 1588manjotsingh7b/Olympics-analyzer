import streamlit as st
import pandas as pd
import olympic_preprocessor as preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

# Load data
df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

# Preprocess
df = preprocessor.preprocess(df, region_df)

# Sidebar
st.sidebar.title("Olympics Analysis")
st.sidebar.image(
    'https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png'
)

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete wise Analysis')
)

# ---------------------- Medal Tally ----------------------
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"{selected_country} overall performance")
    else:
        st.title(f"{selected_country} performance in {selected_year} Olympics")

    st.table(medal_tally)

# ---------------------- Overall Analysis ----------------------
if user_menu == 'Overall Analysis':

    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    # Nations over time
    nations_over_time = helper.data_over_time(df, 'region')
    st.title("Participating Nations over the years")
    st.plotly_chart(px.line(nations_over_time, x="Edition", y="region"))

    # Events over time
    events_over_time = helper.data_over_time(df, 'Event')
    st.title("Events over the years")
    st.plotly_chart(px.line(events_over_time, x="Edition", y="Event"))

    # Athletes over time
    athlete_over_time = helper.data_over_time(df, 'Name')
    st.title("Athletes over the years")
    st.plotly_chart(px.line(athlete_over_time, x="Edition", y="Name"))

    # Heatmap of events
    st.title("No. of Events over time (Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count')
        .fillna(0)
        .astype(int),
        annot=True
    )
    st.pyplot(fig)

    # Most successful athletes
    st.title("Most Successful Athletes")
    sport_list = ['Overall'] + sorted(df['Sport'].unique().tolist())
    selected_sport = st.selectbox('Select a Sport', sport_list)
    st.table(helper.most_successful(df, selected_sport))

# ---------------------- Country-wise Analysis ----------------------
if user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")

    country_list = sorted(df['region'].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    # Medal tally line chart
    country_df = helper.yearwise_medal_tally(df, selected_country)
    st.title(f"{selected_country} Medal Tally over the years")
    st.plotly_chart(px.line(country_df, x="Year", y="Medal"))

    # Heatmap
    st.title(f"{selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(pt, annot=True, ax=ax)
    st.pyplot(fig)

    # Top athletes
    st.title(f"Top 10 athletes of {selected_country}")
    st.table(helper.most_successful_countrywise(df, selected_country))

# ---------------------- Athlete-wise Analysis ----------------------
if user_menu == 'Athlete wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
        [x1, x2, x3, x4],
        ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
        show_hist=False,
        show_rug=False
    )
    fig.update_layout(width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    # Age distribution per sport
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming',
        'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions', 'Handball',
        'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey', 'Rowing', 'Fencing',
        'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
        'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
        'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
        'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(width=1000, height=600)
    st.title("Age Distribution by Sport (Gold Medalists)")
    st.plotly_chart(fig)

    # Height vs Weight
    sport_list = ['Overall'] + sorted(df['Sport'].unique().tolist())
    st.title("Height vs Weight")
    selected_sport = st.selectbox("Select a Sport", sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'],
                    style=temp_df['Sex'], s=60, ax=ax)
    st.pyplot(fig)

    # Men vs Women
    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)
