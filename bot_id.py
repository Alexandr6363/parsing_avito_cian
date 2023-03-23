import requests
TOKEN = "YOUR TELEGRAM BOT TOKEN"
url = f"https://api.telegram.org/bot6014244326:AAFFrfTXtQ8QUbbLf9I7MbDeFffAkFY6cfw/getUpdates"
print(requests.get(url).json())