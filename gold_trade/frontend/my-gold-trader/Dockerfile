# Use the official Node.js image
FROM node:14

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application code
COPY . .

# Build the app for production
RUN npm run build

# Serve the app
CMD ["npx", "serve", "-s", "build"]

# Expose the port the app runs on
EXPOSE 3000
