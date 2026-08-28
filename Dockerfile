FROM python:alpine
RUN pip install requests flask beautifulsoup4
ENV URLPPORT=5000 URLPIP="::" URLPDOMAINS="lain.bgm.tv"
WORKDIR /app/
COPY app.py app.py
CMD [ "python3","app.py" ]