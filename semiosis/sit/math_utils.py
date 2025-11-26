"""
Mathematical utilities for semantic information theory calculations.

This module provides helper functions for token probability extraction,
cross-entropy calculations, and statistical analysis.
"""

from typing import Dict, List, Tuple

import numpy as np
from scipy import stats


def extract_token_probabilities(
    response: str, logprobs_dict: Dict[str, float], default_logprob: float = -10.0
) -> List[Tuple[str, float]]:
    """
    Extract token probabilities for a response from logprobs dictionary.

    Args:
        response: The response string
        logprobs_dict: Dictionary mapping tokens to log probabilities
        default_logprob: Default logprob for tokens not in dictionary

    Returns:
        List of (token, logprob) tuples
    """
    tokens = response.split()
    token_probs = []

    for token in tokens:
        logprob = logprobs_dict.get(token, default_logprob)
        token_probs.append((token, logprob))

    return token_probs


def calculate_cross_entropy(token_logprobs: List[Tuple[str, float]]) -> float:
    """
    Calculate cross-entropy from token log probabilities.

    Args:
        token_logprobs: List of (token, logprob) tuples

    Returns:
        Cross-entropy value
    """
    if not token_logprobs:
        return 0.0

    # Convert log probabilities back to probabilities
    logprobs = [logprob for token, logprob in token_logprobs]

    # Calculate cross-entropy: H(p,q) = -sum(p(x) * log(q(x)))
    # In this case, we're calculating entropy of the distribution:
    # H = -sum(p(x) * log(p(x)))
    # where p(x) represents the probability of each token
    probs = [np.exp(lp) for lp in logprobs]

    # Normalize probabilities to sum to 1
    total_prob = sum(probs)
    if total_prob == 0:
        return 0.0

    probs = [p / total_prob for p in probs]

    # Calculate entropy
    entropy = -sum(p * logprob if p > 0 else 0 for p, logprob in zip(probs, logprobs))
    return entropy


def calculate_perplexity(token_logprobs: List[Tuple[str, float]]) -> float:
    """
    Calculate perplexity from token log probabilities.

    Args:
        token_logprobs: List of (token, logprob) tuples

    Returns:
        Perplexity value
    """
    if not token_logprobs:
        return 0.0

    logprobs = [logprob for token, logprob in token_logprobs]
    avg_logprob = sum(logprobs) / len(logprobs)

    # Perplexity = exp(-average_log_probability)
    perplexity = np.exp(-avg_logprob)
    return perplexity


def calculate_kl_divergence(p_logprobs: List[float], q_logprobs: List[float]) -> float:
    """
    Calculate KL divergence between two probability distributions.

    Args:
        p_logprobs: Log probabilities of distribution P
        q_logprobs: Log probabilities of distribution Q

    Returns:
        KL divergence D(P||Q)
    """
    if len(p_logprobs) != len(q_logprobs) or not p_logprobs:
        return 0.0

    # Convert log probabilities to probabilities
    p_probs = [np.exp(lp) for lp in p_logprobs]
    q_probs = [np.exp(lp) for lp in q_logprobs]

    # Normalize
    p_total = sum(p_probs)
    q_total = sum(q_probs)

    if p_total == 0 or q_total == 0:
        return 0.0

    p_probs = [p / p_total for p in p_probs]
    q_probs = [q / q_total for q in q_probs]

    # Calculate KL divergence: D(P||Q) = sum(P(x) * log(P(x)/Q(x)))
    kl_div = 0.0
    for p, q in zip(p_probs, q_probs):
        if p > 0 and q > 0:
            kl_div += p * np.log(p / q)

    return kl_div


def calculate_confidence_interval(
    data: List[float], confidence: float = 0.95
) -> Tuple[float, float]:
    """
    Calculate confidence interval for a set of values.

    Args:
        data: List of values
        confidence: Confidence level (0-1)

    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    if len(data) < 2:
        if data:
            return (data[0], data[0])
        else:
            return (0.0, 0.0)

    mean = np.mean(data)
    std_err = stats.sem(data)
    h = std_err * stats.t.ppf((1 + confidence) / 2, len(data) - 1)

    return (mean - h, mean + h)


def calculate_correlation(x: List[float], y: List[float]) -> float:
    """
    Calculate Pearson correlation coefficient between two series.

    Args:
        x: First series
        y: Second series

    Returns:
        Correlation coefficient
    """
    if len(x) != len(y) or len(x) < 2:
        return 0.0

    # Convert to numpy arrays
    x_arr = np.array(x)
    y_arr = np.array(y)

    # Calculate means
    x_mean = np.mean(x_arr)
    y_mean = np.mean(y_arr)

    # Calculate numerator and denominators
    numerator = np.sum((x_arr - x_mean) * (y_arr - y_mean))
    sum_sq_x = np.sum((x_arr - x_mean) ** 2)
    sum_sq_y = np.sum((y_arr - y_mean) ** 2)

    if sum_sq_x == 0 or sum_sq_y == 0:
        return 0.0

    denominator = np.sqrt(sum_sq_x * sum_sq_y)
    return numerator / denominator


def moving_average(data: List[float], window_size: int) -> List[float]:
    """
    Calculate moving average of a series.

    Args:
        data: Input series
        window_size: Size of the moving window

    Returns:
        List of moving averages
    """
    if len(data) < window_size:
        return [np.mean(data)] if data else []

    result = []
    for i in range(len(data) - window_size + 1):
        window = data[i : i + window_size]
        result.append(np.mean(window))

    return result


def detect_outliers_iqr(data: List[float], factor: float = 1.5) -> List[int]:
    """
    Detect outliers using the interquartile range method.

    Args:
        data: Input data
        factor: IQR multiplier for outlier detection

    Returns:
        List of indices of outliers
    """
    if len(data) < 4:
        return []

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1

    lower_bound = q1 - factor * iqr
    upper_bound = q3 + factor * iqr

    outliers = []
    for i, value in enumerate(data):
        if value < lower_bound or value > upper_bound:
            outliers.append(i)

    return outliers
