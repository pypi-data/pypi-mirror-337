FROM ubuntu:22.04

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# Set timezone (prevents tzdata prompt)
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

# Python build config
ENV python_version=v3.11.6
ENV python_url=https://github.com/python/cpython.git
ENV location=/tmp/python-${python_version}

# Install system dependencies in one layer
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    git \
    gcc \
    g++ \
    make \
    build-essential \
    wget \
    gettext \
    pkg-config \
    libbz2-dev \
    libffi-dev \
    libgdbm-dev \
    libgdbm-compat-dev \
    liblzma-dev \
    libncurses-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    tk-dev \
    zlib1g-dev \
    # Chrome dependencies
    libx11-xcb1 \
    libxtst6 \
    libxss1 \
    libnss3 \
    libnspr4 \
    fonts-liberation \
    xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Install Chrome (modern method)
RUN mkdir -p /etc/apt/keyrings && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > /etc/apt/keyrings/google-chrome.asc && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.asc] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Build Python with optimizations
RUN git clone --depth=1 "$python_url" --branch "$python_version" --single-branch "$location" && \
    cd "$location" && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    rm -rf "$location"

# Install application requirements
RUN /usr/local/bin/python3.11 -m pip install --no-cache-dir --upgrade pip && \
    /usr/local/bin/python3.11 -m pip install --no-cache-dir vespricetracker==1.1.2

# Final command to execute
CMD ["/usr/local/bin/python3.11", "-m", "vespricetracker"]
