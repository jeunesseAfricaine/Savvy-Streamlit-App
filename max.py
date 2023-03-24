import streamlit as st
st.set_page_config(layout="wide", initial_sidebar_state="expanded", 
                    page_title= "Destina Data App", page_icon=":sunny:")
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo
from PIL import Image
import streamlit.components.v1 as components
import plotly.express as px
import sklearn
from sklearn.cluster import KMeans

#set header

#st.title()


url = "https://raw.githubusercontent.com/Kanka-max/ADS_REV_code/main/011%20lesson%20Retail%20%20analytics/dataonline.csv"
#img = "https://unsplash.com/photos/JCIJnIXv7SE?utm_source=unsplash&utm_medium=referral&utm_content=creditShareLink"
#img = Image.open("keg.jpg")
with st.beta_expander("About The Store"):
        st.write("""
             An accessory shop with broad spectrum of the market including Phone accesories, Compute Parts and Gaming Technology.
            
    #        """)
with st.sidebar.beta_container():
    image = Image.open('savvy.jpg')

    st.image(image, caption='Savvy Tech')

    with st.beta_container():
        st.write("""
                Retail analysis on inventory levels, customer behaviour and sales.""")


data = st.sidebar.file_uploader("Upload Transactions", type=['csv', 'xlsx'])

