FROM alpine:latest
RUN apk add --no-cache python3-dev
RUN pip3 install --upgrade pip
WORKDIR /comp9322chatbot
COPY ./comp9322chatbot /comp9322chatbot
RUN pip3 install -r requirements.txt
EXPOSE 5000
WORKDIR /comp9322chatbot
CMD python3 app.py