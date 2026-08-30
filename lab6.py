import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Mini Wireshark",page_icon="🌐",layout="wide")
st.title("🌐 Mini Wireshark")
st.write("Network Packet Monitoring Dashboard")

CSV_FILE="packets.csv"
df=pd.read_csv(CSV_FILE)

st.sidebar.header("Packet Input")
source=st.sidebar.text_input("Source IP","192.168.1.100")
destination=st.sidebar.text_input("Destination IP","8.8.8.8")
protocol=st.sidebar.selectbox("Protocol",["TCP","UDP","ICMP"])
length=st.sidebar.number_input("Packet Length",min_value=1,max_value=65535,value=64)
status=st.sidebar.radio("Status",["Allowed","Blocked"])

if st.sidebar.button("Add Packet"):
    new_id=len(df)+1
    new_packet={
        "ID":new_id,
        "Source IP":source,
        "Destination IP":destination,
        "Protocol":protocol,
        "Packet Length":length,
        "Status":status
    }
    df=pd.concat([df,pd.DataFrame([new_packet])],ignore_index=True)
    df.to_csv(CSV_FILE,index=False)
    st.success("Packet added successfully!")

st.subheader("Network Statistics")
col1,col2,col3,col4=st.columns(4)

col1.metric("Total Packets",len(df))
col2.metric("TCP Packets",len(df[df["Protocol"]=="TCP"]))
col3.metric("UDP Packets",len(df[df["Protocol"]=="UDP"]))
col4.metric("Blocked Packets",len(df[df["Status"]=="Blocked"]))

st.subheader("Packet Filter")
show_blocked=st.checkbox("Show only blocked packets")

if show_blocked:
    display_df=df[df["Status"]=="Blocked"]
else:
    display_df=df

st.subheader("Captured Packets")
st.dataframe(display_df,use_container_width=True)

with st.expander("View Packet Information"):
    st.write("Source IP:",source)
    st.write("Destination IP:",destination)
    st.write("Protocol:",protocol)
    st.write("Packet Length:",length)
    st.write("Status:",status)

st.subheader("Protocol Analysis")
protocol_count=df["Protocol"].value_counts()
st.bar_chart(protocol_count)

st.subheader("CSV File")
st.write("Packet data is stored in:",CSV_FILE)
