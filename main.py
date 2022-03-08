# @Email:  contact@pythonandvba.com
# @Website:  https://pythonandvba.com
# @YouTube:  https://youtube.com/c/CodingIsFun
# @Project:  Sales Dashboard w/ Streamlit

from pyproj import  CRS

import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit
import matplotlib.pyplot as plt
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="josefeson", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,
    )
    # Add 'hour' column to dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("por favor,escolha um filtro:")
city = st.sidebar.multiselect(
    "Selecione a Cidade:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Selecione o tipo de clinte:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "Selecione um Gênero:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

# ---- MAINPAGE ----
st.title(":bar_chart: joseferson dashboard")
st.markdown("##")

# TOP KPI's
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")

# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>vendas por linha de produto</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",width=200, height=400
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]
sales_by_hour = df_selection.groupby(by=["hour"]).sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Vendas por hora</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",width=200, height=400
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# grafico de rosca  [BAR CHART]
sales_by_hour = df_selection.groupby(by=["Gender"]).sum()[["Total"]]
fig_hourly = px.pie(
    sales_by_hour,
    values="Total",
    names=sales_by_hour.index,
    title="<b>Receita Gerada por sexo</b>",
    hole=.7,
    color_discrete_sequence=["#0083B8"] * len(["Gender"]),
    template="plotly_white",width=200, height=400
)

fig_hourly.update_layout( #margin = dict ( t = 1 ,  b = 1 ,  r = 1,  l = 1 ),
    #xaxis=dict(tickmode="linear"),
    #plot_bgcolor="rgba(0,0,0,0)",
    #yaxis=(dict(showgrid=False)),
)

# Gráfico Renda por Gênero[BAR CHART]
sales_by_hour = df_selection.groupby(["Gender" ,"Date"],as_index = False ).agg ({ "Total" : "sum" })
fig_hourl = px .line(sales_by_hour , x ="Date",y =["Total"],
    title="<b>total de Vendas por Sexo nos 3 Primeiros Meses</b>",
                       color = "Gender", color_discrete_sequence=px.colors.qualitative.Alphabet,
    width=800, height=400)

fig_hourl.update_layout(
   # xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    #yaxis=(dict(showgrid=False))
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourl, use_container_width=True)
right_column.plotly_chart(fig_hourly, use_container_width=True)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


def get_next_card(self):
    pass


def  get_next() :
    pass