# Stage 1: Build the React application
FROM node:20-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy the package.json file to the working directory
COPY package.json ./

# Install all project dependencies
RUN npm install

# Copy the source and public directories explicitly
COPY public ./public
COPY src ./src
COPY vite.config.js ./

# Run the build command
RUN npm run build

# Stage 2: Serve the built application with a lightweight web server
FROM nginx:alpine

# Copy the production files from the build stage to the Nginx public directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 to allow external access
EXPOSE 80

# Command to start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
