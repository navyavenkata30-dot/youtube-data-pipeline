import sqlite3
import pandas as pd

# Load CSV
df = pd.read_csv("data/trending_videos.csv")

# Connect/create SQLite database
conn = sqlite3.connect("youtube_trending.db")
cursor = conn.cursor()

# Create table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS trending_videos (
    title TEXT,
    channel TEXT,
    views INTEGER,
    likes INTEGER,
    comments INTEGER
)
""")

# Load data into the table
df.to_sql("trending_videos", conn, if_exists="replace", index=False)

print("✅ Data loaded into SQLite database: youtube_trending.db")

# Close connection
conn.close()

