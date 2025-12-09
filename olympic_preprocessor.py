import pandas as pd

def preprocess(df, region_df):
    # Filter for Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region data
    df = df.merge(region_df, on='NOC', how='left')

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # One-hot encode medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
