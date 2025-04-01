import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from ml4h_latentverse.tests.probing import run_probing
from ml4h_latentverse.tests.clustering import run_clustering
import os

PLOTS_DIR = "static/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

def extract_numeric(val):
    """
    Recursively extract a numeric value from a nested value.
    If extraction fails, returns np.nan.
    """
    if isinstance(val, (list, np.ndarray)):
        if len(val) == 0:
            return np.nan
        return extract_numeric(val[0])
    try:
        return float(val)
    except Exception:
        return np.nan

def run_robustness(representations, labels, noise_levels, metric="clustering", plots=True):
    """
    Evaluates robustness of a learned representation by adding noise and measuring 
    clustering or probing performance.
    
    Parameters:
      - representations: (N, D) matrix (or DataFrame) of latent representations.
      - labels: (N,) array (or DataFrame) of target labels.
      - noise_levels: List of noise magnitudes to apply.
      - metric: "clustering" or "probing".
      - plots: If True, generate a performance plot.
    
    Returns:
      - A dictionary with "metrics" (mapping each metric name to a list of scores across noise levels)
        and "plot_url" (path to the saved plot, if any).
    """
    if isinstance(labels, pd.DataFrame):
        labels = labels.to_numpy().reshape(-1)
    labels = np.asarray(labels).reshape(-1)
    
    mask = ~np.isnan(labels)
    labels = labels[mask]
    
    if isinstance(representations, pd.DataFrame):
        representations = representations.to_numpy()
    representations = np.asarray(representations)
    
    min_samples = min(len(labels), representations.shape[0])
    labels = labels[:min_samples]
    representations = representations[:min_samples, :]
    representations = representations[mask, :]
    
    noisy_scores = {}
    
    for noise_level in noise_levels:
        noisy_representations = representations + noise_level * np.random.normal(size=representations.shape)

        results = {}
        try:
            if metric == "clustering":
                res = run_clustering(representations=noisy_representations, labels=labels)
                results = res.get("results", {})
            elif metric == "probing":
                res = run_probing(representations=noisy_representations, labels=labels)
                results = res.get("metrics", {})
            else:
                results = {}
        except Exception as e:
            print(f"Error at noise level {noise_level}: {e}")
            results = {}
        
        for key, value in results.items():
            if key not in noisy_scores:
                noisy_scores[key] = []
            noisy_scores[key].append(extract_numeric(value))
        
    plot_url = None
    if plots:
        plt.figure(figsize=(8, 6))
        for key, values in noisy_scores.items():
            if values and all(np.isfinite(v) for v in values):
                plt.plot(noise_levels, values, marker="o", label=key)
            else:
                print(f"Skipping {key} due to non-numeric values: {values}")
        plt.xlabel("Noise Level", fontsize=14)
        plt.ylabel("Performance Score", fontsize=14)
        plt.title(f"Representation Robustness ({metric.capitalize()})", fontsize=16)
        plt.legend()
        plt.grid()
        plot_filename = f"robustness_{metric}.png"
        plot_filepath = os.path.join(PLOTS_DIR, plot_filename)
        plt.savefig(plot_filepath, format="png", dpi=300)
        plt.close()
        if os.path.exists(plot_filepath):
            plot_url = f"/static/plots/{plot_filename}"
    return {"metrics": noisy_scores, "plot_url": plot_url}
