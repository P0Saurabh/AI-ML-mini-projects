import discord
import requests
import os
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    fetch_tech_news.start()

@tasks.loop(minutes=1)
async def fetch_tech_news():
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    url = f'https://newsapi.org/v2/everything?q=computer+science+OR+IT+student+education+beneficial&apiKey={NEWSAPI_KEY}'
                    response = requests.get(url)
                    response.raise_for_status()
                    news = response.json()

                    print(f"Response status code: {response.status_code}")
                    print(f"Response JSON: {news}")

                    articles = news.get('articles', [])
                    if articles:
                        await channel.send('Here are the latest news articles beneficial for IT and CSE students:')
                        for article in articles[:5]:
                            summary = article.get('description', 'No description available.')
                            await channel.send(f"{article['title']}\n{summary}\n{article['url']}")
                    else:
                        await channel.send('No relevant news found!')
                except requests.RequestException as e:
                    await channel.send('Failed to fetch news!')
                    print(f'Error fetching news: {e}')
                break

client.run(DISCORD_TOKEN)
