# EUR/USD Exchange Rate Analyzer
Course: Introduction to Python

This repository contains a Python package for analyzing and forecasting EUR/USD historical exchange rate data. It includes tools for data loading, preprocessing, exploratory data analysis, visualization, and time series forecasting using Facebook's Prophet library.

The package is built to support:
 - Time series forecasting
 - Exchange rate trend and volatility analysis

## Dataset Overview
Source: [Historical EUR/USD exchange rate data (2000–2025)](https://www.kaggle.com/datasets/saifansariai/euro-usd-price-2001-to-2025)

Frequency: Daily

Rows: 11,284

Columns: 7

Format: CSV

Columns:
 - Date – Date of recorded exchange rate (Format: DD-MM-YYYY)
 - Price – Closing price of EUR/USD
 - Open – Opening price
 - High – Highest price of the day
 - Low – Lowest price of the day
 - Vol. – Volume (all values are NaN)
 - Change % – Percent change from previous day (as string with % sign)

## Installation
To install the package locally, clone this repository and install the required dependencies:

```
git clone https://github.com/nisher07/EURUSD_Analysis.git
```
Make sure you have Prophet, pandas, matplotlib, seaborn, and scikit-learn installed. If not, add them via:

```
pip install prophet pandas matplotlib seaborn scikit-learn
```

## Usage Example
Here’s how to use the package after importing:

```
from EURUSD_package import DataLoader, DataAnalyzer, DataVisualizer,
AnalyzeForecast

# 1. Load and preprocess the dataset
loader = DataLoader("EURUSD_data.csv")
loader.load_data()
loader.preprocess_data()

# 2. Analyze the dataset
analyzer = DataAnalyzer(loader.data)
print(analyzer.describe_data())

# 3. Forecast future values
forecast = AnalyzeForecast(loader.data)
forecast.perform_forecasting()
```

For a full walkthrough, check the [TUTORIAL.ipynb](https://github.com/nisher07/EURUSD_Analysis/blob/main/TUTORIAL.ipynb) notebook in this repo.

## License
This project is licensed under the MIT License – see the [LICENSE](https://github.com/nisher07/EURUSD_Analysis/blob/main/LICENSE) file for details.