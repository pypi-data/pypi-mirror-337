import pandas as pd
import os


class DataLoader:
    """
    A class for loading and preprocessing the EUR/USD data.

    Attributes:
    filepath (str): Path to the data file.
    data (DataFrame): Loaded and preprocessed data.
    """
    def __init__(self, filename="EURUSD_data.csv"):
        """
        Initialize the DataLoader class.

        Parameters:
        filename (str): The name of the CSV file containing the EUR/USD data (default is "EURUSD_data.csv").
        """
        self.base_path = os.getcwd()  # Gets the current working directory
        self.filepath = os.path.join(self.base_path, "data", filename)
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"File '{self.filepath}' not found. Please check the path."
            )
        self.data = None
        self.load_data()

    def load_data(self):
        """
        Load data from the CSV file into a pandas DataFrame.
        
        This method handles reading the CSV file and stores the data into the 'data' attribute.
        """
        try:
            self.data = pd.read_csv(self.filepath)
            # Assert that the loaded data is a pandas DataFrame
            assert isinstance(self.data, pd.DataFrame), "Loaded data is not a pandas DataFrame."
            # Assert that the data is not empty
            assert not self.data.empty, "Loaded data is empty."
        except Exception as e:
            print(f"Error loading data: {e}")

    def preprocess_data(self):
        """
        Preprocess the loaded data by:
        - Converting the 'Date' column to datetime.
        - Dropping columns that contain only NaN values.
        - Standardizing column names.
        - Converting the 'change' column to 'change_in_percentage' if it exists.
        - Setting 'Date' as the index and sorting the data.
        
        """
        # Assert that the data has been loaded
        assert self.data is not None, "Data has not been loaded. Please load data first."
        
        if self.data is None:
            print("No data to preprocess.")
            return
        
        # Assert that 'Date' column exists in the DataFrame
        assert "Date" in self.data.columns, "'Date' column is missing in the data."
        
        # Convert 'Date' to datetime
        self.data["Date"] = pd.to_datetime(self.data["Date"], dayfirst=True)

        # Drop columns that are completely NaN
        self.data.drop(
            columns=[col for col in self.data.columns if self.data[col].isna().all()],
            inplace=True,
        )

        # Standardize column names
        self.data.columns = (
            self.data.columns.str.strip()
            .str.lower()
            .str.replace(r"[^\w\s]", "", regex=True)
            .str.replace(" ", "")
        )

        # Convert 'change' column to 'change_percentage' and remove '%'
        if "change" in self.data.columns:
            self.data.rename(
                columns={"change": "change_in_percentage"}, inplace=True
            )
            
            self.data["change_in_percentage"] = (
                self.data["change_in_percentage"]
                .astype(str)
                .str.rstrip("%")
                .astype(float)
            )

        # Set 'Date' as index
        self.data.set_index("date", inplace=True)
        self.data.sort_index(inplace=True)

    def get_data(self):
        """
        Retrieve the processed data.

        Returns:
        DataFrame: The processed data after preprocessing.
        """
        # Assert that data is loaded and not None
        assert self.data is not None, "No data available. Please load and preprocess the data first."
        
        return self.data

