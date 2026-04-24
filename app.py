import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

#---------Load Data-------

df=pd.read_csv("new file.csv")

#----------Navbar----

select=option_menu(
    menu_title=None,
    options=["Home","Player Analysis","Country Insights","Comparisons","Data Explorer"],
    orientation="horizontal"

)

#----------Home------

if select=="Home":

    st.title("Cricket Analytics Dashboard")

    col1,col2,col3=st.columns(3)

    col1.metric("Total Players",df["Player"].nunique())

    col2.metric("Total Runs",df["Runs"].sum())

    col3.metric("Countries",df["Country"].nunique())


    st.dataframe(df.head())

#--------Player Analysis-----

elif select=="Player Analysis":
    st.title("Player Analysis")

    player = st.selectbox("Select Player",df["Player"])

    pdata = df[df["Player"]==player]


    df2=pdata[["100","50","6s","4s","innings","Strike_rate","Matches","Ave"]]
    
    df3=df2.T.reset_index()

    st.dataframe(df3)

    fig=px.bar(df3,x="index",y=df3.columns[1])

    df_pie=pdata[["100","50","6s","4s"]]
    pie1=df_pie.T.reset_index()
    fig_pie=px.pie(pie1,names="index",values=pie1.columns[1])

    col1,col2=st.columns(2)
    with col1:
        st.plotly_chart(fig,use_container_width=True)
    with col2:
        st.plotly_chart(fig_pie,use_container_width=True)

#--------------Country Insight------

elif select=="Country Insights":

    st.title("Country insights")


    scountry=st.selectbox("Select Country",df["Country"].unique())

    col1,col2,col3,col4=st.columns(4)

    cdata=df[df["Country"]==scountry]

    Players=cdata["Player"].nunique()
    total_runs=cdata["Runs"].sum()
    total_matches=cdata["Matches"].sum()
    total_innings=cdata["innings"].sum()

    col1.metric("Total Players",Players)
    col2.metric("Total Runs",total_runs)
    col3.metric("Total Matches",total_matches)
    col4.metric("Total Inning",total_innings)

    df2=cdata[["Player","Runs"]]

    df3=cdata[["Player","Runs","Matches","100","6s"]]

    df4=["Runs","Matches","100","6s"]

    fig=px.pie(df2,names="Player",values="Runs")

    selectc=st.selectbox("Select Choice",df4)

    fig2=px.bar(df3,x="Player",y=selectc)

    col1,col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig,use_container_width=True)

    with col2:
        st.plotly_chart(fig2,use_container_width=True)



#-----------------------Player Comparison-------
# 
# 
elif select=="Comparisons":
    st.title("Player Comparison")

    Player=st.multiselect(
        
        "Compare Players",
        df["Player"],
        default=df["Player"].head(5)
    )

    compare =df[df["Player"].isin(Player)]

    fig=px.scatter(
    compare,
    x="Strike_rate",
    y="Ave",
    size="Runs",
    color="Country",
    hover_name="Player"

    )

    st.plotly_chart(fig,use_container_width=True)

#--------------Data Explorer

elif select=="Data Explorer":
    st.title("Data Explorer")

    st.dataframe(df)
    
               