import os
from urllib.parse import urlparse
from flask import Flask, request, redirect

app = Flask(__name__)

PROXY_PREFIX = os.getenv("PROXY_PREFIX")
ALLOWED_HOSTS = os.getenv("URLPDOMAINS")
HOST = os.getenv("URLPHOST", "::")
PORT = int(os.getenv("URLPPORT", 5000))
ROUTE = "/" + os.getenv("URLPROUTE", "")

# 处理白名单
ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS.split(",") if h.strip()]

if not PROXY_PREFIX:
    raise ValueError("PROXY_PREFIX 环境变量未设置")


def is_allowed(url):
    """检查是否在白名单"""
    parsed = urlparse(url)
    return parsed.hostname in ALLOWED_HOSTS


def transform_url(original_url):
    """转换 URL"""
    if original_url.startswith("https://"):
        return "https/" + original_url[len("https://"):]
    elif original_url.startswith("http://"):
        return "http/" + original_url[len("http://"):]
    else:
        raise ValueError("仅支持 http 或 https 协议")


@app.route(ROUTE)
def proxy():
    url = request.args.get("url")

    if not url:
        return {"error": "missing url parameter"}, 400

    # 白名单校验
    if not is_allowed(url):
        return {"error": "host not allowed"}, 403

    try:
        transformed = transform_url(url)
    except ValueError as e:
        return {"error": str(e)}, 400

    final_url = PROXY_PREFIX.rstrip("/") + "/" + transformed

    return redirect(final_url, code=302)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
