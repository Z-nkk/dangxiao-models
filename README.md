1.启动算法
    ./run.sh

2.配置
    2.1配置RabbitMQ
        修改myrabbitmq.py第23~27行，修改host,port,vhost,user,passwd这几项

    2.2配置minio
        修改minioclass.py第9~11行,修改host:port,access_key,secret_key

    2.3配置openpose
        修改skeleton.py第14行配置openpose的安装位置
        修改skeleton.py第25行配置models位置

    2.4配置exchange和queue
        algorithm.py第156行，配置发送给java后端的exchange和queue
        videoSplit.py第194,195行,配置从java后端接收消息的exchange和queue

3.依赖
    scikit-learn 版本  0.21.2
    pip install scikit-learn==0.21.2

4.模拟启动
    将sendRabbitMQMsg.json里的内容，通过RabbitMQ的管理界面，发送到dev-VideoCaptue队列，即可模拟java后端发起课程。
    msg.json里存储，算法处理后的传给java后端的消息
# dangxiao-models
# dangxiao-models
# dangxiao-models
