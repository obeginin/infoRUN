# 1. Используем официальный образ Node.js (LTS)
FROM node:18-alpine AS builder

# 2. Устанавливаем рабочую директорию
WORKDIR /infoRUN/Client

# 3. Копируем package.json и package-lock.json (если есть)
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install --production --frozen-lockfile

# Копируем собранный билд и статические файлы
COPY .next ./.next
COPY public ./public

# 9. Открываем порт Next.js
EXPOSE 3000

# 10. Запускаем Next.js в продакшн-режиме
CMD ["npm", "run", "start", "--", "-p", "3000", "-H", "0.0.0.0"]
