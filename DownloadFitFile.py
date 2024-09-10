

from fitparse import FitFile
import pandas as pd
import matplotlib.pyplot as plt

# Load the FIT file
fitfile = FitFile('FitFiles\91301803.fit')

# Extract relevant data
records = []
for record in fitfile.get_messages('record'):
    records.append(record.get_values())

# Convert to DataFrame
df = pd.DataFrame(records)

for col in df.columns:
    print(col)

# Convert timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Set timestamp as index
df.set_index('timestamp', inplace=True)

# Plot heart rate over time
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['heart_rate'])
plt.title('Heart Rate Over Time')
plt.xlabel('Time')
plt.ylabel('Heart Rate (bpm)')
plt.grid(True)

plt.draw()
plt.pause(0.001)


# Create a scatter plot of speed vs. heart rate
plt.figure(figsize=(10, 6))
plt.scatter(df['speed'], df['heart_rate'], alpha=0.5)
plt.title('Speed vs. Heart Rate')
plt.xlabel('Speed (m/s)')
plt.ylabel('Heart Rate (bpm)')
plt.grid(True)

# After each plot
plt.draw()
plt.pause(0.001)

plt.show()



