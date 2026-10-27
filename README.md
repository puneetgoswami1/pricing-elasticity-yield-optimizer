# Pricing Elasticity & Revenue Yield Optimization Engine

An econometric pricing and yield management engine designed to estimate empirical price elasticity of demand ($\epsilon$), classify market sensitivity, and calculate margin-maximizing price points.

## Overview
Setting optimal product prices requires balancing sales volume velocity with gross profit contribution. Blind discount campaigns risk margin erosion, while arbitrary price hikes can crush unit sales. This project models price sensitivity across historical price-testing variations using log-log ordinary least squares (OLS) regression to pinpoint profit-maximizing equilibrium.

## Project Structure
- `price_volume_elasticity.sql`: Production SQL CTE pipeline computing week-over-week price deltas, demand velocity, and gross profit contributions.
- `elasticity_revenue_engine.py`: Econometric model evaluating constant elasticity curves ($\ln(Q) = \alpha + \epsilon \cdot \ln(P)$) and optimal markups based on unit marginal cost.
- `requirements.txt`: Python package dependencies.

## Key Econometric Metrics
1. **Elasticity Coefficient ($\epsilon$):** Quantifies percentage change in units demanded per 1% change in product pricing.
   - **Elastic ($\epsilon < -1$):** Price cuts drive disproportionate volume gains.
   - **Inelastic ($-1 < \epsilon < 0$):** Customers absorb price hikes with minimal volume decay, creating pricing power.
2. **Profit-Maximizing Price ($P^*$):** Derived from marginal cost ($MC$) and elasticity:
   $$P^* = MC \times \left(\frac{\epsilon}{1 + \epsilon}\right)$$
3. **Margin-Volume Trade-off:** Simulates gross margin expansion scenarios across multi-tier SKU portfolios.

## How to Run

```bash
# Clone the repository
git clone https://github.com/puneetgoswami1/pricing-elasticity-yield-optimizer.git
cd pricing-elasticity-yield-optimizer

# Install dependencies
pip install -r requirements.txt

# Run pricing elasticity model
python elasticity_revenue_engine.py