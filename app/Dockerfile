FROM node:6

WORKDIR /urs/src/app

COPY package.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "seeds/seed.js"]

CMD ["node", "app.js"]
