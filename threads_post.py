import os
import time
import urllib.request
import urllib.parse
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
START_DATE = datetime(2026, 4, 17, tzinfo=JST).date()

today = datetime.now(JST).date()
day_num = (today - START_DATE).days + 1

print(f"Today is Day {day_num}")

if not (1 <= day_num <= 31):
    print("31日間の投稿期間外です。スキップします。")
    exit(0)

day_str = f"{day_num:02d}"
text_file = Path(f"posts/day{day_str}.txt")
image_file_jpg = Path(f"images/day{day_str}.jpg")
image_file_png = Path(f"images/day{day_str}.png")

REPO_RAW_BASE = "https://raw.githubusercontent.com/xingaiyuyao-commits/x-auto-post-test/main"

# 複数画像（_1〜_N）を優先
image_urls = []
for n in range(1, 11):
    p_jpg = Path(f"images/day{day_str}_{n}.jpg")
    p_png = Path(f"images/day{day_str}_{n}.png")
    if p_jpg.exists():
        image_urls.append(f"{REPO_RAW_BASE}/images/day{day_str}_{n}.jpg")
    elif p_png.exists():
        image_urls.append(f"{REPO_RAW_BASE}/images/day{day_str}_{n}.png")
    else:
        break

# 単数画像へのフォールバック
if not image_urls:
    if image_file_jpg.exists():
        image_urls.append(f"{REPO_RAW_BASE}/images/day{day_str}.jpg")
    elif image_file_png.exists():
        image_urls.append(f"{REPO_RAW_BASE}/images/day{day_str}.png")

reply_files = []
first_reply = Path(f"posts/day{day_str}_reply.txt")
if first_reply.exists():
    reply_files.append(first_reply)
    n = 2
    while True:
        pn = Path(f"posts/day{day_str}_reply{n}.txt")
        if not pn.exists():
            break
        reply_files.append(pn)
        n += 1

if not text_file.exists():
    print(f"投稿ファイルが見つかりません: {text_file}（スキップ）")
    exit(0)

TEXT = text_file.read_text(encoding="utf-8").strip()

ACCESS_TOKEN = os.environ["THREADS_ACCESS_TOKEN"]
USER_ID = os.environ["THREADS_USER_ID"]
API_BASE = "https://graph.threads.net/v1.0"


def api_request(url, params=None, method="POST"):
    if params:
        data = urllib.parse.urlencode(params).encode()
    else:
        data = None
    req = urllib.request.Request(url, data=data, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"HTTPError {e.code}: {body}")
        raise


def create_post(text, reply_to_id=None, image_urls=None):
    image_urls = image_urls or []

    if len(image_urls) >= 2:
        # カルーセル投稿: 各画像で is_carousel_item コンテナを作成 → CAROUSEL でまとめる
        children = []
        for url in image_urls:
            child = api_request(
                f"{API_BASE}/{USER_ID}/threads",
                {
                    "media_type": "IMAGE",
                    "image_url": url,
                    "is_carousel_item": "true",
                    "access_token": ACCESS_TOKEN,
                },
            )
            children.append(child["id"])
            print(f"カルーセル子コンテナ作成: {child['id']} ({url})")

        params = {
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "text": text,
            "access_token": ACCESS_TOKEN,
        }
        if reply_to_id:
            params["reply_to_id"] = reply_to_id
        result = api_request(f"{API_BASE}/{USER_ID}/threads", params)
        creation_id = result["id"]
        print(f"カルーセル親コンテナ作成: {creation_id}")
    else:
        params = {
            "text": text,
            "access_token": ACCESS_TOKEN,
        }
        if image_urls:
            params["media_type"] = "IMAGE"
            params["image_url"] = image_urls[0]
        else:
            params["media_type"] = "TEXT"
        if reply_to_id:
            params["reply_to_id"] = reply_to_id

        result = api_request(f"{API_BASE}/{USER_ID}/threads", params)
        creation_id = result["id"]
        print(f"コンテナ作成完了: {creation_id}")

    time.sleep(5)

    publish_result = api_request(
        f"{API_BASE}/{USER_ID}/threads_publish",
        {"creation_id": creation_id, "access_token": ACCESS_TOKEN},
    )
    post_id = publish_result["id"]
    return post_id


post_id = create_post(TEXT, image_urls=image_urls)
print(f"Day {day_num} Threads投稿完了。Post ID: {post_id}（画像: {len(image_urls)}枚）")

last_id = post_id
for i, rf in enumerate(reply_files, 1):
    REPLY_TEXT = rf.read_text(encoding="utf-8").strip()
    last_id = create_post(REPLY_TEXT, reply_to_id=last_id)
    print(f"リプライ{i} 投稿完了。Reply ID: {last_id}")
