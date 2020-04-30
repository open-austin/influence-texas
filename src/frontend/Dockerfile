FROM node:12.14.1
RUN mkdir /usr/src/frontend
RUN mkdir -p /usr/src/influencetx/static
WORKDIR /usr/src/frontend
COPY package.json /usr/src/frontend/package.json
COPY package-lock.json /usr/src/frontend/package-lock.json
RUN npm install --silent
COPY . .
CMD npm run build

# use 'PUBLIC_URL' if the built version is not finding its assets, EX:
# CMD PUBLIC_URL="http://localhost:5120/static/react-app" npm run build
