import numpy as np
import pandas as pd


def fetch_medal_tally(df, year, country):

    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    flag = 0

    # Apply filters
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    # If country only is selected → group by Year
    if flag == 1:
        x = (temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']]
                    .sum()
                    .sort_values('Year')
                    .reset_index())
    else:
        x = (temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']]
                    .sum()
                    .sort_values('Gold', ascending=False)
                    .reset_index())

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x.astype({'Gold': int, 'Silver': int, 'Bronze': int, 'total': int})


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    country = sorted(df['region'].dropna().unique().tolist())
    country.insert(0, 'Overall')

    return years, country


def data_over_time(df, col):
    temp = (
        df.drop_duplicates(['Year', col])
          .groupby('Year')
          .size()
          .reset_index(name=col)
    )
    
    temp.rename(columns={'Year': 'Edition'}, inplace=True)
    return temp



def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals by athlete name
    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # rename columns explicitly

    # Merge with original df to get sport and region info
    x = medal_counts.head(15).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')

    return x



def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )
    temp_df = temp_df[temp_df['region'] == country]

    return temp_df.groupby('Year')['Medal'].count().reset_index()


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal']).drop_duplicates(
        ['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )
    temp_df = temp_df[temp_df['region'] == country]

    return temp_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0)


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    medal_counts = temp_df['Name'].value_counts().reset_index()
    medal_counts.columns = ['Name', 'Medals']  # rename columns explicitly

    x = medal_counts.head(10).merge(df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return x



def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)

    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
    else:
        temp_df = athlete_df

    # Filter out missing values
    temp_df = temp_df.dropna(subset=['Weight', 'Height'])

    return temp_df




def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year')['Name'].count().reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year')['Name'].count().reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final
