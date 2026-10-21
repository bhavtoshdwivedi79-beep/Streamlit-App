import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📊 Sales Analytics Dashboard")
st.write("Sales and profit analysis by month and region")


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Sales": [15000, 18000, 22000, 25000, 28000, 32000],
    "Profit": [3000, 3600, 5000, 6200, 7000, 8500],
    "Region": ["North", "South", "East", "West", "North", "South"]
})


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("🔎 Filters")

region_options = ["All"] + sorted(
    df["Region"].unique().tolist()
)

selected_region = st.sidebar.selectbox(
    "Select Region",
    region_options
)


# ==========================================
# APPLY FILTER
# ==========================================

filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]


# ==========================================
# METRICS
# ==========================================

st.header("📌 Key Metrics")

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

average_sales = filtered_df["Sales"].mean()

average_profit = filtered_df["Profit"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "💰 Total Sales",
        f"₹{total_sales:,.0f}"
    )


with col2:
    st.metric(
        "📈 Total Profit",
        f"₹{total_profit:,.0f}"
    )


with col3:
    st.metric(
        "📊 Average Sales",
        f"₹{average_sales:,.0f}"
    )


with col4:
    st.metric(
        "💵 Average Profit",
        f"₹{average_profit:,.0f}"
    )


# ==========================================
# DISPLAY DATA
# ==========================================

st.header("📋 Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)


# ==========================================
# MONTHLY SALES
# ==========================================

st.header("📊 Monthly Sales")

fig1 = px.bar(
    filtered_df,
    x="Month",
    y="Sales",
    title="Monthly Sales",
    text="Sales"
)

fig1.update_traces(
    marker_color=[
        "red",
        "blue",
        "green",
        "orange",
        "purple",
        "teal"
    ],
    texttemplate="₹%{text:,}",
    textposition="outside"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==========================================
# MONTHLY PROFIT
# ==========================================

st.header("💰 Monthly Profit")

fig2 = px.line(
    filtered_df,
    x="Month",
    y="Profit",
    title="Monthly Profit",
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# ==========================================
# REGION-WISE SALES
# ==========================================

st.header("🌍 Region-wise Sales")

region_sales = filtered_df.groupby(
    "Region",
    as_index=False
)["Sales"].sum()

fig3 = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Region-wise Sales",
    text="Sales"
)

fig3.update_traces(
    marker_color=[
        "red",
        "blue",
        "green",
        "orange"
    ],
    texttemplate="₹%{text:,}",
    textposition="outside"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ==========================================
# REGION-WISE PROFIT
# ==========================================

st.header("💵 Region-wise Profit")

region_profit = filtered_df.groupby(
    "Region",
    as_index=False
)["Profit"].sum()


fig4 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Region-wise Profit",
    hole=0
)

fig4.update_traces(
    textinfo="label+percent+value",
    texttemplate="%{label}<br>₹%{value:,}<br>%{percent}"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ==========================================
# SALES VS PROFIT
# ==========================================

st.header("📈 Sales vs Profit")

fig5 = px.line(
    filtered_df,
    x="Month",
    y=["Sales", "Profit"],
    title="Sales vs Profit",
    markers=True
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# ==========================================
# BEST SALES MONTH
# ==========================================

st.header("🏆 Best Sales Month")

best_month = filtered_df.loc[
    filtered_df["Sales"].idxmax()
]

st.success(
    f"Best Sales Month: {best_month['Month']} "
    f"with Sales of ₹{best_month['Sales']:,}"
)