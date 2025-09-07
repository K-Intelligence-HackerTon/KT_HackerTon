# React 앱을 위한 Dockerfile
FROM node:18-alpine as build

# 작업 디렉토리 설정
WORKDIR /app

# package.json과 package-lock.json 복사
COPY package*.json ./

# 의존성 설치
RUN npm ci --only=production

# 소스 코드 복사
COPY . .

# 앱 빌드
RUN npm run build

# Nginx를 사용한 프로덕션 서버
FROM nginx:alpine

# Nginx 설정 파일 복사
COPY nginx.conf /etc/nginx/nginx.conf

# 빌드된 앱을 Nginx 디렉토리로 복사
COPY --from=build /app/build /usr/share/nginx/html

# 포트 3000 노출
EXPOSE 3000

# Nginx 시작
CMD ["nginx", "-g", "daemon off;"]
