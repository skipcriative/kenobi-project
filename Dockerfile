FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set timezone to GMT-3 (São Paulo)
ENV TZ=America/Sao_Paulo
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Run scheduler
CMD ["python", "-m", "kenobi.scheduler"]
