# Docker and Containerization

## What is Docker?

Docker is an open-source platform that automates the deployment of applications inside lightweight, portable containers. Containers package code and its dependencies together, ensuring the application runs consistently across different environments.

Docker was released in 2013 and has since become the industry standard for containerization.

## Key Concepts

### Containers
A container is a runnable instance of an image:
- Isolated process with its own filesystem
- Shares the host OS kernel (unlike VMs)
- Lightweight and fast to start
- Ephemeral by default

### Images
An image is a read-only template for creating containers:
- Built from a Dockerfile
- Layered filesystem (each instruction adds a layer)
- Can be shared via Docker registries

### Dockerfile
A text file with instructions to build an image:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Registry
A storage and distribution system for Docker images:
- **Docker Hub**: Public registry (hub.docker.com)
- **GitHub Container Registry**: ghcr.io
- **AWS ECR**: Amazon Elastic Container Registry
- **Self-hosted**: Harbor, Nexus

## Essential Docker Commands

### Images
```bash
docker build -t myapp:1.0 .         # Build image
docker images                        # List images
docker pull nginx                    # Download image
docker push myapp:1.0               # Push to registry
docker rmi myapp:1.0                # Remove image
```

### Containers
```bash
docker run myapp                     # Run container
docker run -d -p 8000:8000 myapp    # Detached with port mapping
docker run -v ./data:/app/data myapp # Mount volume
docker ps                            # List running containers
docker ps -a                         # List all containers
docker stop <id>                     # Stop container
docker rm <id>                       # Remove container
docker logs <id>                     # View logs
docker exec -it <id> bash           # Execute command in container
```

## Docker Compose

Docker Compose defines and runs multi-container applications:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Compose Commands
```bash
docker compose up                    # Start services
docker compose up -d                 # Detached mode
docker compose down                  # Stop and remove
docker compose logs                  # View logs
docker compose exec backend bash    # Shell into service
docker compose build                # Build images
```

## Volumes and Networking

### Volumes
Persist data beyond container lifecycle:
```bash
docker volume create mydata
docker run -v mydata:/app/data myapp
```

### Networks
Containers can communicate on the same network:
```bash
docker network create mynet
docker run --network mynet --name api myapp
docker run --network mynet --name db postgres
```

## Best Practices

### Dockerfile Best Practices
- Use official base images
- Use specific image tags (not `latest`)
- Minimize layers by combining RUN commands
- Use `.dockerignore` to exclude unnecessary files
- Run as non-root user
- Use multi-stage builds for smaller images

### Multi-stage Build Example
```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
```

## Containers vs Virtual Machines

| Feature | Containers | Virtual Machines |
|---------|-----------|-----------------|
| Startup time | Seconds | Minutes |
| Resource usage | Low | High |
| Isolation | Process-level | Full OS |
| Portability | Very high | High |
| OS sharing | Yes | No |
