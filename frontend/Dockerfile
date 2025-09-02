# Use a Node.js base image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy the package.json file and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Run the build command
RUN npm run build

# Expose the port that the app will run on
EXPOSE 80

# Command to serve the built application
CMD ["npm", "run", "preview"]
