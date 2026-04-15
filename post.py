import tweepy
import os

TEXT = """Xに今日から戻ってきます。

これから31日間、
毎日20時に発信します。

試験英語は得意、でも話せない人、
発音で心が折れた人、
一度英語を諦めた人、

どこかで誰かの背中を押せたらいいな。

フォローして待っててください🔥"""

client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_KEY_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)
r = client.create_tweet(text=TEXT)
print(f"Posted Day 1. Tweet ID: {r.data['id']}")
