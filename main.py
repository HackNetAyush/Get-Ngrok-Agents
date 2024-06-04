import os
from aiohttp import web
import json
import ngrok

# Retrieve the ngrok auth token from environment variables
ngrok_auth_token = os.getenv("NGROK_AUTH_TOKEN")

# Ensure the auth token is available
if not ngrok_auth_token:
    raise ValueError("NGROK_AUTH_TOKEN environment variable not set")

client = ngrok.Client(ngrok_auth_token)

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')

def json_response(url):
    return web.Response(text=json.dumps({"ngrok_url": url}), content_type='application/json')

class Handler:

    def __init__(self):
        self.store = {}
        self.headers = {'Access-Control-Allow-Origin': '*'}

    async def get_link(self, request):
        url = None
        for t in client.tunnels.list():
            url = str(t.public_url)
            print(t.public_url)
            break  # Assuming you want the first tunnel's URL

        if url:
            return json_response(url)
        else:
            return web.Response(text=json.dumps({"error": "No active tunnels found"}), content_type='application/json')

def main():
    web.run_app(app)

handler = Handler()
app = web.Application()
app.add_routes([
    web.get('/', handler.get_link)
])

if __name__ == '__main__':
    main()
