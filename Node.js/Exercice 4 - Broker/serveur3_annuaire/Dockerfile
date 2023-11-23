FROM node:14

WORKDIR /app

RUN npm install
RUN npm install ip

COPY . .

ENV PORT 8080
EXPOSE ${PORT}

CMD ["node", "serverAnnuaire.js"]
