FROM python:alpine
RUN pip install requests flask beautifulsoup4
ENV URLPPORT=5000 URLPIP="::"
WORKDIR /app/
CMD [ "python3","main.py" ]