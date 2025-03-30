from dataLoader import DataLoader
from dataAnalyzer import DataAnalyzer
from dataVisualizer import DataVisualizer
from analyzeForecast import AnalyzeForecast

def main():
    # Step 1: Load and preprocess the data
    loader = DataLoader()
    loader.preprocess_data()
    data = loader.get_data()

    # Step 2: Analyze the data
    print("=== Data Summary ===")
    analyzer = DataAnalyzer(data)
    print(analyzer.describe_data())  # Show descriptive stats
    print("\n=== Data Info ===")
    analyzer.describe_info()         # Show structure info

    # Step 3: Visualize the data
    visualizer = DataVisualizer(data)
    visualizer.plot_time_series()
    visualizer.plot_Trend_Component()
    visualizer.plot_Seasonal_Component()
    visualizer.plot_Residual_Component()

    # Step 4: Forecasting and further trend analysis
    forecaster = AnalyzeForecast(data)
    forecaster.plot_time_series_trend()
    forecaster.plot_ma_crossover_trend()
    forecaster.perform_forecasting()

if __name__ == "__main__":
    main()
