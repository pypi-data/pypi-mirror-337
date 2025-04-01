import pytest
import torch
import numpy as np
from ml4h_latentverse.tests.clustering import run_clustering
from ml4h_latentverse.tests.disentanglement import run_disentanglement
from ml4h_latentverse.tests.expressiveness import run_expressiveness
from ml4h_latentverse.tests.robustness import run_robustness
from .test import generate_cluster_data, generate_disentanglement_data, generate_expressiveness_data, generate_robustness_data


########### FIXTURES FOR DATA GENERATION ###########
@pytest.fixture
def cluster_data():
    """Generate data for clustering tests."""
    return {
        "High Clusterability": generate_cluster_data(n_samples=500, var1=0.5, var2=0.5),
        "Low Clusterability": generate_cluster_data(n_samples=500, var1=3.0, var2=3.0),
    }


@pytest.fixture
def disentanglement_data():
    """Generate data for disentanglement tests."""
    return {
        "Fully Disentangled": generate_disentanglement_data(n_samples=500, mode="fully_disentangled"),
        "Partially Disentangled": generate_disentanglement_data(n_samples=500, mode="partially_disentangled"),
        "Fully Entangled": generate_disentanglement_data(n_samples=500, mode="fully_entangled"),
    }


@pytest.fixture
def expressiveness_data():
    """Generate data for expressiveness tests."""
    return {
        "High Expressiveness": generate_expressiveness_data(mode="high"),
        "Low Expressiveness": generate_expressiveness_data(mode="low"),
    }


@pytest.fixture
def robustness_data():
    """Generate data for robustness tests."""
    return {
        "Sensitive Data": generate_robustness_data(mode="sensitive"),
        "Less Sensitive Data": generate_robustness_data(mode="less_sensitive"),
    }


########### TESTS ###########

def test_clusterability(cluster_data):
    """Test clustering quality under different conditions."""
    for name, (data, labels) in cluster_data.items():
        results = run_clustering(data, labels, num_clusters=2)

        assert "results" in results, f"Clustering test failed: No 'results' in output for {name}"
        
        assert results["results"]["Normalized Mutual Information"] > 0.5 if name == "High Clusterability" else True, \
            f"NMI too low for {name}: {results['results']['Normalized Mutual Information']:.4f}"
        
        assert results["results"]["Silhouette Score"] > 0.5 if name == "High Clusterability" else True, \
            f"Silhouette Score too low for {name}: {results['results']['Silhouette Score']:.4f}"
        
        assert results["results"]["Davies-Bouldin Index"] < 1.0 if name == "High Clusterability" else True, \
            f"Davies-Bouldin Index too high for {name}: {results['results']['Davies-Bouldin Index']:.4f}"
        
        assert results["results"]["Cluster Learnability"] > 0.8 if name == "High Clusterability" else True, \
            f"Cluster Learnability too low for {name}: {results['results']['Cluster Learnability']:.4f}"


def test_disentanglement(disentanglement_data):
    """Test disentanglement quality under different conditions."""
    for name, (data, labels) in disentanglement_data.items():
        results = run_disentanglement(data, labels)

        assert "DCI" in results, f"Disentanglement test failed: No 'DCI' in output for {name}"

        assert results["DCI"]["Disentanglement"] > 0.7 if name == "Fully Disentangled" else True, \
            f"DCI Disentanglement too low for {name}: {results['DCI']['Disentanglement']:.4f}"

        assert results["MIG"] > 0.5 if name == "Fully Disentangled" else True, \
            f"MIG Score too low for {name}: {results['MIG']:.4f}"

        assert results["TC"] < 0.5 if name == "Fully Disentangled" else True, \
            f"Total Correlation too high for {name}: {results['TC']:.4f}"

        assert results["DCI"]["Informativeness"] > 0.7 if name == "Fully Disentangled" else True, \
            f"SAP Score too low for {name}: {results['DCI']['Informativeness']:.4f}"


