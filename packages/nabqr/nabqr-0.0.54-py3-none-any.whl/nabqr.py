from .functions import *
from .helper_functions import simulate_correlated_ar1_process, set_n_closest_to_zero
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(["no-latex"])
from .visualization import visualize_results
import datetime as dt



def run_nabqr_pipeline(
    n_samples=5000,
    phi=0.995,
    sigma=8,
    offset_start=10,
    offset_end=500,
    offset_step=15,
    correlation=0.8,
    data_source="NABQR-TEST",
    training_size=0.7,
    epochs=100,
    timesteps=[0, 1, 2, 6, 12, 24],
    quantiles=[0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99],
):
    """Run the complete NABQR pipeline including data simulation, model training, and visualization.

    Parameters
    ----------
    n_samples : int, optional
        Number of time steps to simulate, by default 5000
    phi : float, optional
        AR(1) coefficient for simulation, by default 0.995
    sigma : float, optional
        Standard deviation of noise for simulation, by default 8
    offset_start : int, optional
        Start value for offset range, by default 10
    offset_end : int, optional
        End value for offset range, by default 500
    offset_step : int, optional
        Step size for offset range, by default 15
    correlation : float, optional
        Base correlation between dimensions, by default 0.8
    data_source : str, optional
        Identifier for the data source, by default "NABQR-TEST"
    training_size : float, optional
        Proportion of data to use for training, by default 0.7
    epochs : int, optional
        Number of epochs for model training, by default 100
    timesteps : list, optional
        List of timesteps to use for LSTM, by default [0, 1, 2, 6, 12, 24]
    quantiles : list, optional
        List of quantiles to predict, by default [0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]

    Returns
    -------
    None
        Saves results to files and displays visualization
    """
    # Generate offset and correlation matrix
    offset = np.arange(offset_start, offset_end, offset_step)
    m = len(offset)
    corr_matrix = correlation * np.ones((m, m)) + (1 - correlation) * np.eye(m)

    # Generate simulated data
    simulated_data, actuals = simulate_correlated_ar1_process(
        n_samples, phi, sigma, m, corr_matrix, offset, smooth=5
    )

    # Plot the simulated data
    plt.figure(figsize=(10, 6))
    plt.plot(simulated_data)
    plt.title("Simulated Data")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.show()

    # Run the pipeline
    pipeline(
        simulated_data,
        actuals,
        data_source,
        training_size=training_size,
        epochs=epochs,
        timesteps_for_lstm=timesteps,
        quantiles_taqr=quantiles,
    )

    # Get today's date for file naming
    today = dt.datetime.today().strftime("%Y-%m-%d")

    # Load results
    CE = pd.read_csv(f"results_{today}_{data_source}_corrected_ensembles.csv")
    y_hat = np.load(f"results_{today}_{data_source}_actuals_out_of_sample.npy")
    q_hat = np.load(f"results_{today}_{data_source}_taqr_results.npy")

    # Visualize results
    visualize_results(y_hat, q_hat, f"{data_source} example")


if __name__ == "__main__":
    run_nabqr_pipeline()
