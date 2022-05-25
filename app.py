import os
from flask import Flask
from flask import request

import asyncio
import aiohttp
import aiofiles

app = Flask(__name__)


async def fetch_data(session, item):
    """Fetch the specified URL's data using the aiohttp session specified."""
    response = await session.get(item["url"])
    async with aiofiles.open(os.path.join(os.getcwd(), 'downloads', f'{item["name"]}.txt'), mode='w') as f:
        file_context = await response.json()
        await f.writelines(str(file_context))
    return {'url': response.url, 'status': response.status}


@app.route("/save-data", methods=['POST'])
async def save_data():
    data = request.json
    async with aiohttp.ClientSession() as session:
        tasks = []
        for item in data:
            task = asyncio.create_task(fetch_data(session, item))
            tasks.append(task)
        sites = await asyncio.gather(*tasks)

    response = '<h1>URLs:</h1>'
    for site in sites:
        response += f"<p>URL: {site['url']} --- Status Code: {site['status']}</p>"

    return response

if __name__ == '__main__':
    app.run(debug=True)
