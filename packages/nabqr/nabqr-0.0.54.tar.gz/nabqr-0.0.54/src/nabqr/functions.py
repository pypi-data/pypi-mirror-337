"""Neural Adaptive Basis Quantile Regression (NABQR) Core Functions

This module provides the core functionality for NABQR.

This module includes:
- Scoring metrics (Variogram, CRPS, QSS)
- Dataset creation and preprocessing
- Model definitions and training
- TAQR (Time-Adaptive Quantile Regression) implementation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import properscoring as ps
import tensorflow as tf
import tensorflow_probability as tfp
import datetime as dt
from .helper_functions import set_n_closest_to_zero
from .functions_for_TAQR import *


def variogram_score_single_observation(x, y, p=0.5):
    """Calculate the Variogram score for a given observation.

    Translated from the R code in Energy and AI paper: 
    "An introduction to multivariate probabilistic forecast evaluation" by Mathias B.B. et al.

    Parameters
    ----------
    x : numpy.ndarray
        Ensemble forecast (m x k), where m is ensemble size, k is forecast horizon
    y : numpy.ndarray
        Actual observations (k,)
    p : float, optional
        Power parameter for the variogram score, by default 0.5

    Returns
    -------
    float
        Variogram score for the observation
    """
    m, k = x.shape
    score = 0

    for i in range(k - 1):
        for j in range(i + 1, k):
            Ediff = (1 / m) * np.sum(np.abs(x[:, i] - x[:, j]) ** p)
            score += (1 / np.abs(i - j)) * (np.abs(y[i] - y[j]) ** p - Ediff) ** 2

    return score / k


def variogram_score_R_multivariate(x, y, p=0.5, t1=12, t2=36):
    """Calculate the Variogram score for all observations for the time horizon t1 to t2.
    Modified from the R code in Energy and AI paper: 
    "An introduction to multivariate probabilistic forecast evaluation" by Mathias B.B. et al.
    Here we use t1 -> t2 as our forecast horizon.
    
    Parameters
    ----------
    x : numpy.ndarray
        Ensemble forecast (m x k)
    y : numpy.ndarray
        Actual observations (k,)
    p : float, optional
        Power parameter, by default 0.5
    t1 : int, optional
        Start hour (inclusive), by default 12
    t2 : int, optional
        End hour (exclusive), by default 36

    Returns
    -------
    tuple
        (score, score_list) Overall score and list of individual scores
    """
    m, k = x.shape
    score = 0
    if m > k:
        x = x.T
        m, k = k, m

    score_list = []
    for start in range(0, k, 24):
        if start + t2 <= k:
            for i in range(start + t1, start + t2 - 1):
                for j in range(i + 1, start + t2):
                    Ediff = (1 / m) * np.sum(np.abs(x[:, i] - x[:, j]) ** p)
                    score += (1 / np.abs(i - j)) * (
                        np.abs(y[i] - y[j]) ** p - Ediff
                    ) ** 2
                score_list.append(score)

    return score / (100_000), score_list


def variogram_score_R_v2(x, y, p=0.5, t1=12, t2=36):
    """
    Calculate the Variogram score for all observations for the time horizon t1 to t2.
    Modified from the paper in Energy and AI, >> An introduction to multivariate probabilistic forecast evaluation <<.
    Assumes that x and y starts from day 0, 00:00.
    

    Parameters:
    x : array
        Ensemble forecast (m x k), where m is the size of the ensemble, and k is the maximal forecast horizon.
    y : array
        Actual observations (k,)
    p : float
        Power parameter for the variogram score.
    t1 : int
        Start of the hour range for comparison (inclusive).
    t2 : int
        End of the hour range for comparison (exclusive).

    Returns:
    --------
    tuple
        (score, score_list) Overall score/100_000 and list of individual VarS contributions
    """

    m, k = x.shape  # Size of ensemble, Maximal forecast horizon
    score = 0
    if m > k:
        x = x.T
        m, k = k, m
    else:
        print("m,k: ", m, k)

    score_list = []
    # Iterate through every 24-hour block
    for start in range(0, k, 24):
        # Ensure we don't exceed the forecast horizon
        if start + t2 <= k:
            for i in range(start + t1, start + t2 - 1):
                for j in range(i + 1, start + t2):
                    Ediff = (1 / m) * np.sum(np.abs(x[:, i] - x[:, j]) ** p)
                    score += (1 / np.abs(i - j)) * (
                        np.abs(y[i] - y[j]) ** p - Ediff
                    ) ** 2
                score_list.append(score)

    # Variogram score
    return score / (100_000), score_list


def calculate_crps(actuals, corrected_ensembles, return_full_scores=False):
    """Calculate the Continuous Ranked Probability Score (CRPS) using the properscoring package.
    If the ensembles do not have the correct dimensions, we transpose them.

    Parameters
    ----------
    actuals : numpy.ndarray
        Actual observations
    corrected_ensembles : numpy.ndarray
        Ensemble forecasts

    Returns
    -------
    float
        Mean CRPS score
    """
    if return_full_scores:
        try:
            crps = ps.crps_ensemble(actuals, corrected_ensembles)
            return crps
        except:
            crps = (ps.crps_ensemble(actuals, corrected_ensembles.T))
            return crps
    else:
        try:
            crps = ps.crps_ensemble(actuals, corrected_ensembles)
            return np.mean(crps)
        except:
            crps = np.mean(ps.crps_ensemble(actuals, corrected_ensembles.T))
            return crps



def calculate_qss(actuals, taqr_results, quantiles):
    """Calculate the Quantile Skill Score (QSS).

    Parameters
    ----------
    actuals : numpy.ndarray
        Actual observations
    taqr_results : numpy.ndarray
        TAQR ensemble forecasts
    quantiles : array-like
        Quantile levels to evaluate

    Returns
    -------
    float
        Quantile Skill Score
    """
    qss_scores = multi_quantile_skill_score(actuals, taqr_results, quantiles)
    # table = pd.DataFrame({
    #     "Quantiles": quantiles,
    #     "QSS NABQR": qss_scores
    # })
    # print(table)
    return np.mean(qss_scores)


def multi_quantile_skill_score(y_true, y_pred, quantiles):
    """Calculate the Quantile Skill Score (QSS) for multiple quantile forecasts.

    Parameters
    ----------
    y_true : numpy.ndarray
        True observed values
    y_pred : numpy.ndarray
        Predicted quantile values
    quantiles : list
        Quantile levels between 0 and 1

    Returns
    -------
    numpy.ndarray
        QSS for each quantile forecast
    """
    y_pred = np.array(y_pred)

    if y_pred.shape[0] > y_pred.shape[1]:
        y_pred = y_pred.T

    assert all(0 <= q <= 1 for q in quantiles), "All quantiles must be between 0 and 1"
    assert len(quantiles) == len(
        y_pred
    ), "Number of quantiles must match inner dimension of y_pred"

    N = len(y_true)
    scores = np.zeros(len(quantiles))

    for i, q in enumerate(quantiles):
        E = y_true - y_pred[i]
        scores[i] = np.sum(np.where(E > 0, q * E, (1 - q) * -E))

    return scores / N


def reliability_func(
    quantile_forecasts,
    corrected_ensembles,
    ensembles,
    actuals,
    corrected_taqr_quantiles,
    data_source,
    plot_reliability=True,
):
    n = len(actuals)

    # Handling hpe
    hpe = ensembles[:, 0]
    hpe_quantile = 0.5
    ensembles = ensembles[:, 1:]

    quantiles_ensembles = np.arange(2, 100, 2) / 100
    quantiles_corrected_ensembles = np.linspace(
        0.05, 0.95, corrected_ensembles.shape[1]
    ).round(3)

    # Ensuring that we are working with numpy arrays
    quantile_forecasts = (
        np.array(quantile_forecasts)
        if type(quantile_forecasts) != np.ndarray
        else quantile_forecasts
    )
    actuals = np.array(actuals) if type(actuals) != np.ndarray else actuals
    actuals_ensembles = actuals.copy()
    corrected_taqr_quantiles = (
        np.array(corrected_taqr_quantiles)
        if type(corrected_taqr_quantiles) != np.ndarray
        else corrected_taqr_quantiles
    )
    corrected_ensembles = (
        np.array(corrected_ensembles)
        if type(corrected_ensembles) != np.ndarray
        else corrected_ensembles
    )

    m, n1 = quantile_forecasts.shape
    if m != len(actuals):
        quantile_forecasts = quantile_forecasts.T
        m, n1 = quantile_forecasts.shape

    # Ensure that the length match up
    if len(actuals) != len(quantile_forecasts):
        if len(actuals) < len(quantile_forecasts):
            quantile_forecasts = quantile_forecasts[: len(actuals)]
        else:
            actuals_taqr = actuals[-len(quantile_forecasts) :]

    if len(actuals) != len(corrected_ensembles):
        if len(actuals) < len(corrected_ensembles):
            corrected_ensembles = corrected_ensembles[: len(actuals)]
        else:
            actuals_taqr = actuals[-len(corrected_ensembles) :]

    # Reliability: how often actuals are below the given quantiles compared to the quantile levels
    reliability_points_taqr = []
    for i, q in enumerate(corrected_taqr_quantiles):
        forecast = quantile_forecasts[:, i]
        observed_below = np.sum(actuals_taqr <= forecast) / n
        reliability_points_taqr.append(observed_below)

    reliability_points_taqr = np.array(reliability_points_taqr)

    reliability_points_ensembles = []
    n_ensembles = len(actuals_ensembles)
    for i, q in enumerate(quantiles_ensembles):
        forecast = ensembles[:, i]
        observed_below = np.sum(actuals_ensembles <= forecast) / n_ensembles
        reliability_points_ensembles.append(observed_below)

    reliability_points_corrected_ensembles = []
    for i, q in enumerate(quantiles_corrected_ensembles):
        forecast = corrected_ensembles[:, i]
        observed_below = np.sum(actuals_ensembles <= forecast) / n_ensembles
        reliability_points_corrected_ensembles.append(observed_below)

    # Handle hpe separately
    observed_below_hpe = np.sum(actuals_ensembles <= hpe) / n_ensembles

    reliability_points_ensembles = np.array(reliability_points_ensembles)

    # Index of the 0.5 quantile
    idx_05 = np.where(corrected_taqr_quantiles == 0.5)[0][0]

    # Plotting the reliability plot
    if plot_reliability:
        import scienceplots

        with plt.style.context("no-latex"):
            plt.figure(figsize=(6, 6))
            plt.plot(
                [0, 1], [0, 1], "k--", label="Perfect Reliability"
            )  # Diagonal line
            plt.scatter(
                corrected_taqr_quantiles,
                reliability_points_taqr,
                color="blue",
                label="Reliability CorrectedTAQR",
            )
            plt.scatter(
                quantiles_ensembles,
                reliability_points_ensembles,
                color="grey",
                label="Reliability Original Ensembles",
                marker="p",
                alpha=0.5,
            )
            plt.scatter(
                quantiles_corrected_ensembles,
                reliability_points_corrected_ensembles,
                color="green",
                label="Reliability Corrected Ensembles",
                marker="p",
                alpha=0.5,
            )
            plt.scatter(
                hpe_quantile,
                observed_below_hpe,
                color="grey",
                label="Reliability HPE",
                alpha=0.5,
                marker="D",
                s=25,
            )
            plt.xlabel("Nominal Quantiles")
            plt.ylabel("Observed Frequencies")
            plt.title(
                f'Reliability Plot for {data_source.replace("_", " ").replace("lstm", "")}'
            )
            plt.legend()
            plt.grid(True)
            plt.savefig(f"reliability_plots/nolatex_reliability_plot_{data_source}.pdf")
            plt.show()

    return (
        reliability_points_taqr,
        reliability_points_ensembles,
        reliability_points_corrected_ensembles,
    )


def calculate_scores(
    actuals,
    taqr_results,
    raw_ensembles,
    corrected_ensembles,
    quantiles_taqr,
    data_source,
    plot_reliability=True,
    visualize = True,
    return_full_scores = False
):
    """Calculate Variogram, CRPS, QSS and MAE for the predictions and corrected ensembles.

    Parameters
    ----------
    actuals : numpy.ndarray
        The actual values
    predictions : numpy.ndarray
        The predicted values
    raw_ensembles : numpy.ndarray
        The raw ensembles
    corrected_ensembles : numpy.ndarray
        The corrected ensembles
    quantiles : list
        The quantiles to calculate the scores for
    data_source : str
        The data source
    """

    # Find common index
    common_index = corrected_ensembles.index.intersection(actuals.index)

    ensembles_CE_index = raw_ensembles.loc[common_index]
    actuals_comp = actuals.loc[common_index]

    variogram_score_raw_v2, variogram_score_list_raw = variogram_score_R_v2(
        ensembles_CE_index.loc[actuals_comp.index].values, actuals_comp.values
    )
    variogram_score_raw_corrected_v2, variogram_score_list_raw_corrected = variogram_score_R_v2(
        corrected_ensembles.loc[actuals_comp.index].values, actuals_comp.values
    )
    variogram_score_corrected_taqr_v2, variogram_score_list_corrected_taqr = variogram_score_R_v2(
        taqr_results.values, actuals_comp.values
    )

    qs_raw = calculate_qss(
        actuals_comp.values,
        ensembles_CE_index.loc[actuals_comp.index].T,
        np.linspace(0.05, 0.95, ensembles_CE_index.shape[1]),
    )
    qs_corr = calculate_qss(
        actuals_comp.values,
        corrected_ensembles.loc[actuals_comp.index].T,
        np.linspace(0.05, 0.95, corrected_ensembles.shape[1]),
    )

    # TODO: Should be done with max and min from the training set. 
    taqr_values_clipped = np.clip(taqr_results, 0, max(actuals_comp.values))
    qs_corrected_taqr = calculate_qss(
        actuals_comp.values, taqr_values_clipped, quantiles_taqr
    )

    

    crps_orig_ensembles = calculate_crps(
        actuals_comp.values.flatten(), ensembles_CE_index.loc[actuals_comp.index].T,
        return_full_scores = return_full_scores
    )
    crps_corr_ensembles = calculate_crps(
        actuals_comp.values.flatten(), corrected_ensembles.loc[actuals_comp.index].T,
        return_full_scores = return_full_scores
    )
    crps_corrected_taqr = calculate_crps(
        actuals_comp.values.flatten(), np.array(taqr_results),
        return_full_scores = return_full_scores
    )

    # Instead of calculating mean value of ensembles, we just use the median
    MAE_raw_ensembles = np.abs(
        np.median(ensembles_CE_index.loc[actuals_comp.index].values, axis=1)
        - actuals_comp.values
    )
    MAE_corr_ensembles = np.abs(
        np.median(corrected_ensembles.loc[actuals_comp.index].values, axis=1)
        - actuals_comp.values
    )
    MAE_corrected_taqr = np.abs(
        (np.median(np.array(taqr_results), axis=1) - actuals_comp.values)
    )
    if return_full_scores:
        scores_data = {
            "Metric": ["MAE", "CRPS", "Variogram", "QS"],
            "Original Ensembles": [
                MAE_raw_ensembles,
                crps_orig_ensembles,
                np.diff(np.array(variogram_score_list_raw), prepend=0),
                qs_raw,
            ],
            "Corrected Ensembles": [
                MAE_corr_ensembles,
                crps_corr_ensembles,
                np.diff(np.array(variogram_score_list_raw_corrected), prepend=0),
                qs_corr,
            ],
            "NABQR": [
                MAE_corrected_taqr,
                crps_corrected_taqr,
                np.diff(np.array(variogram_score_list_corrected_taqr), prepend=0),
                qs_corrected_taqr,
            ],
        }
    else:
        scores_data = {
            "Metric": ["MAE", "CRPS", "Variogram", "QS"],
            "Original Ensembles": [
                np.mean(MAE_raw_ensembles),
                crps_orig_ensembles,
                variogram_score_raw_v2,
                np.mean(qs_raw),
            ],
            "Corrected Ensembles": [
                np.mean(MAE_corr_ensembles),
                crps_corr_ensembles,
                variogram_score_raw_corrected_v2,
                np.mean(qs_corr),
            ],
            "NABQR": [
                np.mean(MAE_corrected_taqr),
                crps_corrected_taqr,
                variogram_score_corrected_taqr_v2,
                np.mean(qs_corrected_taqr),
            ],
        }

    scores_df = pd.DataFrame(scores_data).T

    # Calculate relative scores
    scores_data["Corrected Ensembles"] = [
        1
        + (x - scores_data["Original Ensembles"][i])
        / scores_data["Original Ensembles"][i]
        for i, x in enumerate(scores_data["Corrected Ensembles"])
    ]
    scores_data["NABQR"] = [
        1
        + (x - scores_data["Original Ensembles"][i])
        / scores_data["Original Ensembles"][i]
        for i, x in enumerate(scores_data["NABQR"])
    ]

    # Create DataFrame
    scores_df = pd.DataFrame(scores_data).T

    print("Scores: ")
    print(scores_df)

    # Print LaTeX table
    latex_output = scores_df.to_latex(
        column_format="lcccc",
        header=True,
        float_format="%.3f",
        caption=f"Performance Metrics for Different Ensemble Methods on {data_source}",
        label="tab:performance_metrics",
        escape=False,
    ).replace("& 0 & 1 & 2 & 3 \\\\\n\\midrule\n", "")

    with open(f"latex_output_{data_source}_scores.tex", "w") as f:
        f.write(latex_output)

    # Reliability plot 
    reliability_func(
        taqr_results,
        corrected_ensembles,
        raw_ensembles,
        actuals,
        quantiles_taqr,
        data_source,
        plot_reliability = visualize,
    )

    return scores_df



def run_r_script(X_filename, Y_filename, tau):
    """Run R script for quantile regression.

    Parameters
    ----------
    X_filename : str
        Path to X data CSV file
    Y_filename : str
        Path to Y data CSV file
    tau : float
        Quantile level
    """
    import subprocess

    process = subprocess.Popen(
        ["R", "--vanilla"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )

    r_script = f"""
    options(warn = -1)
    # library(onlineforecast) 
    library(quantreg) 
    library(readr) 
    library(SparseM)
    X_full <- read_csv("{X_filename}", col_names = FALSE, show_col_types = FALSE) 
    y <- read_csv("{Y_filename}", col_names = "y", show_col_types = FALSE) 
    X_full <- X_full[1:500,]
    data <- cbind(X_full, y[1:500,1]) 
    predictor_cols <- colnames(X_full) 
    formula_string <- paste("y ~ 0+", paste(predictor_cols, collapse = " + ")) 
    formula <- as.formula(formula_string) 
    rq_fit <- rq(formula, tau = {tau}, data = data ) 
    write.csv(rq_fit$coefficients, "rq_fit_coefficients.csv") 
    write.csv(rq_fit$residuals, "rq_fit_residuals.csv") 
    """

    for line in r_script.strip().split("\n"):
        process.stdin.write(line.encode("utf-8") + b"\n")

    process.stdin.close()
    process.stdout.read()
    process.terminate()


def remove_zero_columns(df):
    """Wrapper function to remove columns that contain only zeros from a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame

    Returns
    -------
    pandas.DataFrame
        DataFrame with zero columns removed
    """
    return df.loc[:, (df != 0).any(axis=0)]


def remove_zero_columns_numpy(arr):
    """Remove columns that contain only zeros or constant values from a numpy array.

    Parameters
    ----------
    arr : numpy.ndarray
        Input array

    Returns
    -------
    numpy.ndarray
        Array with zero/constant columns removed
    """
    return arr[:, (arr != 0).any(axis=0) & (arr != arr[0]).any(axis=0)]


def create_dataset_for_lstm(X, Y, time_steps):
    """Create a dataset suitable for LSTM training with multiple time steps (i.e. lags).

    Parameters
    ----------
    X : numpy.ndarray
        Input features
    Y : numpy.ndarray
        Target values
    time_steps : list
        List of time steps to include

    Returns
    -------
    tuple
        (X_lstm, Y_lstm) LSTM-ready datasets
    """
    X = np.array(X)
    Y = np.array(Y)

    Xs, Ys = [], []
    for i in range(len(X)):
        X_entry = []
        for ts in time_steps:
            if i - ts >= 0:
                X_entry.append(X[i - ts, :])
            else:
                X_entry.append(np.zeros_like(X[0, :]))
        Xs.append(np.array(X_entry))
        Ys.append(Y[i])
    return np.array(Xs), np.array(Ys)


class QuantileRegressionLSTM(tf.keras.Model):
    """LSTM-based model for quantile regression.
    Input: x -> LSTM -> Dense -> Dense -> output

    Parameters
    ----------
    n_quantiles : int
        Number of quantiles to predict
    units : int
        Number of LSTM units
    n_timesteps : int
        Number of time steps in input
    """

    def __init__(self, n_quantiles, units, n_timesteps, **kwargs):
        super().__init__(**kwargs)
        self.lstm = tf.keras.layers.LSTM(
            units, input_shape=(None, n_quantiles, n_timesteps), return_sequences=False
        )
        self.dense = tf.keras.layers.Dense(n_quantiles, activation="sigmoid")
        self.dense2 = tf.keras.layers.Dense(n_quantiles, activation="relu")
        self.n_quantiles = n_quantiles
        self.n_timesteps = n_timesteps

    def call(self, inputs, training=None):
        """Forward pass of the model.

        Parameters
        ----------
        inputs : tensorflow.Tensor
            Input tensor
        training : bool, optional
            Whether in training mode, by default None

        Returns
        -------
        tensorflow.Tensor
            Model output
        """
        x = self.lstm(inputs, training=training)
        x = self.dense(x)
        x = self.dense2(x)
        return x

    def get_config(self):
        """Get model configuration.

        Returns
        -------
        dict
            Model configuration
        """
        config = super(QuantileRegressionLSTM, self).get_config()
        config.update(
            {
                "n_quantiles": self.n_quantiles,
                "units": self.lstm.units,
                "n_timesteps": self.n_timesteps,
            }
        )
        return config

    @classmethod
    def from_config(cls, config):
        """Create model from configuration.

        Parameters
        ----------
        config : dict
            Model configuration

        Returns
        -------
        QuantileRegressionLSTM
            Model instance
        """
        return cls(**config)


def quantile_loss_3(q, y_true, y_pred):
    """Calculate quantile loss for a single quantile.

    Parameters
    ----------
    q : float
        Quantile level
    y_true : tensorflow.Tensor
        True values
    y_pred : tensorflow.Tensor
        Predicted values

    Returns
    -------
    tensorflow.Tensor
        Quantile loss value
    """
    y_true = tf.cast(y_true, tf.float32)
    y_pred = tf.cast(y_pred, tf.float32)
    y_true = tfp.stats.percentile(y_true, 100 * q, axis=1)
    error = y_true - y_pred
    return tf.maximum(q * error, (q - 1) * error)


def quantile_loss_func(quantiles):
    """Create a loss function for multiple quantiles.

    Parameters
    ----------
    quantiles : list
        List of quantile levels

    Returns
    -------
    function
        Loss function for multiple quantiles
    """

    def loss(y_true, y_pred):
        """Calculate the loss for given true and predicted values.

        Parameters
        ----------
        y_true : tensorflow.Tensor
            True values
        y_pred : tensorflow.Tensor
            Predicted values

        Returns
        -------
        tensorflow.Tensor
            Combined loss value for all quantiles
        """
        losses = []
        for i, q in enumerate(quantiles):
            loss = quantile_loss_3(q, y_true, y_pred[:, i])
            losses.append(loss)
        return tf.reduce_mean(tf.stack(losses))

    return loss


def map_range(values, input_start, input_end, output_start, output_end):
    """Map values from one range to another.

    Parameters
    ----------
    values : list
        Values to map
    input_start : float
        Start of input range
    input_end : float
        End of input range
    output_start : float
        Start of output range
    output_end : float
        End of output range

    Returns
    -------
    numpy.ndarray
        Mapped values
    """
    mapped_values = []
    for value in values:
        proportion = (value - input_start) / (input_end - input_start)
        mapped_value = output_start + (proportion * (output_end - output_start))
        mapped_values.append(int(mapped_value))

    return np.array(mapped_values)


def legend_without_duplicate_labels(ax):
    """Create a legend without duplicate labels.
    Primarily used for ensemble plots.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes object to create legend for
    """
    handles, labels = ax.get_legend_handles_labels()
    unique = [
        (h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]
    ]
    ax.legend(*zip(*unique))


def remove_straight_line_outliers(ensembles):
    """Remove ensemble members that are perfectly straight lines (constant slope).
    Explanation: Sometimes the output from the LSTM is a straight line, which is not useful for the ensemble.

    Parameters
    ----------
    ensembles : numpy.ndarray
        2D array where rows are time steps and columns are ensemble members

    Returns
    -------
    numpy.ndarray
        Filtered ensemble data without straight-line outliers
    """
    # Calculate differences along the time axis
    differences = np.diff(ensembles, axis=0)

    # Identify columns where all differences are the same (perfectly straight lines)
    straight_line_mask = np.all(differences == differences[0, :], axis=0)

    # Remove the columns with perfectly straight lines
    return ensembles[:, ~straight_line_mask]


def train_model_lstm(
    quantiles,
    epochs: int,
    lr: float,
    batch_size: int,
    x,
    y,
    x_val,
    y_val,
    n_timesteps,
    data_name,
):
    """Train LSTM model for quantile regression.
    The @tf.function decorator is used to speed up the training process.


    Parameters
    ----------
    quantiles : list
        List of quantile levels to predict
    epochs : int
        Number of training epochs
    lr : float
        Learning rate for optimizer
    batch_size : int
        Batch size for training
    x : tensor
        Training input data
    y : tensor
        Training target data
    x_val : tensor
        Validation input data
    y_val : tensor
        Validation target data
    n_timesteps : int
        Number of time steps in input sequence
    data_name : str
        Name identifier for saving model artifacts

    Returns
    -------
    tf.keras.Model
        Trained LSTM model
    """
    model = QuantileRegressionLSTM(
        n_quantiles=len(quantiles), units=256, n_timesteps=n_timesteps
    )
    optimizer = tf.keras.optimizers.Adam(learning_rate=lr)

    @tf.function
    def train_step(x_batch, y_batch):
        with tf.GradientTape() as tape:
            y_pred = model(x_batch, training=True)
            losses = quantile_loss_func(quantiles)(y_batch, y_pred)
            total_loss = tf.reduce_mean(losses)

        grads = tape.gradient(total_loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))
        return total_loss

    @tf.function
    def val_step(x_batch, y_batch):
        y_pred = model(x_batch, training=False)
        losses = quantile_loss_func(quantiles)(y_batch, y_pred)
        total_loss = tf.reduce_mean(losses)
        return total_loss

    train_loss_history = []
    val_loss_history = []
    y_preds = []
    y_true = []

    for epoch in range(epochs):
        epoch_train_loss = 0.0
        epoch_val_loss = 0.0
        num_batches = 0

        # Training loop
        for i in range(0, len(x), batch_size):
            x_batch = x[i : i + batch_size]
            y_batch = y[i : i + batch_size]

            batch_train_loss = train_step(x_batch, y_batch)
            epoch_train_loss += batch_train_loss
            num_batches += 1

            y_preds.append(model(x_batch, training=False))
            y_true.append(y_batch)

        epoch_train_loss /= num_batches
        train_loss_history.append(epoch_train_loss)

        # Validation loop
        num_val_batches = 0
        for i in range(0, len(x_val), batch_size):
            x_val_batch = x_val[i : i + batch_size]
            y_val_batch = y_val[i : i + batch_size]

            batch_val_loss = val_step(x_val_batch, y_val_batch)
            epoch_val_loss += batch_val_loss
            num_val_batches += 1

        epoch_val_loss /= num_val_batches
        val_loss_history.append(epoch_val_loss)

        print(
            f"Epoch {epoch+1} Train Loss: {epoch_train_loss:.4f} Validation Loss: {epoch_val_loss:.4f}"
        )

    y_preds_concat = tf.concat(y_preds, axis=0).numpy()
    y_true_concat = tf.concat(y_true, axis=0).numpy()

    return model


def one_step_quantile_prediction(
    X_input,
    Y_input,
    n_init,
    n_full,
    quantile=0.5,
    already_correct_size=False,
    n_in_X=5000,
    print_output=True,
):
    """Perform one-step quantile prediction using TAQR.

    This function takes the entire training set and, based on the last n_init observations,
    calculates residuals and coefficients for the quantile regression.

    An easy wrapper function to run TAQR.

    Parameters
    ----------
    X_input : numpy.ndarray or pd.DataFrame
        Input features
    Y_input : numpy.ndarray or pd.Series
        Target values
    n_init : int
        Number of initial observations for warm start
    n_full : int
        Total number of observations to process
    quantile : float, optional
        Quantile level for prediction, by default 0.5
    already_correct_size : bool, optional
        Whether input data is already correctly sized, by default False
    n_in_X : int, optional
        Number of observations to include in design matrix, by default 5000

    Returns
    -------
    tuple
        (predictions, actual values, coefficients)
    """
    assert n_init <= n_full - 2, "n_init must be less two greater than n_full"

    if type(X_input) == pd.DataFrame:
        X_input = X_input.to_numpy()

    if type(Y_input) == pd.Series or type(Y_input) == pd.DataFrame:
        Y_input = Y_input.to_numpy()

    n, m = X_input.shape
    if print_output:
        print("X_input shape: ", X_input.shape)

    full_length, p = X_input.shape

    X = X_input[:n_full, :].copy()
    Y = Y_input[:n_full]

    X_for_residuals = X[:n_init, :]
    Y_for_residuals = Y[:n_init]

    np.savetxt("X_for_residuals.csv", X_for_residuals, delimiter=",")
    np.savetxt("Y_for_residuals.csv", Y_for_residuals, delimiter=",")

    run_r_script("X_for_residuals.csv", "Y_for_residuals.csv", tau=quantile)

    def ignore_first_column(s):
        return float(s)

    residuals = np.genfromtxt(
        "rq_fit_residuals.csv",
        delimiter=",",
        skip_header=1,
        usecols=(1,),
        converters={0: ignore_first_column},
    )

    beta_init = np.genfromtxt(
        "rq_fit_coefficients.csv",
        delimiter=",",
        skip_header=1,
        usecols=(1,),
        converters={0: ignore_first_column},
    )

    if print_output:
        print("len of beta_init: ", len(beta_init))
        print(
            "There is: ",
            sum(residuals == 0),
            "zeros in residuals",
            "and",
            sum(abs(residuals) < 1e-8),
            "close to zeroes",
        )
        print("p: ", p)

    if len(beta_init) < p:
        beta_init = np.append(beta_init, np.ones(p - len(beta_init)))
    else:
        beta_init = beta_init[:p]
    r_init = set_n_closest_to_zero(arr=residuals, n=len(beta_init))
    
    if print_output:
        print(sum(r_init == 0), "r_init zeros")

    X_full = np.column_stack((X, Y, np.random.choice([1, 1], size=n_full)))
    IX = np.arange(p)
    Iy = p
    Iex = p + 1
    bins = np.array([-np.inf, np.inf])
    tau = quantile
    n_in_bin = int(1.0 * full_length)
    if print_output:
        print("n_in_bin", n_in_bin)

    n_input = n_in_X
    N, BETA, GAIN, Ld, Rny, Mx, Re, CON1, T = rq_simplex_final(
        X_full, IX, Iy, Iex, r_init, beta_init, n_input, tau, bins, n_in_bin
    )

    y_pred = np.sum((X_input[(n_input + 2) : (n_full), :] * BETA[1:, :]), axis=1)
    y_actual = Y_input[(n_input+2) : (n_full)] # TODO: check if this is correct    
    if print_output:
        print("y_pred shape", y_pred.shape)
        print("y_actual shape", y_actual.shape)

    y_actual_quantile = np.quantile(y_actual, quantile)
    return y_pred, y_actual, BETA


def run_taqr(corrected_ensembles, actuals, quantiles, n_init, n_full, n_in_X):
    """Wrapper function to run TAQR on corrected ensembles.

    Parameters
    ----------
    corrected_ensembles : numpy.ndarray
        Shape (n_timesteps, n_ensembles)
    actuals : numpy.ndarray
        Shape (n_timesteps,)
    quantiles : list
        Quantiles to predict
    n_init : int
        Number of initial timesteps for warm start
    n_full : int
        Total number of timesteps
    n_in_X : int
        Number of timesteps in design matrix

    Returns
    -------
    list
        TAQR results for each quantile
    """
    if type(actuals) == pd.Series or type(actuals) == pd.DataFrame:
        actuals = actuals.to_numpy()
        actuals[np.isnan(actuals)] = 0
    else:
        actuals[np.isnan(actuals)] = 0

    taqr_results = []
    actuals_output = []
    BETA_output = []
    for q in quantiles:
        print("Running TAQR for quantile: ", q)
        time_start_quantile = time.time()
        y_pred, y_actuals, BETA_q = one_step_quantile_prediction(
            corrected_ensembles,
            actuals,
            n_init=n_init,
            n_full=n_full,
            quantile=q,
            already_correct_size=True,
            n_in_X=n_in_X,
        )
        time_end_quantile = time.time()
        print(f"TAQR time for quantile {q}: {time_end_quantile - time_start_quantile} seconds")
        taqr_results.append(y_pred)
        actuals_output.append(y_actuals)
        BETA_output.append(BETA_q)

    return taqr_results, actuals_output[1], BETA_output


def reliability_func(
    quantile_forecasts,
    corrected_ensembles,
    ensembles,
    actuals,
    corrected_taqr_quantiles,
    data_source,
    plot_reliability=True,
):
    # Problem: there is a problem with simulated original ensembles. Function should be cleaned and tested.
    # For now, the original ensembles are not plotted.
    # Fix: Actually it is correct. However the problem is that the original ensembles are not even close to spanning the range of the data
    # Maybe actually the problem is that the ensembles are covering the data too well...
    # 
    #  
    n = len(actuals)

    # Ensuring that we are working with numpy arrays
    quantile_forecasts = (
        np.array(quantile_forecasts)
        if type(quantile_forecasts) != np.ndarray
        else quantile_forecasts
    )
    actuals = np.array(actuals) if type(actuals) != np.ndarray else actuals
    actuals_ensembles = actuals.copy()
    actuals_taqr = actuals.copy()
    corrected_taqr_quantiles = (
        np.array(corrected_taqr_quantiles)
        if type(corrected_taqr_quantiles) != np.ndarray
        else corrected_taqr_quantiles
    )
    corrected_ensembles = (
        np.array(corrected_ensembles)
        if type(corrected_ensembles) != np.ndarray
        else corrected_ensembles
    )
    ensembles = np.array(ensembles) if type(ensembles) != np.ndarray else ensembles

    # Handling hpe (high probability ensemble)
    hpe = ensembles[:, 0]
    hpe_quantile = 0.5
    ensembles = ensembles[:, 1:]

    quantiles_ensembles = np.linspace(0.05, 0.95, ensembles.shape[1]).round(3)
    quantiles_corrected_ensembles = np.linspace(
        0.05, 0.95, corrected_ensembles.shape[1]
    ).round(3)

    m, n1 = quantile_forecasts.shape
    if m != len(actuals):
        quantile_forecasts = quantile_forecasts.T
        m, n1 = quantile_forecasts.shape

    # Ensure that the length match up
    if len(actuals) != len(quantile_forecasts):
        if len(actuals) < len(quantile_forecasts):
            quantile_forecasts = quantile_forecasts[: len(actuals)]
        else:
            actuals_taqr = actuals[-len(quantile_forecasts) :]

    if len(actuals) != len(corrected_ensembles):
        if len(actuals) < len(corrected_ensembles):
            corrected_ensembles = corrected_ensembles[: len(actuals)]
        else:
            actuals_taqr = actuals[-len(corrected_ensembles) :]

    if len(actuals) != len(ensembles):
        if len(actuals) < len(ensembles):
            ensembles = ensembles[: len(actuals)]
            hpe = hpe[: len(actuals)]
        else:
            actuals_taqr = actuals[-len(ensembles) :]
            hpe = hpe[-len(ensembles) :]

    # Reliability: how often actuals are below the given quantiles compared to the quantile levels
    reliability_points_taqr = []
    for i, q in enumerate(corrected_taqr_quantiles):
        forecast = quantile_forecasts[:, i]
        observed_below = np.sum(actuals_taqr <= forecast) / n
        reliability_points_taqr.append(observed_below)

    reliability_points_taqr = np.array(reliability_points_taqr)

    reliability_points_ensembles = []
    n_ensembles = len(actuals_ensembles)
    for i, q in enumerate(quantiles_ensembles):
        forecast = ensembles[:, i]
        observed_below = np.sum(actuals_ensembles <= forecast) / n_ensembles
        reliability_points_ensembles.append(observed_below)

    reliability_points_corrected_ensembles = []
    for i, q in enumerate(quantiles_corrected_ensembles):
        forecast = corrected_ensembles[:, i]
        observed_below = np.sum(actuals_ensembles <= forecast) / n_ensembles
        reliability_points_corrected_ensembles.append(observed_below)

    # Handle hpe separately
    observed_below_hpe = np.sum(actuals_ensembles <= hpe) / n_ensembles

    reliability_points_ensembles = np.array(reliability_points_ensembles)

    # Find the index of the 0.5 quantile
    idx_05 = np.argmin(np.abs(corrected_taqr_quantiles - 0.5))

    if plot_reliability:
        import scienceplots

        with plt.style.context("no-latex"):
            # Plot reliability: nominal quantiles vs calculated quantiles
            plt.figure(figsize=(6, 6))
            plt.plot(
                [0, 1], [0, 1], "k--", label="Perfect Reliability"
            )  # Diagonal line
            plt.scatter(
                corrected_taqr_quantiles,
                reliability_points_taqr,
                color="blue",
                label="NABQR",
            )
            # TODO: fix this problem and uncomment, once fixed. 
            # plt.scatter(
            #     quantiles_ensembles,
            #     reliability_points_ensembles,
            #     color="grey",
            #     label="Original Ensembles",
            #     marker="p",
            #     alpha=0.5,
            # )
            plt.scatter(
                quantiles_corrected_ensembles,
                reliability_points_corrected_ensembles,
                color="green",
                label="Corrected Ensembles",
                marker="p",
                alpha=0.5,
            )
            plt.scatter(
                hpe_quantile,
                observed_below_hpe,
                color="grey",
                label="High Prob. Ensemble",
                alpha=0.5,
                marker="D",
                s=25,
            )
            plt.xlabel("Nominal Quantiles")
            plt.ylabel("Observed Frequencies")
            plt.title(
                f'Reliability Plot for {data_source.replace("_", " ").replace("lstm", "")}'
            )
            plt.legend()
            plt.grid(True)
            plt.savefig(f"reliability_plot_{data_source}.pdf")
            plt.show()

    return (
        reliability_points_taqr,
        reliability_points_ensembles,
        reliability_points_corrected_ensembles,
    )


def pipeline(
    X,
    y,
    name="TEST",
    training_size=0.8,
    epochs=100,
    timesteps_for_lstm=[0, 1, 2, 6, 12, 24, 48],
    **kwargs,
):
    """Main pipeline for NABQR model training and evaluation.

    The pipeline:
    1. Trains an LSTM network to correct the provided ensembles
    2. Runs TAQR algorithm on corrected ensembles to predict observations
    3. Saves results and model artifacts

    Parameters
    ----------
    X : pd.DataFrame or numpy.ndarray
        Shape (n_samples, n_features) - Ensemble data
    y : pd.Series or numpy.ndarray
        Shape (n_samples,) - Observations
    name : str, optional
        Dataset identifier, by default "TEST"
    training_size : float, optional
        Fraction of data to use for training, by default 0.8
    epochs : int, optional
        Number of training epochs, by default 100
    timesteps_for_lstm : list, optional
        Time steps to use for LSTM input, by default [0, 1, 2, 6, 12, 24, 48]
    **kwargs : dict
        Additional keyword arguments

    Returns
    -------
    tuple
        A tuple containing:
        - corrected_ensembles: pd.DataFrame
            The corrected ensemble predictions.
        - taqr_results: list of numpy.ndarray
            The TAQR results.
        - actuals_output: list of numpy.ndarray
            The actual output values.
        - BETA_output: list of numpy.ndarray
            The BETA parameters.
    """
    # Data preparation
    #. // TODO: check, that this loading works for npy and pd,... seems fine as of now, 5th feb 2025
    actuals = y
    ensembles = X
    
    if isinstance(y, pd.Series):
        idx = y.index
    elif isinstance(X, pd.DataFrame):
        idx = X.index
    else:
        idx = pd.RangeIndex(start=0, stop=len(y), step=1)

    if isinstance(y, np.ndarray):
        X_y = np.concatenate((X, y.reshape(-1, 1)), axis=1)
        y = pd.Series(y, index=idx)
    else:
        X_y = np.concatenate((X, y.values.reshape(-1, 1)), axis=1)
        y = pd.Series(y.values.flatten(), index=idx)

    train_size = int(training_size * len(actuals))
    ensembles = pd.DataFrame(ensembles, index=idx)
    # ensembles.index = pd.to_datetime(ensembles.index, utc=False).tz_localize(None)
    actuals = pd.DataFrame(actuals, index=idx)
    # actuals.index = pd.to_datetime(actuals.index, utc=False).tz_localize(None)
    common_index = ensembles.index.intersection(actuals.index)
    X_y = pd.DataFrame(X_y, index=idx)
    # X_y.index = pd.to_datetime(X_y.index, utc=False).tz_localize(None)
    ensembles = ensembles.loc[common_index]
    actuals = actuals.loc[common_index]
    X_y = X_y.loc[common_index]

    timesteps = timesteps_for_lstm
    Xs, X_Ys = create_dataset_for_lstm(ensembles, X_y, timesteps_for_lstm)

    # Handle NaN values
    if np.isnan(Xs).any():
        print("Xs has NaNs")
        Xs[np.isnan(Xs).any(axis=(1, 2))] = 0
    if np.isnan(X_Ys).any():
        print("X_Ys has NaNs")
        X_Ys[np.isnan(X_Ys).any(axis=1)] = 0

    # Data standardization
    XY_s_max_train = np.max(X_Ys[:train_size])
    XY_s_min_train = np.min(X_Ys[:train_size])

    X_Ys_scaled_train = (X_Ys[:train_size] - XY_s_min_train) / (
        XY_s_max_train - XY_s_min_train
    )
    Xs_scaled_train = (Xs[:train_size] - XY_s_min_train) / (
        XY_s_max_train - XY_s_min_train
    )

    validation_size = 100
    X_Ys_scaled_validation = (
        X_Ys[train_size : (train_size + validation_size)] - XY_s_min_train
    ) / (XY_s_max_train - XY_s_min_train)
    Xs_scaled_validation = (
        Xs[train_size : (train_size + validation_size)] - XY_s_min_train
    ) / (XY_s_max_train - XY_s_min_train)

    # Train LSTM model
    quantiles_lstm = np.linspace(0.05, 0.95, 20)
    time_start_lstm = time.time()
    model = train_model_lstm(
        quantiles=quantiles_lstm,
        epochs=epochs,
        lr=1e-3,
        batch_size=50,
        x=tf.convert_to_tensor(Xs_scaled_train),
        y=tf.convert_to_tensor(X_Ys_scaled_train),
        x_val=tf.convert_to_tensor(Xs_scaled_validation),
        y_val=tf.convert_to_tensor(X_Ys_scaled_validation),
        n_timesteps=timesteps,
        data_name=f"{name}_LSTM_epochs_{epochs}",
    )
    time_end_lstm = time.time()
    print(f"LSTM training time: {time_end_lstm - time_start_lstm} seconds")

    save_files = kwargs.get("save_files", True)
    if save_files:
        # Save model
        try:
            today = dt.datetime.today().strftime("%Y-%m-%d")
            model.save(f"Model_{name}_{epochs}_{today}.keras")
        except:
            model.save(f"Models_{name}_{epochs}.keras")

    # Generate predictions
    Xs_scaled_test = (Xs[train_size:] - XY_s_min_train) / (
        XY_s_max_train - XY_s_min_train
    )
    corrected_ensembles = model(Xs_scaled_test)
    corrected_ensembles = (
        corrected_ensembles * (XY_s_max_train - XY_s_min_train) + XY_s_min_train
    )
    actuals_out_of_sample = actuals[train_size:]
    test_idx = idx[train_size:]

    # Run TAQR
    quantiles_taqr = kwargs.get("quantiles_taqr", [0.1, 0.3, 0.5, 0.7, 0.9])
    n_full = len(actuals_out_of_sample)
    n_init = int(0.25 * n_full)
    limit = kwargs.get("limit", 5000)
    if n_init < limit: # TODO: should actually be 5000 for optimal results... for wind power production.
        print(f"25% of the data is less than {limit} timesteps, thus, setting n_init to 50% of the data length or {limit}, whichever is smaller")
        n_init = min(int(0.5*n_full), limit)
    # print("n_init, n_full: ", n_init, n_full)

    corrected_ensembles = corrected_ensembles.numpy()
    corrected_ensembles = remove_zero_columns_numpy(corrected_ensembles)
    corrected_ensembles = remove_straight_line_outliers(corrected_ensembles)
    corrected_ensembles = pd.DataFrame(corrected_ensembles, index=test_idx)
    n_in_X = n_init
    time_start_taqr = time.time()
    taqr_results, actuals_output, BETA_output = run_taqr(
        corrected_ensembles,
        actuals_out_of_sample,
        quantiles_taqr,
        n_init,
        n_full,
        n_in_X,
    )
    time_end_taqr = time.time()
    print(f"TAQR time: {time_end_taqr - time_start_taqr} seconds")
    actuals_out_of_sample = actuals_out_of_sample[(n_init + 1) : (n_full - 1)]
    actuals_output = pd.Series(
        actuals_output.flatten(), index=test_idx[(n_init + 1) : (n_full - 1)]
    )
    corrected_ensembles = corrected_ensembles.iloc[(n_init + 1) : (n_full - 1)]
    idx_to_save = test_idx[(n_init + 1) : (n_full - 1)]

    # Save results
    data_source = f"{name}"
    today = dt.datetime.today().strftime("%Y-%m-%d")

    if save_files:  
        np.save(
            f"results_{today}_{data_source}_actuals_out_of_sample.npy",
            actuals_out_of_sample,
        )
    df_corrected_ensembles = pd.DataFrame(corrected_ensembles, index=idx_to_save)
    if save_files:
        df_corrected_ensembles.to_csv(
            f"results_{today}_{data_source}_corrected_ensembles.csv"
        )
        np.save(f"results_{today}_{data_source}_taqr_results.npy", taqr_results)
        np.save(f"results_{today}_{data_source}_actuals_output.npy", actuals_output)
        np.save(f"results_{today}_{data_source}_BETA_output.npy", BETA_output)

    return (
        corrected_ensembles,
        pd.DataFrame(np.array(taqr_results).T, index=idx_to_save),
        actuals_output,
        BETA_output,
        ensembles,
    )
