import pandas as pd
import numpy as np
from datetime import datetime
import os

# -------------------------
# CONFIGURATION
# -------------------------

# 4 ans d'historique : 2021-01 à 2024-12
START = "2021-01-01"
END   = "2024-12-01"

OUTPUT_PATH = os.path.join("..", "Data", "tolgo_revenue_history.csv")
np.random.seed(42)


def generate_history(start=START, end=END):
    # Crée une série mensuelle
    dates = pd.date_range(start=start, end=end, freq="MS")

    n = len(dates)

    # Croissance forte : base + tendance + bruit
    # Nombre d'utilisateurs actifs
    base_users = 5000
    users_trend = np.linspace(0, 8000, n)  # +8k users sur la période
    users_noise = np.random.normal(0, 400, n)
    users = base_users + users_trend + users_noise
    users = np.maximum(users, 1000)  # jamais négatif

    # ARPU (Average Revenue Per User)
    # Légère hausse dans le temps (plus de premium)
    base_arpu = 28
    arpu_trend = np.linspace(0, 7, n)  # passe de 28 à ~35
    arpu_noise = np.random.normal(0, 1, n)
    arpu = base_arpu + arpu_trend + arpu_noise
    arpu = np.maximum(arpu, 20)

    # MRR = users * ARPU
    mrr = users * arpu

    # Revenu total = MRR + petits one-offs (frais ponctuels, etc.)
    one_offs = np.random.normal(0.03, 0.01, n)  # 3% moyenne
    revenue = mrr * (1 + one_offs)

    # Churn en baisse (meilleure rétention)
    # part de clients qui quittent sur le mois
    base_churn = 0.065  # 6.5%
    churn_trend = np.linspace(0, -0.025, n)  # descend vers ~4%
    churn_noise = np.random.normal(0, 0.004, n)
    churn_rate = base_churn + churn_trend + churn_noise
    churn_rate = np.clip(churn_rate, 0.02, 0.12)

    # Growth rate du MRR (variation % mois / mois)
    mrr_series = pd.Series(mrr, index=dates)
    growth_rate = mrr_series.pct_change().fillna(0)

    # Mix de plans (light / standard / premium)
    # Plus on avance, plus le premium augmente
    light_share = np.clip(
        0.45 - np.linspace(0, 0.15, n) + np.random.normal(0, 0.015, n),
        0.10, 0.60
    )
    premium_share = np.clip(
        0.25 + np.linspace(0, 0.15, n) + np.random.normal(0, 0.015, n),
        0.15, 0.55
    )
    standard_share = 1 - light_share - premium_share

    plan_mix_light = light_share
    plan_mix_standard = standard_share
    plan_mix_premium = premium_share

    # Construire le DataFrame final
    df = pd.DataFrame({
        "month": dates,
        "active_users": users.round().astype(int),
        "arpu": arpu.round(2),
        "mrr": mrr.round(2),
        "total_revenue": revenue.round(2),
        "churn_rate": churn_rate.round(4),
        "mrr_growth_rate": growth_rate.round(4),
        "plan_light_share": plan_mix_light.round(4),
        "plan_standard_share": plan_mix_standard.round(4),
        "plan_premium_share": plan_mix_premium.round(4),
    })

    # Sécurité : s'assurer que les parts de plans somment à 1 (± petite marge)
    shares_sum = (
        df["plan_light_share"]
        + df["plan_standard_share"]
        + df["plan_premium_share"]
    )
    df["plan_standard_share"] = (
        df["plan_standard_share"] + (1 - shares_sum)
    ).round(4)

    return df


def main():
    df = generate_history()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print("Dataset generated!")
    print(f"Shape: {df.shape}")
    print(f"Saved to: {OUTPUT_PATH}")
    print("\nHead:\n", df.head())


if __name__ == "__main__":
    main()
