FROM python:alpine
RUN pip install requests flask beautifulsoup4
ENV URLPPORT=5000 URLPHOST="::" URLPDOMAINS="lain.bgm.tv" URL_PROXY_PREFIX="" URLPROUTE=""
WORKDIR /app/
COPY app.py app.py
CMD [ "python3","app2.py" ]