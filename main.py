import pandas as pd
import numpy as np
import streamlit as st
import Preprocessor

# changing the layout of streamlit
st.set_page_config(layout="wide")

# Reading the data
df = pd.read_csv("data.csv")

# Creatiing time features
df = Preprocessor.fetch_time_features(df)

# sidebar
st.sidebar.title("Filters")

# Filters
selected_year = Preprocessor.multiselect("Select Year", df["Financial_Year"].unique())
selected_retailer = Preprocessor.multiselect("Select Retailer", df["Retailer"].unique())
selected_company = Preprocessor.multiselect("Select Company", df["Company"].unique())
selected_month = Preprocessor.multiselect("Select Month", df["Financial_Month"].unique())

# Global filtering
filtered_df = df[(df["Financial_Year"].isin(selected_year)) & (df["Retailer"].isin(selected_retailer)) & (df["Company"].isin(selected_company)) & (df["Financial_Month"].isin(selected_month))]

# Title for dashbaord
st.title("Sales Analytics Dashboard")


# Creating columns for Indicators or KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label = "Total sales", value = int(filtered_df["Amount"].sum()))
with col2:
    st.metric(label = "Total margin", value = int(filtered_df["Margin"].sum()))
with col3:
    st.metric(label = "Total transactions", value = len(filtered_df["Margin"]))
with col4:
    st.metric(label = "Margin percentage (in %)", value = int(filtered_df["Margin"].sum()*100/filtered_df["Amount"].sum()))

# Month on month sales
yearly_sales = filtered_df[["Financial_Year", "Financial_Month", "Amount"]].groupby(["Financial_Year", "Financial_Month"]).sum().reset_index().pivot(index = "Financial_Month", columns = "Financial_Year", values = "Amount")
st.line_chart(yearly_sales, x_label = "Financial Month", y_label = "Total sales")

col5, col6 = st.columns(2)
# Retailer Revenue
with col5:
    st.title("Retailers count by revenue %")
    retailer_count = Preprocessor.fetch_top_revenue_retailers(filtered_df)
    retailer_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(retailer_count, x_label = "percentage revenue",y_label = "retailer_count")

with col6:
    st.title("Companies count by revenue %")
    company_count = Preprocessor.fetch_top_revenue_companies(filtered_df)
    company_count.set_index("percentage revenue", inplace = True)
    st.bar_chart(company_count, x_label = "percentage revenue",y_label = "company_count")

# Retaiter revenue
def fetch_top_revenue_retailers(df):
    retailers_revenue = df[["Retailer", "Amount"]].groupby("Retailer").sum().reset_index().sort_values(by = "Amount", ascending = False)
    total_revenue = retailers_revenue["Amount"].sum()
    percentages =  [100,90,80,70,60,50,40,30,20,10]
    retailer_count = []
    for i in percentages:
        target_revenue = 0.01*i*total_revenue
        loop = 1
        while loop <= len(retailers_revenue) and retailers_revenue.iloc[:loop, 1].sum() <= target_revenue:
            loop += 1
        retailer_count.append(loop)
    retailers = pd.DataFrame(data = {"percentage revenue" : percentages, "retailer_count" : retailer_count})
    return retailers

# Company revenue
# Companies revenue
def fetch_top_revenue_companies(df):
    company_revenue = df[["Company", "Amount"]].groupby("Company").sum().reset_index().sort_values(by = "Amount", ascending = False)
    total_revenue = company_revenue["Amount"].sum()
    percentages =  [100,90,80,70,60,50,40,30,20,10]
    company_count = []
    for i in percentages:
        target_revenue = 0.01*i*total_revenue
        loop = 1
        while loop <= len(company_revenue) and company_revenue.iloc[:loop, 1].sum() <= target_revenue:
            loop += 1
        company_count.append(loop)
    companies = pd.DataFrame(data = {"percentage revenue" : percentages, "company_count" : company_count})
    return companies