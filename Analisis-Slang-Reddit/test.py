import requests
from datetime import datetime

# Set the time range for 2022
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)

# Convert to Unix timestamps
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# Reddit API endpoint for searching posts
url = f"https://api.reddit.com/r/memes/search?q=timestamp:{start_timestamp}..{end_timestamp}&sort=desc&limit=5"

# Make the API request
headers = {'User-Agent': 'my-reddit-app'}
response = requests.get(url, headers=headers)

# Parse the response
if response.status_code == 200:
    posts = response.json()['data']['children']
    for post in posts:
        print(f"Title: {post['data']['title']}")
        print(f"Score: {post['data']['score']}")
        print(f"URL: {post['data']['url']}")
        print(f"Date: {datetime.utcfromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Text: {post['data']['selftext']}")
        print('-' * 80)
else:
    print("Error fetching data")
