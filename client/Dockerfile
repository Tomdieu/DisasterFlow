FROM node:node:20.11.0-alpine3.19

WORKDIR /client

COPY package*.json ./

RUN npm install

EXPOSE 3000

CMD npm run dev