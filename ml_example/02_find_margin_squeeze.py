import pandas as pd

df = pd.read_csv('financial_demo_quarterly.csv')
df['period'] = pd.PeriodIndex(df['quarter'], freq='Q').to_timestamp('Q')

# Sort and compute YoY deltas by company
df = df.sort_values(['company','period']).reset_index(drop=True)
df['revenue_yoy_%'] = df.groupby('company')['revenue_musd'].pct_change(4) * 100
df['gm_yoy_pp']    = df.groupby('company')['gross_margin_pct'].diff(4)  # percentage points

# Define "margin squeeze": revenue up YoY but GM down YoY
df['margin_squeeze'] = (df['revenue_yoy_%'] > 0) & (df['gm_yoy_pp'] < 0)

interesting = (df[df['margin_squeeze']]
               .loc[:, ['company','quarter','revenue_musd','gross_margin_pct','revenue_yoy_%','gm_yoy_pp']]
               .sort_values(['company','quarter']))

print("Margin squeeze quarters (revenue ↑ YoY, gross margin ↓ YoY):")
display(interesting.head(10))
