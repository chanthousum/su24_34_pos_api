# ==============================
# 1️⃣ Base image
# ==============================
FROM python:3.12-slim

# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# ==============================
# 2️⃣ Install dependencies
# ==============================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# ==============================
# 3️⃣ Collect static files
# ==============================
RUN python manage.py collectstatic --noinput

# ==============================
# 4️⃣ Run migrations + start server
# ==============================
# Use port 8090 instead of 8000
CMD ["sh", "-c", "python manage.py migrate && gunicorn su24_34_pos_api.wsgi:application --bind 0.0.0.0:8090"]
# Expose Django port
EXPOSE 8090
