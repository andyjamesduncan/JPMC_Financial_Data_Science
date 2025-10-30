import matplotlib.pyplot as plt

company = 'AAPLCo'   # change to 'BetaBank' if you like
sub = df[df['company'] == company].copy()

fig, ax1 = plt.subplots(figsize=(11,4.5))

# Revenue (bars)
ax1.bar(sub['period'], sub['revenue_musd'])
ax1.set_ylabel('Revenue (USD millions)')
ax1.set_xlabel('Quarter')
ax1.set_title(f'{company}: Revenue vs Gross Margin (highlighting margin squeezes)')

# Gross margin (line) on secondary axis
ax2 = ax1.twinx()
ax2.plot(sub['period'], sub['gross_margin_pct'], marker='o')
ax2.set_ylabel('Gross Margin (%)')

# Annotate squeeze quarters
squeezes = sub[sub['margin_squeeze']]
for _, r in squeezes.iterrows():
    ax2.annotate('squeeze',
                 xy=(r['period'], r['gross_margin_pct']),
                 xytext=(0,10),
                 textcoords='offset points',
                 ha='center', fontsize=8)

fig.tight_layout()
plt.show()
