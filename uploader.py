import os
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.http

def upload_to_youtube():
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not client_id or not client_secret or not refresh_token:
        print("ERROR: Missing YouTube Secrets! Check YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET, and YOUTUBE_REFRESH_TOKEN in Repository Secrets.")
        raise ValueError("YouTube API credentials incomplete.")

    credentials = google.oauth2.credentials.Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret
    )

    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

    video_title = "Crazy Mind-Blowing Fact! #shorts #facts"
    if os.path.exists("script.txt"):
        with open("script.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            if lines:
                video_title = lines[0].strip()[:60] + " #shorts #facts"

    request_body = {
        "snippet": {
            "title": video_title,
            "description": "Mind blowing viral facts explained! Subscribe for more daily videos!\n\n#shorts #viral #trending #facts #mindblowingfacts #interestingfacts #didyouknow #shortsfeed",
            "tags": [
                "shorts", 
                "viral", 
                "trending", 
                "facts", 
                "mind blowing facts", 
                "interesting facts", 
                "did you know", 
                "shorts feed"
            ],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }

    video_file = "final_output.mp4"
    if not os.path.exists(video_file):
        raise FileNotFoundError(f"Video file '{video_file}' not found. Make sure video_builder.py runs successfully.")

    media = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    
    print("Uploading video to YouTube Shorts...")
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )
    
    response = request.execute()
    print(f"SUCCESS: Video uploaded successfully! Video ID: {response.get('id')}")

if __name__ == "__main__":
    upload_to_youtube()
