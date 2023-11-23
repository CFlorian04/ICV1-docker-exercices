FROM node:14

WORKDIR /app

RUN npm install
RUN npm install ip

COPY . .

ENV PORT 4567
EXPOSE ${PORT}

CMD ["node", "serverPing.js"]
