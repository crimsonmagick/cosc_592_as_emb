FROM nvidia/cuda:13.3.0-devel-ubuntu24.04

RUN apt-get update && apt-get install -y \
    build-essential \
    python3 \
    python3-venv \
    python3-pip \
    python3-dev \
    git \
    vim \
    clang \
    wine64 \
    msitools \
    ca-certificates \
    winbind \
    && apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/py

WORKDIR /workspace

RUN $(command -v wine64 || command -v wine || false) wineboot --init && \
    while pgrep wineserver > /dev/null; do sleep 1; done

RUN git clone https://github.com/mstorsjo/msvc-wine.git
RUN ./msvc-wine/vsdownload.py --dest msvc --accept-license
RUN ./msvc-wine/install.sh msvc
RUN echo 'export PATH="$PATH:/workspace/msvc/bin/x64"' >> ~/.bashrc
ENV PATH="/workspace/msvc/bin/x64:${PATH}"

COPY requirements.txt .
COPY ./src ./src
COPY ./.git ./.git
COPY ./.gitignore ./.gitignore
RUN py -m venv .venv
RUN . .venv/bin/activate && pip install -r requirements.txt
ENV VIRTUAL_ENV=/workspace/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"