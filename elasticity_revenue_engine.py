"""
Pricing Elasticity of Demand & Revenue Yield Optimizer
Author: Puneet Goswami
Description: Estimates empirical price elasticity using log-log OLS regression 
             and calculates profit-maximizing price points based on marginal cost.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm


def generate_pricing_history(n_weeks: int = 104) -> pd.DataFrame:
    """Simulates 2 years of weekly price and demand variations across catalog segments."""
    np.random.seed(42)

    # Product A: Price Elastic (e.g., consumer electronics/accessories, true elasticity ~ -1.75)
    base_price_a = 49.0
    price_variations_a = base_price_a * np.random.uniform(0.85, 1.25, size=n_weeks)
    cost_a = 18.0
    # Demand generating function: Q = K * (P ^ epsilon) * noise
    demand_a = np.round(150000 * np.power(price_variations_a, -1.75) * np.random.normal(1.0, 0.08, size=n_weeks)).astype(int)

    # Product B: Price Inelastic (e.g., essential niche goods, true elasticity ~ -0.65)
    base_price_b = 85.0
    price_variations_b = base_price_b * np.random.uniform(0.90, 1.20, size=n_weeks)
    cost_b = 32.0
    demand_b = np.round(25000 * np.power(price_variations_b, -0.65) * np.random.normal(1.0, 0.06, size=n_weeks)).astype(int)

    df_a = pd.DataFrame({"sku_id": "SKU-ELAS-101", "name": "Wireless Audio Hub", "price": price_variations_a, "units": demand_a, "marginal_cost": cost_a})
    df_b = pd.DataFrame({"sku_id": "SKU-INEL-202", "name": "Industrial Sensor Module", "price": price_variations_b, "units": demand_b, "marginal_cost": cost_b})

    return pd.concat([df_a, df_b], ignore_index=True)


def estimate_elasticity_and_optimal_price(df: pd.DataFrame):
    """Performs log-log regression ln(Q) = a + e * ln(P) and outputs economic thresholds."""
    print("==========================================================================")
    print("ECONOMETRIC PRICING ELASTICITY & REVENUE OPTIMIZATION BENCHMARK")
    print("==========================================================================")

    for sku_id, group in df.groupby("sku_id"):
        product_name = group["name"].iloc[0]
        marginal_cost = group["marginal_cost"].iloc[0]
        avg_price = group["price"].mean()
        avg_volume = group["units"].mean()

        # Log transform for constant elasticity model
        log_price = np.log(group["price"])
        log_units = np.log(group["units"])
        X = sm.add_constant(log_price)

        model = sm.OLS(log_units, X).fit()
        elasticity = model.params.iloc[1]
        r_squared = model.rsquared

        print(f"\n--- Product: {product_name} ({sku_id}) ---")
        print(f"Current Avg Price: ${avg_price:.2f} | Avg Weekly Volume: {avg_volume:,.0f} units")
        print(f"Estimated Price Elasticity (ε) : {elasticity:.3f} (R² = {r_squared:.2f})")

        # Economic Classification
        if elasticity < -1.0:
            classification = "Elastic (Demand is sensitive; price drops increase gross revenue)"
            # Optimal markup formula for elastic goods: P* = MC * (e / (1 + e))
            optimal_price = marginal_cost * (elasticity / (1.0 + elasticity))
            recommendation = f"Target Profit-Maximizing Price: ${optimal_price:.2f} (from baseline ${avg_price:.2f})"
        else:
            classification = "Inelastic (Demand is resilient; selective price hikes expand margins)"
            recommendation = "Pricing power exists: Modest 5-8% price hike recommended to capture margin."

        print(f"Market Regime                 : {classification}")
        print(f"Executive Strategic Action    : {recommendation}")


if __name__ == "__main__":
    sales_logs = generate_pricing_history(104)
    estimate_elasticity_and_optimal_price(sales_logs)