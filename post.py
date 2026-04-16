import tweepy
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
START_DATE = datetime(2026, 4, 15, tzinfo=JST).date()  # Day 1 の日付

today = datetime.now(JST).date()
day_num = (today - START_DATE).days + 1

print(f"Today is Day {day_num}")

if not (1 <= day_num <= 31):
    print("31日間の投稿期間外です。スキップします。")
    exit(0)

day_str = f"{day_num:02d}"
text_file = Path(f"posts/day{day_str}.txt")
reply_file = Path(f"posts/day{day_str}_reply.txt")
image_file_jpg = Path(f"images/day{day_str}.jpg")
image_file_png = Path(f"images/day{day_str}.png")

if not text_file.exists():
    print(f"投稿ファイルが見つかりません: {text_file}")
    exit(1)

TEXT = text_file.read_text(encoding="utf-8").strip()

# 画像ファイルの確認
image_path = None
if image_file_jpg.exists():
    image_path = image_file_jpg
elif image_file_png.exists():
    image_path = image_file_png

# Tweepy クライアント（v2）
client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_KEY_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)

# 画像アップロード（v1.1 API が必要）
media_ids = None
if image_path:
    auth = tweepy.OAuth1UserHandler(
        os.environ["X_API_KEY"],
        os.environ["X_API_KEY_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )
    api_v1 = tweepy.API(auth)
    media = api_v1.media_upload(filename=str(image_path))
    media_ids = [media.media_id]
    print(f"画像アップロード完了: {image_path} (media_id: {media.media_id})")

# 本文を投稿
tweet = client.create_tweet(text=TEXT, media_ids=media_ids)
tweet_id = tweet.data["id"]
print(f"Day {day_num} 投稿完了。Tweet ID: {tweet_id}")

# リプライがあれば投稿
if reply_file.exists():
    REPLY_TEXT = reply_file.read_text(encoding="utf-8").strip()
    reply = client.create_tweet(
        text=REPLY_TEXT,
        in_reply_to_tweet_id=tweet_id,
    )
    print(f"リプライ投稿完了。Reply ID: {reply.data['id']}")
