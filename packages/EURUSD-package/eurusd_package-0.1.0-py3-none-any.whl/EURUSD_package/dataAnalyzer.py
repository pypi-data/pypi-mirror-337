import pandas as pd

class DataAnalyzer:
    """
    A class for analyzing and generating descriptive statistics for the data.

    Attributes:
    data (DataFrame): The data to analyze.
    """
    def __init__(self, data):
        """
        Initialize the DataAnalyzer class.

        Parameters:
        data (DataFrame): The input data to analyze.
        """
        # Assert that data is a pandas DataFrame
        assert isinstance(data, pd.DataFrame), "Input data must be a pandas DataFrame."
        
        # Assert that the DataFrame is not empty
        assert not data.empty, "Input DataFrame is empty."
        
        self.data = data

    # Method to return descriptive statistics of the DataFrame.
    def describe_data(self):
        """
        Generate descriptive statistics that summarize the central tendency, dispersion,
        and shape of the dataset distribution, excluding NaN values.

        Returns:
        DataFrame: Descriptive statistics of the data.
        """
        # The describe() method generates descriptive statistics that
        # summarize the central tendency, dispersion, and shape of
        # the dataset’s distribution, excluding NaN values. This
        # includes metrics like mean, median, mode, standard
        # deviation, etc., for each column.
        # Assert that the DataFrame has at least one numeric column to describe
        assert not self.data.select_dtypes(include=["number"]).empty, "Data must contain numeric columns for description."
        
        return self.data.describe()

    # Method to print a concise summary of the DataFrame.
    def describe_info(self):
        """
        Print a concise summary of the DataFrame including column types, non-null counts, 
        and memory usage.

        Returns:
        Data info
        """
        # The info() method prints a concise summary of a DataFrame.
        # This includes information about the index dtype and columns,
        # non-null values, and memory usage.
        return self.data.info()
