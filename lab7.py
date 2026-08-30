import streamlit as st
import re
import os
import shutil

FILE="packets.txt"
BACKUP="packets_backup.txt"

def create_file():
    records=[
        "1,192.168.1.10,8.8.8.8,TCP,443,Allowed\n",
        "2,192.168.1.20,8.8.4.4,UDP,53,Allowed\n",
        "3,10.0.0.5,10.0.0.1,ICMP,0,Blocked\n",
        "4,192.168.1.15,1.1.1.1,TCP,80,Allowed\n",
        "5,172.16.0.5,172.16.0.10,UDP,53,Blocked\n",
        "6,192.168.1.25,142.250.182.14,TCP,443,Allowed\n",
        "7,10.10.10.5,10.10.10.1,ICMP,0,Allowed\n",
        "8,192.168.2.10,8.8.8.8,TCP,22,Blocked\n"
    ]
    with open(FILE,"w") as f:
        f.writelines(records)

def read_records():
    try:
        with open(FILE,"r") as f:
            records=f.readlines()
        return records
    except FileNotFoundError:
        return []

def append_record(record):
    with open(FILE,"a") as f:
        f.write(record+"\n")

def search_record(packet_id):
    records=read_records()
    for record in records:
        data=record.strip().split(",")
        if data[0]==packet_id:
            return data
    return None

def update_record(packet_id,new_record):
    records=read_records()
    found=False
    with open(FILE,"w") as f:
        for record in records:
            data=record.strip().split(",")
            if data[0]==packet_id:
                f.write(new_record+"\n")
                found=True
            else:
                f.write(record)
    return found

def delete_record(packet_id):
    records=read_records()
    found=False
    with open(FILE,"w") as f:
        for record in records:
            data=record.strip().split(",")
            if data[0]==packet_id:
                found=True
            else:
                f.write(record)
    return found

def backup_file():
    shutil.copy(FILE,BACKUP)

def valid_ip(ip):
    pattern=r"^(\d{1,3}\.){3}\d{1,3}$"
    return re.match(pattern,ip) is not None

def display_records():
    records=read_records()
    if not records:
        st.warning("No records found.")
        return
    st.write("ID | Source IP | Destination IP | Protocol | Port | Status")
    st.write("---")
    for record in records:
        st.write(record.strip())

st.title("🌐 Network Packet File Management System")
st.write("Mini Wireshark - File Handling Application")

if not os.path.exists(FILE):
    create_file()

option=st.sidebar.selectbox(
    "Select Operation",
    [
        "View Records",
        "Add Packet",
        "Search Packet",
        "Update Packet",
        "Delete Packet",
        "Backup File",
        "File Operations Demo"
    ]
)

if option=="View Records":
    st.header("All Packet Records")
    display_records()

elif option=="Add Packet":
    st.header("Add New Packet")
    packet_id=st.text_input("Packet ID")
    source=st.text_input("Source IP")
    destination=st.text_input("Destination IP")
    protocol=st.selectbox("Protocol",["TCP","UDP","ICMP"])
    port=st.number_input("Port",min_value=0,max_value=65535,value=80)
    status=st.radio("Status",["Allowed","Blocked"])

    if st.button("Add Packet"):
        if packet_id=="":
            st.error("Packet ID is required.")
        elif not valid_ip(source):
            st.error("Invalid Source IP.")
        elif not valid_ip(destination):
            st.error("Invalid Destination IP.")
        elif search_record(packet_id):
            st.error("Packet ID already exists.")
        else:
            record=f"{packet_id},{source},{destination},{protocol},{port},{status}"
            append_record(record)
            st.success("Packet added successfully!")

elif option=="Search Packet":
    st.header("Search Packet")
    packet_id=st.text_input("Enter Packet ID")

    if st.button("Search"):
        result=search_record(packet_id)
        if result:
            st.success("Packet found!")
            st.write("Packet ID:",result[0])
            st.write("Source IP:",result[1])
            st.write("Destination IP:",result[2])
            st.write("Protocol:",result[3])
            st.write("Port:",result[4])
            st.write("Status:",result[5])
        else:
            st.error("Packet not found.")

elif option=="Update Packet":
    st.header("Update Packet")
    packet_id=st.text_input("Packet ID to update")
    source=st.text_input("New Source IP")
    destination=st.text_input("New Destination IP")
    protocol=st.selectbox("New Protocol",["TCP","UDP","ICMP"])
    port=st.number_input("New Port",min_value=0,max_value=65535,value=80)
    status=st.radio("New Status",["Allowed","Blocked"])

    if st.button("Update"):
        if not valid_ip(source):
            st.error("Invalid Source IP.")
        elif not valid_ip(destination):
            st.error("Invalid Destination IP.")
        else:
            new_record=f"{packet_id},{source},{destination},{protocol},{port},{status}"
            if update_record(packet_id,new_record):
                st.success("Packet updated successfully!")
            else:
                st.error("Packet not found.")

elif option=="Delete Packet":
    st.header("Delete Packet")
    packet_id=st.text_input("Packet ID")

    if st.button("Delete"):
        if delete_record(packet_id):
            st.success("Packet deleted successfully!")
        else:
            st.error("Packet not found.")

elif option=="Backup File":
    st.header("Backup")

    if st.button("Create Backup"):
        try:
            backup_file()
            st.success("Backup created successfully!")
        except FileNotFoundError:
            st.error("Data file does not exist.")

elif option=="File Operations Demo":
    st.header("File Handling Demonstration")

    try:
        f=open(FILE,"r+")
        st.write("File opened using: r+")
        position=f.tell()
        st.write("Current position:",position)
        content=f.read()
        st.text_area("read() output",content,height=200)
        f.seek(0)
        st.write("After seek(0), position:",f.tell())
        first_line=f.readline()
        st.write("readline() output:",first_line)
        f.close()
        st.success("File closed successfully.")
    except Exception as e:
        st.error("File error: "+str(e))
