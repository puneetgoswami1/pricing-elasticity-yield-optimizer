-- =====================================================================
-- PRICING VARIATION & DEMAND VOLUME AGGREGATION PIPELINE
-- Author: Puneet Goswami
-- Description: Aggregates weekly SKU price changes, unit volume velocity,
--              and discount depth to prepare econometric modeling inputs.
-- =====================================================================

WITH weekly_product_sales AS (
    SELECT 
        sku_id,
        DATE_TRUNC('week', order_date) AS sales_week,
        ROUND(AVG(unit_selling_price_usd), 2) AS avg_weekly_price_usd,
        SUM(quantity_sold) AS weekly_units_sold,
        SUM(net_revenue_usd) AS weekly_gross_revenue_usd,
        ROUND(AVG(discount_percentage), 2) AS avg_discount_depth_pct
    FROM retail_dw.fct_daily_sales
    WHERE order_date >= CURRENT_DATE - INTERVAL '365 DAYS'
    GROUP BY sku_id, DATE_TRUNC('week', order_date)
),

price_fluctuation_lagged AS (
    SELECT 
        sku_id,
        sales_week,
        avg_weekly_price_usd,
        weekly_units_sold,
        weekly_gross_revenue_usd,
        avg_discount_depth_pct,
        
        -- Lag price and volume from the prior week
        LAG(avg_weekly_price_usd, 1) OVER (
            PARTITION BY sku_id 
            ORDER BY sales_week ASC
        ) AS prior_week_price_usd,

        LAG(weekly_units_sold, 1) OVER (
            PARTITION BY sku_id 
            ORDER BY sales_week ASC
        ) AS prior_week_units_sold
    FROM weekly_product_sales
),

weekly_elasticity_deltas AS (
    SELECT 
        sku_id,
        sales_week,
        avg_weekly_price_usd,
        weekly_units_sold,
        weekly_gross_revenue_usd,
        prior_week_price_usd,
        prior_week_units_sold,
        
        -- Percentage changes
        ROUND(((avg_weekly_price_usd - prior_week_price_usd) / NULLIF(prior_week_price_usd, 0.0)) * 100, 2) AS price_delta_pct,
        ROUND(((weekly_units_sold - prior_week_units_sold) / NULLIF(prior_week_units_sold, 0.0)) * 100, 2) AS demand_delta_pct
    FROM price_fluctuation_lagged
    WHERE prior_week_price_usd IS NOT NULL
)

SELECT 
    d.sku_id,
    p.sku_name,
    p.category,
    p.unit_marginal_cost_usd,
    d.sales_week,
    d.avg_weekly_price_usd,
    d.weekly_units_sold,
    d.weekly_gross_revenue_usd,
    d.price_delta_pct,
    d.demand_delta_pct,
    
    -- Naive Point Elasticity (% Change in Quantity / % Change in Price)
    ROUND(
        d.demand_delta_pct / NULLIF(d.price_delta_pct, 0.0), 2
    ) AS naive_point_elasticity,

    -- Gross Profit Contribution
    ROUND(d.weekly_units_sold * (d.avg_weekly_price_usd - p.unit_marginal_cost_usd), 2) AS weekly_gross_profit_usd
FROM weekly_elasticity_deltas d
JOIN retail_dw.dim_product p ON d.sku_id = p.sku_id
WHERE ABS(d.price_delta_pct) >= 2.0 -- Filter negligible noise (<2% price change)
ORDER BY d.sku_id, d.sales_week DESC;