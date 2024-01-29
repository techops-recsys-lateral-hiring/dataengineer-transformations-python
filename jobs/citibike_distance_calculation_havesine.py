import pandas as pd
import math

# Haversine formula to calculate distance between two lat/long points
def haversine(lat1, lon1, lat2, lon2):
      R = 6371.0  # Earth radius in kilometers

      lat1_rad = math.radians(lat1)
      lon1_rad = math.radians(lon1)
      lat2_rad = math.radians(lat2)
      lon2_rad = math.radians(lon2)

      dlat = lat2_rad - lat1_rad
      dlon = lon2_rad - lon1_rad
      a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# c is the angular distance between two points (in radians), 
# and a is the square of half the chord length between two points

      distance = R * c
      return distance

  # Load the CSV file
file_name = 'citibike.csv' 
df = pd.read_csv(file_name)

# Apply the Haversine formula to each row
df['distance_km'] = df.apply(
    lambda row: haversine(row['start station latitude'], row['start station longitude'],
                          row['end station latitude'], row['end station longitude']), 
    axis=1
)

# Output the first few rows to check
print(df.head())

# Optional: Save the result back to a new CSV file
df.to_csv('distance_haversine_citibike.csv', index=False)
