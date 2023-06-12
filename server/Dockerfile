FROM swr.cn-north-4.myhuaweicloud.com/ilbwb/lnup:v1.0
#MAINTAINER 维护者信息
LABEL maintainer="swortect@gmail.com"
#工作目录
WORKDIR /home/myquant
#拷贝文件至工作目录
COPY . .
RUN chmod +x run.sh && rm -rf ~/.cache/pip
#EXPOSE 映射端口
EXPOSE 5000
#容器启动时执行命令

EXPOSE 5000
# RUN ls -l ./run.sh
# RUN sh ./run.sh
# 运行uwsgi
RUN chmod 755 /home/myquant/ 
CMD ["./run.sh"]
# CMD ["uwsgi", "--http", ":5000", "--wsgi-file", "app.py"]
