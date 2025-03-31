FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime

ENV python_version=v3.11.6
ENV python_url=https://github.com/python/cpython.git
ENV location=/tmp/python-${python_version}

RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y \
    ca-certificates \
    git \
    gnupg2 \
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
    xdg-utils && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
    
RUN git clone --depth=1 "$python_url" --branch "$python_version" --single-branch "$location" && \
    cd "$location" && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    rm -rf "$location"

RUN /usr/local/bin/python3.11 -m pip install --no-cache-dir --upgrade pip && \
    /usr/local/bin/python3.11 -m pip install --no-cache-dir vespricetracker==1.1.3

CMD ["/usr/local/bin/python3.11", "-m", "vespricetracker"]
