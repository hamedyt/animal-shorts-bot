import requests
import re
import os
import subprocess
import time
from telegram import Bot

# تنظیمات
TELEGRAM_BOT_TOKEN = '7437180246:AAG0jQCLc7zL3XltxPK_3SJw0r6vfWX_qSQ'
TELEGRAM_CHANNEL_ID = '@hamedshortbot'
SEARCH_QUERY = 'funny animals'
MAX_RESULTS = 10

def get_youtube_shorts_links(query, count=10):
    q = query.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={q}&sp=EgIYAQ%253D%253D"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    matches = re.findall(r'/shorts/[a-zA-Z0-9_-]{11}', res.text)
    return ['https://www.youtube.com' + link for link in list(dict.fromkeys(matches))[:count]]

def download_video(url, output_path):
    subprocess.run(['yt-dlp', '-f', 'mp4', '--output', output_path, url])
    return os.path.exists(output_path)

def send_video_to_telegram(token, channel, path):
    bot = Bot(token=token)
    with open(path, 'rb') as f:
        bot.send_video(chat_id=channel, video=f)

def main():
    links = get_youtube_shorts_links(SEARCH_QUERY, MAX_RESULTS)
    for i, url in enumerate(links, 1):
        filename = f'video_{i}.mp4'
        print(f"Downloading: {url}")
        if download_video(url, filename):
            print(f"Sending to Telegram: {filename}")
            send_video_to_telegram(TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID, filename)
            time.sleep(5)
            os.remove(filename)
        else:
            print(f"Failed to download: {url}")

if __name__ == '__main__':
    main()
