#Libraries that we would be needing
import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go

#Data Reading
df = pd.read_excel(r"E:\Adidas Project\Project\Adidas.xlsx")
df.head(5) #Printing the first 5 rows of the data

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image = Image.open("Adidas logo.jpg")

#Creating two columns
col1, col2 = st.columns([0.1, 0.9]) #Giving them width
with col1:
    st.image(image, width=100)

html_title = """
    <style>
    .title-test{
    font-weight:bold;
    padding:5px;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Adidas Interactive Sales Dashboard</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

col3,  col4, col5 = st.columns([0.1, 0.45, 0.45])
with col3:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write(f"Last updated by:  \n {box_date}")

with col4:
    fig = px.bar(df, x = "Retailer", y = "TotalSales", labels={"TotalSales ": "Total Sales (in $)"},
                 title="Total Sales by Retailer", hover_data=["TotalSales"], template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15, 0.20, 0.20, 0.20,0.20])
with view1:
    expander = st.expander("Retailer wise sales")
    data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data.to_csv().encode("utf-8"),
                       file_name="RetailerSales.csv", mime="text/csv")
    
df["Month_Year"] = df["InvoiceDate"].dt.strftime("%b'%y")
result = df.groupby(by = df["Month_Year"])["TotalSales"].sum().reset_index()

with col5:
    fig1 = px.line(result, x = "Month_Year", y = "TotalSales", title = "Total Sales Over Time", 
                   template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    #data = df[["Retailer", "TotalSales"]].groupby(by="Retailer")["TotalSales"].sum()
    data = result
    expander.write(data)

with dwn2:
    st.download_button("Get Data", data = result.to_csv().encode("utf-8"),
                       file_name="MonthlySales.csv", mime="text/csv")
    
st.divider()

res1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

fig3 = go.Figure()  # Fixed: go.Figure() with capital F
fig3.add_trace(go.Bar(x=res1["State"], y=res1["TotalSales"], name="Total Sales"))
fig3.add_trace(go.Scatter(
    x=res1["State"], 
    y=res1["UnitsSold"], 
    mode="lines",
    name="Units Sold", 
    yaxis="y2"
))

fig3.update_layout(
    title="Total Sales and Units sold by State",  # Removed "a" for better grammar
    xaxis=dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid=True),  # Fixed: showgrid spelling
    yaxis2=dict(
        title="Units Sold", 
        overlaying="y", 
        side="right",
        showgrid=False  # Added for consistency
    ),
    template="gridon",
    legend=dict(x=1, y=1.1)
)

# Fixed columns syntax - using parentheses and proper values
_, col6 = st.columns((0.1, 1))  # Fixed: st.columns with parentheses
with col6:
    st.plotly_chart(fig3, use_container_width=True)

_, view3, dwn3, = st.columns((0.5, 0.45, 0.45))
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(res1)
with dwn3:
    st.download_button("Get Data", data = res1.to_csv().encode("utf-8"),
                       file_name="Sales_by_UnitsSold.csv", mime="text/csv")

st.divider()

#Creating a Tree Map Chart
_, col7 = st.columns([0.1, 1])
treemap = df[["Region", "City", "TotalSales"]].groupby(by = ["Region", "City"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value > 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)
    
treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(treemap, path = ["Region", "City"], values = "TotalSales", hover_name= "TotalSales (Formatted)",
                hover_data= ["TotalSales (Formatted)"],
                  color = "City", height = 700, width = 600)
fig4.update_traces(textinfo = "label+value")

with col7:
    st.subheader("Total Sales by Region and City in Treemap")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4, = st.columns([0.4, 0.45, 0.45])
with view4:
    res2 = df[["Region", "City", "TotalSales"]].groupby(by=["Region", "City"])["TotalSales"].sum()
    expander = st.expander("View Data for Total Sales by Region and City")
    expander.write(res2)

with dwn4:
    st.download_button("Get Data", data=res2.to_csv().encode("utf-8"), file_name="Sales_by_region.csv", mime="text/csv")
st.divider()

# Adding two more simple graphs
st.subheader("Additional Insights")

# First graph: City vs Operating Profit
col8, col9 = st.columns(2)

with col8:
    fig5 = px.bar(df, x="City", y="OperatingProfit", 
                 title="Operating Profit by City",
                 labels={"OperatingProfit": "Operating Profit ($)"},
                 color="City",
                 template="gridon")
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

# Second graph: Region vs Price per Unit
with col9:
    fig6 = px.box(df, x="Region", y="PriceperUnit", 
                 title="Price per Unit Distribution by Region",
                 labels={"PriceperUnit": "Price per Unit ($)"},
                 color="Region",
                 template="gridon")
    st.plotly_chart(fig6, use_container_width=True)

# Add download buttons for these new visualizations
_, view6, dwn6, view7, dwn7 = st.columns([0.15, 0.20, 0.20, 0.20, 0.20])

with view6:
    expander = st.expander("View Operating Profit by City")
    data_city_profit = df.groupby("City")["OperatingProfit"].sum().reset_index()
    expander.write(data_city_profit)

with dwn6:
    st.download_button("Get Operating Profit Data", 
                      data=data_city_profit.to_csv().encode("utf-8"),
                      file_name="OperatingProfit_by_City.csv", 
                      mime="text/csv")

with view7:
    expander = st.expander("View Price per Unit by Region")
    data_region_price = df.groupby("Region")["PriceperUnit"].describe()
    expander.write(data_region_price)

with dwn7:
    st.download_button("Get Price per Unit Data", 
                      data=data_region_price.to_csv().encode("utf-8"),
                      file_name="PriceperUnit_by_Region.csv", 
                      mime="text/csv")
st.divider()

# Now if we want to view the entire dataset.
_, view5, dwn5 = st.columns([0.4,0.45,0.45])
with view5:
    expander = st.expander("View Entire Sales Raw Dataset")
    expander.write(df)
with dwn5:
    st.download_button("Get Raw Data", data=df.to_csv().encode("utf-8"), file_name="Sales_RawData.csv", mime="text/csv")
st.divider()