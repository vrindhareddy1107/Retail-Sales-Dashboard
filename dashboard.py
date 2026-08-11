import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import plot

# Read Excel file
df = pd.read_excel(
    r"C:\Users\sonti\OneDrive\Desktop\sales_with_season.xlsx"
)

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# 1. Revenue by Season & Region
# -----------------------------
season_sales = df.groupby(
    ["Season", "Region"],
    as_index=False
)["Revenue"].sum()

fig1 = px.bar(
    season_sales,
    x="Season",
    y="Revenue",
    color="Region",
    title="Total Revenue by Season and Region",
    barmode="group"
)

# -----------------------------
# 2. Units Sold by Season & Region
# -----------------------------
season_units = df.groupby(
    ["Season", "Region"],
    as_index=False
)["Units_Sold"].sum()

fig2 = px.bar(
    season_units,
    x="Season",
    y="Units_Sold",
    color="Region",
    title="Units Sold by Season and Region",
    barmode="group"
)

# -----------------------------
# 3. Sales Trend Over Time
# -----------------------------
fig3 = px.line(
    df,
    x="Date",
    y="Revenue",
    color="Region",
    title="Sales Trend Over Time"
)

# -----------------------------
# 4. Average Discount by Season
# -----------------------------
season_discount = df.groupby(
    "Season",
    as_index=False
)["Discount"].mean()

fig4 = px.pie(
    season_discount,
    names="Season",
    values="Discount",
    title="Average Discount by Season"
)

# -----------------------------
# Create 2 x 2 Dashboard
# -----------------------------
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Total Revenue by Season",
        "Units Sold by Season",
        "Sales Trend Over Time",
        "Average Discount by Season"
    ),
    specs=[
        [{"type": "bar"}, {"type": "bar"}],
        [{"type": "scatter"}, {"type": "pie"}]
    ]
)

# Add charts
fig.add_traces(fig1.data, rows=1, cols=1)
fig.add_traces(fig2.data, rows=1, cols=2)
fig.add_traces(fig3.data, rows=2, cols=1)
fig.add_traces(fig4.data, rows=2, cols=2)

# -----------------------------
# Dashboard Layout
# -----------------------------
fig.update_layout(
    title_text="Retail Sales Seasonal Dashboard",
    showlegend=True,
    height=900
)

# -----------------------------
# Save Dashboard
# -----------------------------
output_path = (
    r"C:\Users\sonti\OneDrive\Desktop\Retail Dashboard-1"
    r"\seasonal_dashboard.html"
)

plot(
    fig,
    filename=output_path,
    auto_open=True
)

print("Dashboard created successfully!")
print("Open the seasonal_dashboard.html file to view it.")