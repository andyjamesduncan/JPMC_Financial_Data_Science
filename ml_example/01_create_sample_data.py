import pandas as pd
import numpy as np

np.random.seed(42)

# Build quarterly date range
quarters = pd.period_range('2019Q1', '2024Q4', freq='Q')
n = len(quarters)

def make_company(name, base_rev, rev_trend, rev_vol, base_gm, gm_drift, gm_vol):
    # revenue: trend + noise
    revenue = base_rev * (1 + rev_trend) ** np.arange(n)
    revenue = revenue * (1 + np.random.normal(0, rev_vol, n))
    revenue = np.maximum(revenue, 1.0)

    # gross margin %: slow drift + noise, clipped to [20, 70]
    gm = base_gm + gm_drift * np.arange(n) + np.random.normal(0, gm_vol, n)
    gm = np.clip(gm, 20, 70)

    # opex %: gently mean-reverting around 20–25%
    opex = (22 + np.random.normal(0, 1.2, n)).clip(12, 32)

    df = pd.DataFrame({
        'company': name,
        'quarter': quarters.astype(str),
        'revenue_musd': revenue.round(2),
        'gross_margin_pct': gm.round(2),
        'opex_pct': opex.round(2)
    })
    return df

df_a = make_company('AAPLCo', base_rev=18000, rev_trend=0.02, rev_vol=0.05,
                    base_gm=42, gm_drift=0.05, gm_vol=1.4)
df_b = make_company('BetaBank', base_rev=9000, rev_trend=0.025, rev_vol=0.06,
                    base_gm=37, gm_drift=-0.03, gm_vol=1.6)

data = pd.concat([df_a, df_b], ignore_index=True)

# Derived metrics
data['cogs_musd'] = (data['revenue_musd'] * (1 - data['gross_margin_pct']/100)).round(2)
data['gross_profit_musd'] = (data['revenue_musd'] - data['cogs_musd']).round(2)
data['opex_musd'] = (data['revenue_musd'] * data['opex_pct']/100).round(2)
data['op_income_musd'] = (data['gross_profit_musd'] - data['opex_musd']).round(2)
data['op_margin_pct'] = (100 * data['op_income_musd'] / data['revenue_musd']).round(2)

# Save the sample file
data.to_csv('financial_demo_quarterly.csv', index=False)
data.head(10)
