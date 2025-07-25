#import httpx  Для прокси
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv('AI_TOKEN'))
''', Для прокси
                        http_client=httpx.AsyncClient(
                        proxies=os.getenv('PROXY'),
                        transport=httpx.HTTPTransport(local_address="0.0.0.0")
                    ))'''

async def ask_gpt(question):
    response = await client.chat.completions.create(
        messages=[{"role": "user",
                  "content": str(question)}],
        model="gpt-3.5-turbo"
    )

    return response