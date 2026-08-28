from flask import Flask, request, redirect
import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
BASE_URL = "https://siteproxy.ai"


def check_url(url: str):
    if not url:
        return False

    parsed = urlparse(url)
    host = parsed.netloc.lower()

    # 去掉端口
    host = host.split(":")[0]

    if host not in ALLOWED_DOMAINS:
        raise ValueError(f"Blocked domain: {host}")

    return True


@app.route("/api/proxy")
def proxy():
    input_url = request.args.get("input")

    try:
        check_url(input_url)
    except Exception as e:
        return str(e), 403

    session = requests.Session()

    headers = {"User-Agent": USER_AGENT}

    # 第一次请求拿 token
    resp = session.get(BASE_URL, headers=headers)
    token = re.search(r'initialToken\\":\\"(.*?)\\"', resp.text)

    if not token:
        return "no token"

    headers.update({
        "origin": BASE_URL,
        "referer": BASE_URL,
        "x-stats-id": token.group(1),
    })

    # 第二次请求
    resp = session.post(
        f"{BASE_URL}/api/servers",
        headers=headers,
        data={"input": input_url}
    )

    soup = BeautifulSoup(resp.text, "html.parser").find(
        "meta", attrs={"http-equiv": "x-refresh"}
    )

    if not soup:
        return "no redirect"

    return redirect(soup.get("content"), code=302)


if __name__ == "__main__":
    ALLOWED_DOMAINS = set(os.getenv("URLPDOMAINS", "lain.bgm.tv").split(","))
    port = int(os.getenv("URLPPORT", 5000))
    ip = os.getenv("URLPIP", "::")
    app.run(host=ip, port=port)
