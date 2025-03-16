import praw
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Reddit API credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

# Inisialisasi Reddit API dengan PRAW
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# Pilih subreddit yang ingin diambil datanya
subreddit_name = 'memes'  # Ganti dengan subreddit yang kamu inginkan
subreddit = reddit.subreddit(subreddit_name)

# Tentukan tanggal awal untuk tahun 2022
start_timestamp = datetime(2019, 1, 1).timestamp()

# Cetak start_timestamp untuk memeriksa apakah nilainya sesuai
print("Start Timestamp for 2022-01-01:", start_timestamp)

# Ambil 5 postingan top dalam waktu "all" (semua waktu) dan filter berdasarkan tahun
for submission in subreddit.top(time_filter='all', limit=5):  # Ambil 5 postingan teratas
    # Cetak timestamp untuk debugging
    print(f"Submission created_utc: {submission.created_utc}")
    
    # Filter postingan yang dibuat setelah 1 Januari 2022
    if submission.created_utc >= start_timestamp:
        # Konversi timestamp menjadi waktu yang dapat dibaca
        submission_time = datetime.fromtimestamp(submission.created_utc, timezone.utc)
        
        # Cetak detail postingan jika tersedia
        print("Title:", submission.title if submission.title else "No title")
        print("Score:", submission.score if submission.score else "No score")
        print("URL:", submission.url if submission.url else "No URL")
        print("Date:", submission_time.strftime('%Y-%m-%d %H:%M:%S'))
        print("Text:", submission.selftext if submission.selftext else "No text")
        print('-' * 80)
