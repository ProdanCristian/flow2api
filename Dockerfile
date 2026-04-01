FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PLAYWRIGHT_BROWSERS_PATH=0 \
    ALLOW_DOCKER_HEADED_CAPTCHA=true \
    DISPLAY=:99 \
    XVFB_WHD=1920x1080x24 \
    BROWSER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable

COPY requirements.txt ./

# 有头模式基础依赖：虚拟显示、窗口管理器。
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        xvfb \
        fluxbox \
        wget \
        gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt \
    && python -m playwright install --with-deps chromium

COPY . .
COPY docker/entrypoint.headed.sh /usr/local/bin/entrypoint.headed.sh
RUN sed -i 's/\r$//' /usr/local/bin/entrypoint.headed.sh && chmod +x /usr/local/bin/entrypoint.headed.sh

EXPOSE 8000

CMD ["/usr/local/bin/entrypoint.headed.sh"]
