FROM node:16

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm install -g nodemon
RUN npm install
# If you are building your code for production
# RUN npm ci --only=production

COPY . .

RUN mkdir -p /var/log/server_logs
RUN chmod 777 /var/log/server_logs

RUN chmod ugo+x ./entrypoint.sh