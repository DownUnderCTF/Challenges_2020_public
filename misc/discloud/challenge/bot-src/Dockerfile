FROM node:14

RUN useradd -ms /bin/bash discord

WORKDIR /home/discord/app
COPY package.json package*.json ./
RUN chown -R discord:discord /home/discord/app

USER discord

# COPY package.json package*.json ./
RUN npm install --only=production
COPY index.js bucket.js parse.js ./
CMD ["npm", "start"]