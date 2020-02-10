FROM node:12.14.1
RUN mkdir /usr/src/frontend
RUN mkdir -p /usr/src/influencetx/static
WORKDIR /usr/src/frontend
COPY package.json /usr/src/frontend/package.json
COPY package-lock.json /usr/src/frontend/package-lock.json
RUN npm install --silent
COPY . .
RUN npm run build
