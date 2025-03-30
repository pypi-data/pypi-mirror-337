import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


class DataVisualizer:
    """
    A class for visualizing data and performing seasonal decomposition.

    Attributes:
    data (DataFrame): The data to visualize.
    decomposition (DecomposeResult): Seasonal decomposition result of the 'price' column.
    """
    def __init__(self, data):
        """
        Initialize the DataVisualizer class.

        Parameters:
        data (DataFrame): The input data to visualize.
        """
        self.data = data
        # Perform seasonal decomposition on the 'price' column of the
        # DataFrame to separate it into trend, seasonal, and residual
        # components. This uses an additive model with a periodicity
        # of 365 days (assuming daily data).
        self.decomposition = seasonal_decompose(
            self.data["price"], model="additive", period=365
        )

    # Method to plot the original time series data.
    def plot_time_series(self):
        """
        Plot the original time series of 'price' against the index (Date).
        """
        # Set the style of the plot to 'whitegrid' which adds a grid for
        # better readability.
        sns.set_style("whitegrid")
        plt.figure(figsize=(14, 10))
        # Plot the 'price' data as a line plot, labeling it as 'Original'.
        sns.lineplot(
            data=self.data,
            x=self.data.index,
            y="price",
            label="Original",
            linewidth=2.5,
        )
        # Add a legend to the upper left corner of the plot.
        plt.legend(loc="upper left")
        # Set the title of the plot.
        plt.title("Original Time Series")
        # Display the plot.
        plt.show()

    # Method to plot the Trend component extracted by seasonal decomposition.
    def plot_Trend_Component(self):
        """
        Plot the trend component extracted from seasonal decomposition.
        """
        plt.figure(figsize=(10, 6))
        # Plot the trend component, label it as 'Trend'.
        plt.plot(self.decomposition.trend, label="Trend")
        plt.legend(loc="upper left")
        plt.title("Trend Component")
        plt.show()

    # Method to plot the Seasonal component extracted by
    # seasonal decomposition.
    def plot_Seasonal_Component(self):
        """
        Plot the seasonal component extracted from seasonal decomposition.
        """
        plt.figure(figsize=(10, 6))
        # Plot the seasonal component, label it as 'Seasonality'.
        plt.plot(self.decomposition.seasonal, label="Seasonality")
        plt.legend(loc="upper left")
        plt.title("Seasonal Component")
        plt.show()

    # Method to plot the Residual component extracted by
    # seasonal decomposition.
    def plot_Residual_Component(self):
        """
        Plot the residual component extracted from seasonal decomposition.

        """
        plt.figure(figsize=(10, 6))
        # Plot the residual component, label it as 'Residual'.
        plt.plot(self.decomposition.resid, label="Residual")
        plt.legend(loc="upper left")
        plt.title("Residual Component")
        plt.show()
