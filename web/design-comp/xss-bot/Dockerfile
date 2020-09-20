FROM node:14.9-stretch-slim as base
FROM base as build

RUN mkdir /build
WORKDIR /build

COPY package.json package.json
COPY package-lock.json package-lock.json
RUN npm install

COPY tsconfig.json tsconfig.json
COPY src src/
RUN npx tsc

FROM base as dist

RUN apt update \
 && apt install -y wget gnupg ca-certificates \
 && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
 && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
 && apt update \
 && apt install -y google-chrome-stable libxss1 \
 && apt remove -y google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
COPY --from=build /build/node_modules/ /app/node_modules/
COPY --from=build /build/build/ /app/src

RUN groupadd xssbot \
 && useradd -g xssbot xssbot \
 && chown -R xssbot:xssbot /app \
 && chown root:root /app/node_modules/puppeteer/.local-chromium/linux-*/chrome-linux/chrome_sandbox \
 && chmod 4755 /app/node_modules/puppeteer/.local-chromium/linux-*/chrome-linux/chrome_sandbox \
 && cp -p /app/node_modules/puppeteer/.local-chromium/linux-*/chrome-linux/chrome_sandbox /usr/local/sbin/chrome-devel-sandbox

ENV CHROME_DEVEL_SANDBOX=/usr/local/sbin/chrome-devel-sandbox

EXPOSE 80/tcp
ENTRYPOINT ["node"]
CMD ["src/api.js"]