import os
import tweepy
import json
from datetime import datetime

client = tweepy.Client(
    consumer_key=os.environ["X_API_KEY"],
    consumer_secret=os.environ["X_API_KEY_SECRET"],
    access_token=os.environ["X_ACCESS_TOKEN"],
    access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
)

me = client.get_me()
if me.data is None:
    print("ERROR: get_me() returned no data")
    exit(1)

user_id = me.data.id
username = me.data.username
print(f"=== Analyzing @{username} (ID: {user_id}) ===")
print()

try:
    resp = client.get_users_tweets(
        id=user_id,
        max_results=100,
        tweet_fields=["public_metrics", "created_at", "text", "non_public_metrics", "organic_metrics"],
        exclude=["retweets", "replies"],
    )
except tweepy.errors.TweepyException as e:
    print(f"Fetch error (trying without non_public_metrics): {e}")
    resp = client.get_users_tweets(
        id=user_id,
        max_results=100,
        tweet_fields=["public_metrics", "created_at", "text"],
        exclude=["retweets", "replies"],
    )

if not resp.data:
    print("No tweets found")
    exit(0)

tweets = resp.data
print(f"Fetched {len(tweets)} tweets")
print()

scored = []
for t in tweets:
    m = t.public_metrics or {}
    score = m.get("like_count", 0) + m.get("retweet_count", 0) * 2 + m.get("reply_count", 0)
    scored.append({
        "score": score,
        "likes": m.get("like_count", 0),
        "rt": m.get("retweet_count", 0),
        "reply": m.get("reply_count", 0),
        "quote": m.get("quote_count", 0),
        "impression": m.get("impression_count", 0),
        "date": t.created_at.strftime("%Y-%m-%d %H:%M") if t.created_at else "?",
        "text": t.text,
        "id": t.id,
    })

scored.sort(key=lambda x: x["score"], reverse=True)

print("=== TOP 20 POSTS (by likes + RT*2 + replies) ===")
print()
for i, s in enumerate(scored[:20], 1):
    print(f"--- #{i} | Score: {s['score']} ---")
    print(f"Likes: {s['likes']} | RT: {s['rt']} | Reply: {s['reply']} | QT: {s['quote']} | Imp: {s['impression']}")
    print(f"Date: {s['date']}")
    print(f"URL: https://x.com/{username}/status/{s['id']}")
    print(f"Text:\n{s['text']}")
    print()

total_likes = sum(s["likes"] for s in scored)
total_rt = sum(s["rt"] for s in scored)
total_reply = sum(s["reply"] for s in scored)
total_imp = sum(s["impression"] for s in scored)
print("=== TOTALS ===")
print(f"Total tweets: {len(scored)}")
print(f"Total likes: {total_likes} (avg {total_likes/len(scored):.1f})")
print(f"Total RT: {total_rt} (avg {total_rt/len(scored):.1f})")
print(f"Total replies: {total_reply} (avg {total_reply/len(scored):.1f})")
print(f"Total impressions: {total_imp} (avg {total_imp/len(scored):.1f})")

with open("analysis_output.json", "w", encoding="utf-8") as f:
    json.dump({"username": username, "tweets": scored}, f, ensure_ascii=False, indent=2)
print()
print("Saved to analysis_output.json")
