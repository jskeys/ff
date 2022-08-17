#!/usr/bin/env python3

import pandas as pd

from urllib.request import Request, urlopen

URLS = [
    "https://fantasyfootballcalculator.com/rankings/qb",
    "https://fantasyfootballcalculator.com/rankings/rb",
    "https://fantasyfootballcalculator.com/rankings/wr",
    "https://fantasyfootballcalculator.com/rankings/te",
    "https://fantasyfootballcalculator.com/rankings/defense",
]


def create_dataframe_from_url(url):

    r = Request(url, headers={"User-Agent": "Mozilla"})
    with urlopen(r) as f:
        lines = [str(line) for line in f.readlines()]

    starts = []
    stops = []
    for i, line in enumerate(lines):
        if r"<table" in str(line):
            starts.append(i)
        elif r"/table" in str(line):
            stops.append(i)
        else:
            pass

    if len(starts) != len(stops):
        raise RuntimeError("Unbalanced table tags")

    if len(starts) > 1:
        raise RuntimeError("URL HTML contains more than one table start tag")

    dfs = pd.read_html("\n".join(lines[starts[0] : stops[0]]))

    return dfs[0]


for url in URLS:
    csv_name = url.rsplit("/")[-1] + ".csv"
    create_dataframe_from_url(url).to_csv(csv_name)
    print(f"Wrote {csv_name}")
