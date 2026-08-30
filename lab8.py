import pandas as pd
import numpy as np

df = pd.read_csv("packets.csv")

print("\n1. Complete Dataset")
print(df)

print("\n2. Source IP, Destination IP and Protocol")
print(df[["Source IP", "Destination IP", "Protocol"]])

print("\n3. First 5 Records")
print(df.iloc[:5])

print("\n4. Packets with Packet Length > 500")
print(df[df["Packet Length"] > 500])

print("\n5. TCP Packets with Packet Length > 1000")
print(df[(df["Protocol"] == "TCP") & (df["Packet Length"] > 1000)])

df["AdjustedSize"] = df["Packet Length"] + 20

print("\n6. Dataset with AdjustedSize")
print(df)


def assign_priority(size):

    if pd.isna(size):
        return np.nan
    elif size >= 1200:
        return "High"
    elif size >= 800:
        return "Medium"
    elif size >= 400:
        return "Low"
    else:
        return "Very Low"


df["Priority"] = df["Packet Length"].apply(assign_priority)

print("\n7. Dataset with Priority")
print(df)

print("\n8. Missing Values")
print(df.isnull())

print("\nMissing Values Count")
print(df.isnull().sum())

mean_size = df["Packet Length"].mean()

df["Packet Length"] = df["Packet Length"].fillna(mean_size)

print("\n9. Packet Length after Filling Missing Values")
print(df)

df["Status"] = df["Status"].fillna("Captured")

print("\n10. Status after Filling Missing Values")
print(df)

sorted_df = df.sort_values(
    by="Packet Length",
    ascending=False
)

print("\n11. Sorted by Packet Length")
print(sorted_df)

print("\n12. Average Packet Length by Protocol")
print(df.groupby("Protocol")["Packet Length"].mean())

df = df.drop_duplicates()

print("\n13. Dataset after Removing Duplicates")
print(df)