import plotly.graph_objects as go

def _code_mapping(df, src, targ):
    """ Maps labels / strings in src and target
    and converts them to integers 0,1,2,3... """

    # Extract distinct labels
    labels = sorted(list(set(list(df[src])))) + list(set(list(df[targ])))

    # define integer codes
    codes = list(range(len(labels)))

    # pair labels with list
    lc_map = dict(zip(labels, codes))

    # in df, substitute codes for labels
    df = df.replace({src: lc_map, targ: lc_map})

    return df, labels

def make_sankey(df, *args, vals=None):
    """Generate the sankey diagram """

    df, labels = _code_mapping(df, args[0], args[1])

    if vals:
        values = df[vals]
    else:
        values = [1] * len(df)

    link = {'source': df[args[0]], 'target': df[args[1]], 'value': values}
    node = {'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()
