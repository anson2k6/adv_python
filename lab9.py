import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("packets.csv")

print("NETWORK PACKET DATA")
print(df)

packet_lengths = np.array(df["Packet Length"])

print("\n--- NUMPY COMPUTATION ---")

print("Packet lengths:")
print(packet_lengths)

new_lengths = packet_lengths + 10

print("\nPacket lengths after adding 10:")
print(new_lengths)

print("\n--- AGGREGATIONS ---")

print("Total packet size:", np.sum(packet_lengths))

print("Mean packet size:", np.mean(packet_lengths))

print("Median packet size:", np.median(packet_lengths))

print("Standard deviation:", np.std(packet_lengths))

print("Minimum packet size:", np.min(packet_lengths))

print("Maximum packet size:", np.max(packet_lengths))

print("Variance:", np.var(packet_lengths))


print("\n--- COMPUTATION ON ARRAYS ---")

print("Packet size × 2:")
print(packet_lengths * 2)

print("\nPacket size / 2:")
print(packet_lengths / 2)

print("\nPacket size squared:")
print(packet_lengths ** 2)


print("\n--- COMPARISONS AND MASKS ---")

mask = packet_lengths > 500

print("Mask:")
print(mask)

print("\nPackets larger than 500 bytes:")

print(df[mask])

mask2 = (packet_lengths >= 100) & (packet_lengths <= 500)

print("\nPackets between 100 and 500 bytes:")

print(df[mask2])


print("\n--- BOOLEAN ARRAY ---")

tcp_mask = df["Protocol"].values == "TCP"

print("TCP mask:")
print(tcp_mask)

print("\nNumber of TCP packets:")
print(np.sum(tcp_mask))

print("\n--- FANCY INDEXING ---")

indexes = [0, 3, 5, 8]

selected = packet_lengths[indexes]

print("Selected indexes:", indexes)

print("Selected packet lengths:", selected)


print("\n--- SORTING ---")

sorted_lengths = np.sort(packet_lengths)

print("Original:")
print(packet_lengths)

print("\nSorted:")
print(sorted_lengths)

print("\nDescending:")
print(sorted_lengths[::-1])


print("\n--- PROTOCOL ANALYSIS ---")

protocol_counts = df["Protocol"].value_counts()

print(protocol_counts)

plt.figure()

protocol_counts.plot(kind="bar")

plt.title("Number of Packets by Protocol")

plt.xlabel("Protocol")

plt.ylabel("Number of Packets")

plt.tight_layout()

plt.show()


plt.figure()

plt.plot(df["ID"], df["Packet Length"], marker="o")

plt.title("Packet Length Analysis")

plt.xlabel("Packet ID")

plt.ylabel("Packet Length")

plt.grid()

plt.show()

plt.figure()

plt.hist(packet_lengths, bins=5)

plt.title("Distribution of Packet Lengths")

plt.xlabel("Packet Length")

plt.ylabel("Frequency")

plt.show()