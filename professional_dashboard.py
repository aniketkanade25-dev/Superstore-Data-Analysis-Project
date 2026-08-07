#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import pandas as pd
import plotly.express as px


# In[6]:


st.set_page_config(
   page_title=" Superstore Sales Dashboard",
   page_icon="📊",
   layout="wide"
)
st.title("Superstore Sales Dashboard")
st.markdown("### Interactive Business Intelligence Dashboard")
st.markdown("----")


# In[7]:


df= pd.read_csv("Superstore.csv", encoding="latin1")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"]= df["Order Date"].dt.month_name()


# In[9]:


st.sidebar.header("Dashboard Filters")

region=st.sidebar.multiselect(
    "Select Region",
     df["Region"].unique(),
     default=df["Region"].unique()
)

category= st.sidebar.multiselect(
     "Select Category",
      df["Category"].unique(),
      default=df["Category"].unique()
)

segment= st.sidebar.multiselect(
    "Select Segment",
    df["Segment"].unique(),
    default=df["Segment"].unique()
)

year= st.sidebar.multiselect(
      "Select Year",
       df["Year"].unique(),
       default=df["Year"].unique()
)

filtered_df = df[
         (df["Region"].isin(region)) &
         (df["Category"].isin(category)) &
         (df["Segment"].isin(segment)) &
         (df["Year"].isin(year)) 

    
]


# In[14]:


total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
average_sales = filtered_df["Sales"].mean()

col1,col2,col3,col4=st.columns(4)

col1.metric(" Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Orders", total_orders)
col4.metric("Avg Sales", f"${average_sales:,.2f}")


# In[15]:


category_sales = (
  filtered_df.groupby("Category")["Sales"].sum().reset_index())


# In[16]:


fig1 = px.bar( category_sales,
             x="Category",
             y="Sales",
             color="Category",
             title="sales by Category")
st.plotly_chart(fig1, use_container_width=True)


# In[19]:


region_profit =(
    filtered_df.groupby("Region")["Profit"].sum().reset_index())
fig2 = px.bar(
      region_profit,
      x="Region",
      y="Profit",
      color="Region",
      title="Profit By Region")

st.plotly_chart(fig2, use_container_width=True)


# In[20]:


month_order =[
    "January","February","March","April","May","June","July","August","September","October","November","December"
    
]

monthly_sales = ( filtered_df.groupby("Month")["Sales"].sum().reset_index())

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True)

monthly_sales= monthly_sales.sort_values("Month")

fig3= px.line(
   monthly_sales,
   x="Month",
   y="Sales",
   markers=True,
   title="Monthly Sales Trend"
)

st.plotly_chart(fig3,use_container_width=True)


# In[25]:


fig4 = px.pie(
    filtered_df,
    names="Segment",
    values="Sales",
    title="Sales By Segment"
)

st.plotly_chart(fig4, use_container_width=True)


# In[26]:


top_products =(
  filtered_df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(10).reset_index())
fig5 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products"
)

st.plotly_chart(fig5,use_container_width=True)


# In[30]:


top_states=(
   filtered_df.groupby("State")["Sales"].sum().sort_values(ascending=False).head(10).reset_index())

fig6 =px.bar(
   top_states,
   x="State",
   y="Sales",
   color="Sales",
   title="Top 10 States")

st.plotly_chart(fig6, use_container_width=True)


# In[33]:


fig7 =px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["Product Name"],
    title="Sales vs Profit"
)

st.plotly_chart(fig7, use_container_width=True)


# In[34]:


st.subheader("Dataset Preview")
st.dataframe(filtered_df)


# In[35]:


csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
  label ="Download Filtered Data",
  data=csv,
  file_name="Filtered_Sales.csv",
  mime="text/csv")


# In[ ]:




