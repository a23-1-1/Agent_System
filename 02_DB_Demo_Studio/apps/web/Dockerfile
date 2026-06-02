# apps/web/Dockerfile
# 前端 — Vite 构建 + Nginx 托管

# Stage 1: Build
FROM node:22-alpine AS builder

WORKDIR /app
COPY apps/web/package.json apps/web/package-lock.json* ./
RUN npm ci

COPY apps/web/ .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

COPY apps/web/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
