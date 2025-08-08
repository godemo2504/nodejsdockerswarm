FROM node:18-alpine
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install --production
COPY . .
ENV PORT=3000
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD wget -qO- http://localhost:3000/ || exit 1
CMD ["npm", "start"]
