# 1. Base Image (Lightweight Python)
FROM python:3.9-slim

# 2. Create working directory inside the container
WORKDIR /app

# 3. Copy requirement file first (for caching speed)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application files
COPY app.py .
COPY insurance_model.pkl .

# 6. Open the port for Streamlit
EXPOSE 8501

# 7. Command to run the app
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]