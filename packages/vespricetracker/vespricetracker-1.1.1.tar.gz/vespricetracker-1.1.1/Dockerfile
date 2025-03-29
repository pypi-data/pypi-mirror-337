FROM ubuntu:22.04

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y \
        python3.11 \
        python3.11-venv \
        libgconf-2-4 \
        libnss3 \
        libxss1 \
        fonts-liberation \
        xvfb \
        wget \
        gnupg2 \
        libgbm1 \
        && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

USER appuser
WORKDIR /app

# Install your package from PyPI
RUN python3.11 -m ensurepip --upgrade && python3.11 -m pip install --user --no-cache-dir vespricetracker==1.1.1

# Environment variables
ENV PATH="/home/appuser/.local/bin:/usr/local/bin:${PATH}"
ENV DISPLAY=:99
ENV SCREEN_GEOMETRY=1920x1080x24

ENTRYPOINT ["sh", "-c", "Xvfb :99 -screen 0 $SCREEN_GEOMETRY -ac +extension RANDR >/dev/null 2>&1 & python3.11 -m vespricetracker"]
