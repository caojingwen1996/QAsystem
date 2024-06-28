# 使用官方的 Python 基础镜像
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 将 requirements.txt 文件复制到工作目录
COPY requirements.txt .

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件复制到工作目录
COPY . .

# 运行 Flask 应用程序
CMD ["python", "app.py"]
