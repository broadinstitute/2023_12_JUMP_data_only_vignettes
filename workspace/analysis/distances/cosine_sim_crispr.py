#!/usr/bin/env jupyter

from itertools import product
from pathlib import Path

from copairs.compute import pairwise_cosine

sfrom crispr import split_parquet

filename = "harmonized_no_sphering_profiles"
dir_path = Path("../../profiles/")
profiles_path = dir_path / f"{filename}.parquet"
dframe_path = dir_path / f"{filename}_pert.parquet"
meta, vals, _ = split_parquet(parquet_path)
n_samples = len(meta)

iterator = product((range(n_samples), range(n_samples)))
cosine_dist = np.zeros((n_samples, n_samples), dtype=np.float32)

a = np.random.random_sample((100, 100))
b = np.random.random_sample((100, 100))
iterator = list( product(range(100),range(100)) )

def pairwise_cosine(x_sample: np.ndarray, y_sample: np.ndarray) -> np.ndarray:
    x_norm = x_sample / np.linalg.norm(x_sample, axis=1)[:, np.newaxis]
    y_norm = y_sample / np.linalg.norm(y_sample, axis=1)[:, np.newaxis]
    c_sim = np.sum(x_norm * y_norm, axis=1)
    return c_sim


def cosine_dist(loc):
    cosine_dist[loc[0], loc[1]] = pairwise_cosine(vals[loc[0]], vals[loc[1]])


cos_sim1 =np.sum((a @ b.T) / (norm(a) * norm(b)), axis=1)
cos_sim2 = pairwise_cosine(a, b)

%timeit np.sum((a @ b.T) / (norm(a) * norm(b)), axis=1)
%timeit dot(a, b)/(norm(a)*norm(b))
%timeit best_candidate(a, b)

p_umap(cosine_dist, iterator)
np.savez("crispr_cos_dist.npz", cosine_dist)
