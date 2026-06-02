# apps/api/Dockerfile
# FastAPI 后端 — Python 3.12 slim

FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖（psycopg2、pymysql 需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目（packages 被 apps/api 通过 sys.path 引用）
COPY . .

# 确保 packages 可被 import
ENV PYTHONPATH="/app/packages/ai-tools:/app/packages/db-engine:/app/packages/execution-workflow:${PYTHONPATH}"

EXPOSE 8000

CMD ["uvicorn", "apps.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