def test_expressiveness(expressiveness_data):
    """Test expressiveness metric behavior."""
    for name, (data, labels) in expressiveness_data.items():
        results = run_expressiveness(data, labels, percent_to_remove_list=[10, 20, 30, 40, 50], plots=False)

        assert "metrics" in results, f"Expressiveness test failed: No 'metrics' in output for {name}"
        assert len(results["metrics"]) > 0, f"Expressiveness results are empty for {name}"


@pytest.mark.parametrize("metric", ["clustering", "probing"])
def test_robustness(robustness_data, metric):
    """
    Test robustness metric behavior with noise for both clustering and probing.
    Ensures that sensitive data degrades faster than less sensitive data.
    """
    noise_levels = [0.1, 0.2, 0.3, 0.4, 0.5]
    
    for name, (data, labels) in robustness_data.items():
        results = run_robustness(data, labels, noise_levels=noise_levels, metric=metric, plots=False)

        # Ensure results contain metrics
        assert "metrics" in results, f"Robustness test failed: No 'metrics' in output for {name} using {metric}"
        assert len(results["metrics"]) > 0, f"Robustness results are empty for {name} using {metric}"

        # Check that expected metrics exist
        expected_metrics = ["Silhouette Score", "Davies-Bouldin Index", "Normalized Mutual Information", "Cluster Learnability"]
        if metric == "probing":
            expected_metrics = ["Model Complexity", "AUROC", "Accuracy", "R²"]
        
        for key in expected_metrics:
            assert key in results["metrics"], f"Missing expected metric '{key}' in {name} using {metric}"

        # Ensure values degrade correctly for sensitive data
        if name == "Sensitive Data":
            if metric == "clustering":
                assert results["metrics"]["Silhouette Score"][0] > results["metrics"]["Silhouette Score"][-1], \
                    f"Silhouette Score did not decrease as expected for {name} using {metric}"
                
                assert results["metrics"]["Davies-Bouldin Index"][0] < results["metrics"]["Davies-Bouldin Index"][-1], \
                    f"Davies-Bouldin Index did not increase as expected for {name} using {metric}"
                
                assert results["metrics"]["Normalized Mutual Information"][0] > results["metrics"]["Normalized Mutual Information"][-1], \
                    f"NMI did not decrease as expected for {name} using {metric}"
                
                assert results["metrics"]["Cluster Learnability"][0] > results["metrics"]["Cluster Learnability"][-1], \
                    f"Cluster Learnability did not decrease as expected for {name} using {metric}"

            elif metric == "probing":
                assert results["metrics"]["Accuracy"][0] > results["metrics"]["Accuracy"][-1], \
                    f"Accuracy did not decrease as expected for {name} using {metric}"
                
                assert results["metrics"]["AUROC"][0] > results["metrics"]["AUROC"][-1], \
                    f"AUROC did not decrease as expected for {name} using {metric}"
                
                if "R²" in results["metrics"]:  # Only applicable for regression
                    assert results["metrics"]["R²"][0] > results["metrics"]["R²"][-1], \
                        f"R² did not decrease as expected for {name} using {metric}"

        # Ensure less sensitive data is more stable
        if name == "Less Sensitive Data":
            if metric == "clustering":
                assert results["metrics"]["Silhouette Score"][-1] >= results["metrics"]["Silhouette Score"][0] * 0.8, \
                    f"Silhouette Score decreased too much for {name} using {metric}"
                
                assert results["metrics"]["Davies-Bouldin Index"][-1] <= results["metrics"]["Davies-Bouldin Index"][0] * 1.2, \
                    f"Davies-Bouldin Index increased too much for {name} using {metric}"

            elif metric == "probing":
                assert results["metrics"]["Accuracy"][-1] >= results["metrics"]["Accuracy"][0] * 0.8, \
                    f"Accuracy dropped too much for {name} using {metric}"
                
                assert results["metrics"]["AUROC"][-1] >= results["metrics"]["AUROC"][0] * 0.8, \
                    f"AUROC dropped too much for {name} using {metric}"
