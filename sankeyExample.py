import pandas as pd
import sankey as sk
import json
from collections import Counter
pd.options.mode.chained_assignment = None

def single_sankey(frame, src, targ, mincount=20):
    """Condense dataframe to contain only specified artist traits for sankey diagram with 1 source and 1 target"""

    # Create dictionary with counts of each artist featuring the combination of given source and target traits
    sankeydict = {}
    i = 0
    for item1 in list(set(frame[src])):
        for item2 in list(set(frame[targ])):
            sankeydict[i] = [item1, item2, list(frame[frame[src] == item1][targ]).count(item2)]
            i += 1

    # Create dataframe from artist-trait count dictionary
    sankeydf = pd.DataFrame.from_dict(sankeydict, orient='index', columns=['Source', 'Target', 'Count'])

    # Filter out rows with an artist count below desired quantity
    sankeydf = sankeydf[sankeydf['Count'] > mincount]

    return sankeydf

def artist_sankey(frame, *args):
    """ Create and show sankey diagram consisting of either 1 or 2 source-target pairs"""

    if len(args) == 2:

        # Create dataframe for single source-target pair sankey diagram to be made from
        sankeydf = single_sankey(frame, args[0], args[1])

    elif len(args) == 3:
        # Create dataframes for each individual source-target pair
        df1 = single_sankey(frame, args[0], args[1])
        df2 = single_sankey(frame, args[1], args[2])

        # Combine dataframes for double source-target sankey diagram to be made from
        sankeydf = pd.concat([df1, df2])

    # Create and show desired sankey diagram
    sk.make_sankey(sankeydf, 'Source', 'Target', vals='Count')

def main():
    ## Clean up data
    # Open Artists.json file and load data into dictionary
    with open('Artists.json') as infile:
        df_dict = json.load(infile)

    # Create DataFrame from artist data dictionary
    df = pd.DataFrame.from_dict(df_dict)

    # Condense DataFrame into columns with only nationality, gender, and birth decade data
    for each in list(df.columns):
        if each not in ['Nationality', 'Gender', 'BeginDate']:
            df.drop(each, axis=1, inplace=True)

    # Relabel each artist's birth year as the first year of that decade (ex: 1945 becomes 1940)
    dec_list = []
    df.rename(columns={'BeginDate': 'BirthDecade'}, inplace=True)
    for index, artist in df.iterrows():
        decade = list(str(artist['BirthDecade']))
        decade[-1] = '0'
        dec_list.append(int(''.join(decade)))
    df['BirthDecade'] = dec_list

    # Filter out rows with unknown birth decade
    df = df[df['BirthDecade'] != 0]

    # Replace null gender descriptors as 'Gender unknown'
    df['Gender'].fillna('Gender unknown', inplace=True)

    ## Create 3 desired single source-target sankey diagrams and 1 double source-target pair sankey diagram
    artist_sankey(df, 'Nationality', 'BirthDecade')
    artist_sankey(df, 'Nationality', 'Gender')
    artist_sankey(df, 'Gender', 'BirthDecade')
    artist_sankey(df, 'Nationality', 'Gender', 'BirthDecade')

if __name__ == '__main__':
    main()