if data is not None:
    df = pd.read_csv(data)
        #df = pd.read_excel(data)
    df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
        #Add temporal variables - revenue, month, year
    df["Revenue"] = df["UnitPrice"] * df["Quantity"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
    df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year

else:

    df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
    df["Revenue"] = df["UnitPrice"] * df["Quantity"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
    df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year

   



    
menu = ['Business Selfie','Customer Segmentation','Predictive Analytics']

with st.beta_container():
  
#add selection box
  selection = st.selectbox("Key Performance Indicator (KPI) ", menu)

#add descriptive information about the general functionality of the app
#'Retail analytics is the process of providing analytical data on inventory levels, supply chain movement, consumer demand, sales, etc. ... The analytics on demand and supply data can be used for maintaining procurement level and also for taking marketing decisions.
df_temp = df.groupby(["InvoiceMonth", "InvoiceYear"])["Quantity"].sum().reset_index()
df_temp1 = df.groupby(["InvoiceMonth"])["Revenue"].sum().reset_index()

df_merge = df_temp.merge(df_temp1, how="left", on=["InvoiceMonth"])
#Active Customers
df_active = df.groupby(["InvoiceMonth", "InvoiceYear"])["CustomerID"].nunique().reset_index()
df_table = df.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].sum().reset_index()
df_table = df_table.set_index("InvoiceMonth", inplace=True)
#Customer Type
#df_first_purchase = df.groupby(["CustomerID"])["InvoiceDate"].min().reset_index()
#df_first_purchase.columns = ["CustomerID", "FirstPurchaseDate"]

#df = pd.merge(df, df_first_purchase, on="CustomerID")

#["UserType"] = "New"

#df.loc[df["InvoiceDate"] > df["FirstPurchaseDate"], "UserType"] = "Existing"

#df_new_revenue = df.groupby(["InvoiceMonth", "InvoiceYear", "UserType"])["Revenue"].sum().reset_index()

if selection == "Business Selfie":
    st.markdown("**Inventory vs Sales Overview**")
    #st.table(df_merge.head(10))

    #col1 = st.columns(1)


    with st.beta_container():
        # Creating trace1
        fig = go.Figure()

        fig.add_trace(
            go.Bar(
                    x = df_merge.InvoiceMonth,
                    y = df_merge.Revenue,
                    orientation = "v",  # type of plot like marker, line or line + markers
                    name = "Revenue",#name of the plots
                    marker = dict(color = 'Indigo',
                    line = dict(color = "Indigo")),
                    showlegend = True,
                   
                    text= df.InvoiceYear) #The hover text (hover is curser)


            )
        fig.add_trace(
            go.Bar(
                    x = df_merge.InvoiceMonth,
                    y = df_merge.Quantity,
                    orientation = "v",
                    name = "Sales (Electronics)",
                    marker = dict(color = 'Purple',
                    line = dict(color = "Purple")),
                    showlegend = True,
                    
                    text= df_merge.InvoiceYear)


            )
        #fig.add_trace(
        #    go.Bar(
        #            x = df_active.InvoiceMonth,
        #            y = df_active.CustomerID,
        #            orientation = "v",
        #            name = "Active Customers",
        #            marker = dict(color = 'gold',
        #            line = dict(color = "gold")),
        #            showlegend = True,
                    
        #            text= df_merge.InvoiceYear)


        #    )

        #fig.add_trace(
        #    go.Scatter(
        #            x = df_merge.InvoiceMonth,
        #            y = df_merge.CustomerID,
        #           # orientation = "v",
        #            name = "Total Revenue",
        #            mode = "lines+markers",
        #            marker = dict(color = 'gold',
        #            line = dict(color = "gold")),
        #            showlegend = True,
                    
        #            text= df_merge.InvoiceYear)


        #    )
        #fig.add_trace(
        #    go.Scatter(
        #            x = df_merge.InvoiceMonth,
        #            y = df_merge.Quantity,
        #           # orientation = "v",
        #            name = "Total Liquor Sold",
        #            mode = "lines",
        #            marker = dict(color = 'gold',
        #            line = dict(color = "gold")),
        #            showlegend = True,
                    
        #            text= df_merge.InvoiceYear)


        #    )
        #fig.add_trace(
        #    go.Scatter(
        #            x = df_active.InvoiceMonth,
        #            y = df_active.CustomerID,
        #           # orientation = "v",
        #            name = "Total Revenue",
        #            mode = "lines+markers",
        #            marker = dict(color = 'gold',
        #            line = dict(color = "gold")),
        #            showlegend = True,
                    
        #            text= df_active.InvoiceYear)


        #    )


# layout 
        
        fig.update_layout(
            title_text = "Revenue and Electronics Sold Overview",
            title_font_size = 22,
            title_font_color = "Purple",
            title_font_family = "Raleway",
            xaxis=dict(
            title = "Month",
            showgrid=False,
            showline=True,
            showticklabels=False,
            zeroline=False,
        
        ),
            yaxis=dict(
            showgrid=True,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
            barmode='group',
            paper_bgcolor='Lavender',
            plot_bgcolor='Lavender',
            margin=dict(l=20, r=10, t=80, b=80),

            legend = dict(x=0, y=1.0, bgcolor = "black", bordercolor = "gold"),
            
    )

        st.plotly_chart(fig, sharing="streamlit", use_container_width=True)

        with st.beta_expander("See Chart Explanation"):
            st.write("""
            The chart above shows the relationship between *Revenue* and *Electronics Sold* across the years 2010/2011.
            Each stacked bar represents Revenue and Electronics sold overview on a monthly basis.
            The line shows the trend of active customers.
            """)    

    #col2 = st.columns(1)
    with st.beta_container():
        st.write("**Tabular Business Snapshot**")
        #st.table(df_table.head())
        #df_merge = df_merge.set_index("InvoiceMonth", inplace=True)
        st.table(df_merge.head(10))

        total_annual_revenue = df_merge.Revenue.sum()
        average_annual_revenue = df_merge.Revenue.mean()

        with st.beta_expander("See Annual Revenue"):
            st.write(total_annual_revenue)
        with st.beta_expander("See Average Revenue"):
            st.write(average_annual_revenue)

if selection == "Customer Segmentation":
    
    df_user=pd.DataFrame(df["CustomerID"].unique())
    df_user.columns=["CustomerID"]


    df_last_purchase=df.groupby(["CustomerID"])["InvoiceDate"].max().reset_index()
    df_last_purchase.columns=["CustomerID", "LastPurchaseDate"]

    df_last_purchase["Recency"]= (df_last_purchase["LastPurchaseDate"].max()-df_last_purchase["LastPurchaseDate"]).dt.days
    df_recency=pd.merge(df_user, df_last_purchase[["CustomerID", "Recency"]])

    
# find out how many clusters are optimal
# Cluster Customer based on Recency
    #y=df_recency[["Recency"]]
    #kmodel_recency=KMeans(n_clusters=4)
    #kmodel_recency.fit(y)
    #kpredict_recency=kmodel_recency.predict(y)
    #kpredict_recency[0:5]
    #df_recency["RecencyCluster"]=kpredict_recency
    #df_recency = df_recency.groupby(["RecencyCluster"])["Recency"].describe()

    
    st.subheader("Customer Recency")
    #    st.table(df_recency.head())
    with st.beta_expander("See Recency Cluster"):
        st.write("""
            This segment will describe summary statistics of;
            how **recently** customers make purchase.
            
            """)

# frequency of orders
#    df_frequency=df.groupby(["CustomerID"])["InvoiceDate"].count().reset_index()
#    df_frequency.columns=["CustomerID", "Frequency"]
#    df_frequency=pd.merge(df_user, df_frequency, on="CustomerID")

#    x=df_frequency[["Frequency"]]
 #   k_model_frequency=KMeans(n_clusters=4)
#    k_model_frequency.fit(x)
#    k_model_frequency_predict=k_model_frequency.predict(x)
#    df_frequency["FrequencyCluster"]=k_model_frequency_predict

    # Statistical Analysis of clusters based on frequency
   # df_frequency = df_frequency.groupby(["FrequencyCluster"])["Frequency"].describe()
    
    st.subheader("Frequency Of Orders")
        #st.table(df_frequency.head())
    with st.beta_expander("Frequency of Orders Cluster"):
        st.write("""
            This segement will describe summary statistics of;
            how **often** customers make purchase.
            
            """)
#Monetary 
    #df_customer_revenue=df.groupby(["CustomerID"])["Revenue"].sum().reset_index()
    #df_customer_revenue=pd.merge(df_user, df_customer_revenue, on="CustomerID")    
# Segmenting Customers Based on their Monetary Value
    #a=df_customer_revenue[["Revenue"]]
    #k_model_revenue=KMeans(n_clusters=4)
    #k_model_revenue.fit(a)
    #k_model_revenue_pred=k_model_revenue.predict(a)
    #df_customer_revenue["RevenueCluster"]=k_model_revenue_pred

    #df_customer_revenue = df_customer_revenue.groupby(["RevenueCluster"])["Revenue"].describe()


    st.subheader("Monetary Value")
    #    st.table(df_frequency.head())
    with st.beta_expander("Monetary Value Cluster"):
        st.write("""
            This segement will describe summary statistics of;
            how **much** customers spend at the liquor store.
            
    #        """)

if selection == "Predictive Analytics":
    st.write("Nothing to predict just yet! :sunglasses:")
    with st.beta_expander("See Why"):
        st.write("""
        This page will have predictions of sales using time series.
        Currently, we require sales data that spans 3 months or 1 quarter of a fiscal year.
        A year will be *better*!
        """)

with st.beta_container():

    st.write("Data App designed by **Destina AI** :sunny:")

@st.cache
def fetch_image(img):
    return st.sidebar.image(img, caption="Max Liquor")

@st.cache(persist=True)
def fetch_clean_data(url):
    if data is not None:
        df = pd.read_csv(data)
        #df = pd.read_excel(data)
        df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
        #Add temporal variables - revenue, month, year
        df["Revenue"] = df["UnitPrice"] * df["Quantity"]
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
        df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year

    else:

        df = pd.read_csv(url, encoding="ISO-8859-1", low_memory=False)
        df["Revenue"] = df["UnitPrice"] * df["Quantity"]
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["InvoiceMonth"] = pd.DatetimeIndex(df["InvoiceDate"]).month
        df["InvoiceYear"] = pd.DatetimeIndex(df["InvoiceDate"]).year

    return df

#@st.cache(persist=True)
#def fit_recency_model(y):

#    if y is not none:
#        kmodel_recency=KMeans(n_clusters=4)
#        kmodel_recency.fit(y)
#        kpredict_recency=kmodel_recency.predict(y)
#        #kpredict_recency[0:5]
#        df_recency["RecencyCluster"]=kpredict_recency

#    return df_recency

#@st.cache(persist=True)
#def fit_frequency_model(x):

#    if x is not none:
#        k_model_frequency=KMeans(n_clusters=4)
#        k_model_frequency.fit(x)
#        k_model_frequency_predict=k_model_frequency.predict(x)
#        df_frequency["FrequencyCluster"]=k_model_frequency_predict

#    return df_frequency

#@st.cache(persist=True)
#def fit_monetary_model(a):

#    if a is not none:
#        k_model_revenue=KMeans(n_clusters=4)
#        k_model_revenue.fit(a)
#        k_model_revenue_pred=k_model_revenue.predict(a)
#        df_customer_revenue["RevenueCluster"]=k_model_revenue_pred
#    return df_customer_revenue        
