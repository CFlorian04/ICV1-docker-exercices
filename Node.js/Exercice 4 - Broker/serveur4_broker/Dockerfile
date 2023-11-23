FROM node:14

WORKDIR /app

RUN npm install
RUN npm install ip

COPY . .

ENV PORT 1111
EXPOSE ${PORT}

CMD ["node", "serverBroker.js"]
