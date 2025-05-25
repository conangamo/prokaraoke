FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Tạo thư mục cho ảnh tải lên
RUN mkdir -p app/static/images

EXPOSE 5000

CMD ["python", "run.py"] 