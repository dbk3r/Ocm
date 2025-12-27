# Stage 1: Angular build
FROM node:20 AS frontend_builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build --configuration production

# Stage 2: Python backend
FROM python:3.13-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/app ./app/
COPY --from=frontend_builder /app/frontend/dist/ /app/static/
EXPOSE 8080
ENV PYTHONPATH="/app"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]