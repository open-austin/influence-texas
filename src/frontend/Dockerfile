# base image
FROM node:9.6.1

# set working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# add `/usr/src/app/node_modules/.bin` to $PATH
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install and cache app dependencies
COPY package.json /usr/src/app/package.json
RUN npm install --silent
RUN npm install react-scripts@1.1.1 -g --silent

VOLUME /usr/src/app/build/static
VOLUME /usr/src/app/node_modules

# run react app in development mode
CMD npm start

# run react app to generate static content at /usr/src/app/build/static
#CMD npm run build
