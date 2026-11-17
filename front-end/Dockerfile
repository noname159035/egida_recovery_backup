# Этап 1: Сборка приложения
FROM node:23-alpine AS builder

WORKDIR /app

# Копируем файлы зависимостей
COPY package.json package-lock.json ./
RUN npm ci --production

# Копируем весь код приложения
COPY . .

# Собираем приложение для продакшена
RUN npm run build

# Этап 2: Финальный образ для продакшена
FROM node:23-alpine

WORKDIR /app

# Создаём пользователя без root-привилегий
RUN addgroup -g 1001 -S appgroup && adduser -S -u 1001 -G appgroup appuser
USER appuser

# Копируем только необходимые файлы из этапа сборки
COPY --from=builder /app/.output ./.output

# Устанавливаем переменную окружения для порта
ENV PORT=3000

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]