import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from statsmodels.tsa.statespace.sarimax import SARIMAX

# Prophet optionnel (si installé)
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except:
    PROPHET_AVAILABLE = False


DATA_PATH = os.path.join("..", "Data", "tolgo_revenue_history.csv")
OUTPUT_PATH = os.path.join("..", "Data", "forecast_output.csv")

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

def load_data(path=DATA_PATH):
    df = pd.read_csv(path, parse_dates=["month"])
    df = df.sort_values("month")
    df.set_index("month", inplace=True)
    return df


# --------------------------------------------------
# ARIMA Forecasting
# --------------------------------------------------

def forecast_arima(series, steps=12):
    model = SARIMAX(
        series,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 12),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    results = model.fit(disp=False)

    forecast = results.get_forecast(steps=steps)
    forecast_df = forecast.summary_frame()

    forecast_df = forecast_df[["mean", "mean_ci_lower", "mean_ci_upper"]]
    forecast_df.columns = ["mrr_forecast", "lower_ci", "upper_ci"]

    return forecast_df


# --------------------------------------------------
# Prophet Forecasting
# --------------------------------------------------

def forecast_prophet(df):
    if not PROPHET_AVAILABLE:
        print("Prophet not installed. Skipping Prophet forecast.")
        return None

    df_prophet = pd.DataFrame({
        "ds": df.index,
        "y": df["mrr"]
    })

    model = Prophet(yearly_seasonality=True)
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=12, freq="MS")
    forecast = model.predict(future)

    forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast.columns = ["month", "mrr_prophet", "lower_ci", "upper_ci"]

    return forecast.tail(12)


# --------------------------------------------------
# Main forecasting routine
# --------------------------------------------------

def main():
    df = load_data()
    mrr = df["mrr"]

    print("Running ARIMA forecast...")
    arima_fc = forecast_arima(mrr)

    # Reset index for export
    arima_fc.index = pd.date_range(
        start=df.index[-1] + pd.offsets.MonthBegin(),
        periods=12,
        freq="MS"
    )
    arima_fc.index.name = "month"

    # Prophet (optional)
    if PROPHET_AVAILABLE:
        print("Running Prophet forecast...")
        prophet_fc = forecast_prophet(df)
        prophet_fc.set_index("month", inplace=True)

        output = pd.concat([arima_fc, prophet_fc], axis=1)
    else:
        prophet_fc = None
        output = arima_fc

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    output.to_csv(OUTPUT_PATH)

    print("\nForecast saved to:", OUTPUT_PATH)
    print("\n--- Forecast Preview ---")
    print(output.head())

    # Quick plot
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df["mrr"], label="Historical MRR")
    plt.plot(output.index, output["mrr_forecast"], label="Forecast MRR (ARIMA)")
    plt.fill_between(
        output.index,
        output["lower_ci"],
        output["upper_ci"],
        alpha=0.2,
        label="Confidence Interval"
    )
    plt.title("Tolgo MRR Forecast – ARIMA")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
