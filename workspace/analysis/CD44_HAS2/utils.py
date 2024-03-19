#!/usr/bin/env jupyter

import pandas as pd
from pathlib import Path


def load_path(path: str or Path):
    return pd.read_parquet(Path(path))


def get_figs_dir():
    figs_dir = Path("../../figs")
    figs_dir.mkdir(exist_ok=True)
    return figs_dir
