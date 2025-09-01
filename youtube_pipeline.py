import pandas as pd
from googleapiclient.discovery import build
import sqlite3
from config import API_KEY   # Import your API key

# -------------------- Extract --------------------
def get_trending_videos(region_code="US", max_results=5):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "views": int(item["statistics"].get("viewCount", 0)),
            "likes": int(item["statistics"].get("likeCount", 0)),
            "comments": int(item["statistics"].get("commentCount", 0)),
        })

    df = pd.DataFrame(videos)
    # Save CSV (optional)
    df.to_csv("data/trending_videos.csv", index=False)
    print("✅ Extracted data saved to data/trending_videos.csv")
    return df

# -------------------- Load --------------------
def load_to_db(df):
    conn = sqlite3.connect("youtube_trending.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trending_videos (
        title TEXT,
        channel TEXT,
        views INTEGER,
        likes INTEGER,
        comments INTEGER
    )
    """)

    df.to_sql("trending_videos", conn, if_exists="replace", index=False)
    print("✅ Data loaded into SQLite database: youtube_trending.db")
    conn.close()

# -------------------- Main Pipeline --------------------
if __name__ == "__main__":
    df = get_trending_videos()
    load_to_db(df)
    print("🎯 YouTube ETL Pipeline completed successfully!")

