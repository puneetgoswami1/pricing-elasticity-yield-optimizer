# Price Elasticity & Margin Yield Analysis

An econometric pricing workflow using log-log regression to estimate SKU price elasticity of demand and evaluate margin-vs-volume trade-offs.

## Problem Context
Blanket discounting erodes gross margin on inelastic items, while uncalibrated price increases hurt volume on price-sensitive SKUs. This project estimates empirical elasticity coefficients from historical price changes and computes margin-optimal price points.

## Files
- `price_volume_elasticity.sql`: Calculates week-over-week price changes, unit volume shifts, and gross profit contribution.
- `elasticity_revenue_engine.py`: Fits log-log OLS demand curves (`ln(Q) = a + e * ln(P)`) and computes optimal markups over unit cost.
- `requirements.txt`: Python dependencies.

## How It Works
1. **Elasticity Estimation:** Measures percentage demand change per 1% price movement to separate elastic (`e < -1`) from inelastic SKUs.
2. **Margin Equilibrium:** Uses unit marginal cost and elasticity to calculate profit-maximizing price points.
3. **Scenario Simulation:** Compares gross profit impact across SKU tiers before rolling out price updates.

## Run Locally

    git clone https://github.com/puneetgoswami1/pricing-elasticity-yield-optimizer.git
    cd pricing-elasticity-yield-optimizer
    pip install -r requirements.txt
    python elasticity_revenue_engine.py
