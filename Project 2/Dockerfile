FROM python:3.10.11
ENV HOME /root
WORKDIR /root
COPY . .
# Download dependancies
RUN pip3 install -r requirements.txt
EXPOSE 8000
#Add this for MongoDB
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python3 -u web.py