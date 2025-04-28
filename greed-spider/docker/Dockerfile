# 设置基础镜像
FROM python:3.13.3-alpine

# 设置工作目录
WORKDIR /opt/app

# 拷贝项目文件
COPY ./sse-stock-line-spider.py /opt/app
COPY ./requirements.txt /opt/app
COPY ./GPLIST.csv /opt/app

# 安装项目依赖
RUN pip install -r requirements.txt

# 运行项目
CMD ["python", "sse-stock-line-spider.py"]