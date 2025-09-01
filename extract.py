import pandas as pd
from googleapiclient.discovery import build
from config import API_KEY   # Import your real key

def get_trending_videos(region_code="US", max_results=5):
    try:
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
        # Optional: save to CSV
        df.to_csv("data/trending_videos.csv", index=False)
        print("✅ Data fetched and saved to data/trending_videos.csv")
        return df

    except Exception as e:
        print("❌ Error fetching data:", e)
        return pd.DataFrame()

if __name__ == "__main__":
    df = get_trending_videos()
    print(df)

