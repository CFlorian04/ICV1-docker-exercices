FROM node:14

WORKDIR /app

RUN npm install
RUN npm install ip

COPY . .

ENV PORT 5372
EXPOSE ${PORT}

CMD ["node", "serverPong.js"]
