import pika
import threading
import json
import datetime
import time
import sys

from pika.exceptions import ChannelClosed
from pika.exceptions import ConnectionClosed
from RabbitMqAction import PublishActinon1
import numpy as np


import time
# RabbitMq服务器相关
import cv2


class RabbitMQServer(object):

    # rabbitmq 配置信息
    MQ_CONFIG = {
        "host": "192.168.10.58",
        "port": 5672,
        "vhost": "Party School",
        "user": "education",
        "passwd": "education",
    }
    _instance_lock = threading.Lock()

    def __init__(self, exchange = 'exchange', exchange_type = 'direct', durable = True):
        # 创建RabbitMq类的时候，要指定一下当前服务端的交换机及其类型
        self.exchange = exchange
        self.connection = None
        self.channel = None
        self.exchange_type = exchange_type
        self.durable = durable

    def reconnect(self):
        try:
            
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            # 指定RabbitMq的用户名和密码
            credentials = pika.PlainCredentials(
                                                self.MQ_CONFIG.get("user"),     
                                                self.MQ_CONFIG.get("passwd"),
                                                0,
                                                )
            # 指定连接的参数
            parameters = pika.ConnectionParameters(
                                                self.MQ_CONFIG.get("host"), 
                                                self.MQ_CONFIG.get("port"), 
                                                self.MQ_CONFIG.get("vhost"),
                                                credentials,
                                                )
            # 创建一个连接
            self.connection = pika.BlockingConnection(parameters)
            # 在连接上创建一个频道
            self.channel = self.connection.channel()
            # 创建一个交换机
            if len(self.exchange) > 0:
                self.channel.exchange_declare(
                                            exchange = self.exchange, 
                                            exchange_type = self.exchange_type, 
                                            durable=self.durable,
                                            )
        except Exception as e:
            print(e)



# 生产者，生产者类在生成的时候可以指定交换机以及队列，同时可以指定生产者的动作
class RabbitPublisher(RabbitMQServer):
    # 初始化父类：RabbitMq的配置
    def __init__(self, action = '',
                        data = '',
                        exchange = 'exchange', 
                        queue = 'testQueue', 
                        exchange_type = 'direct',
                        durable = True):
        self.queue = queue
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.durable = durable
        self.action = action
        self.data = data
        # 创建的RabbitMq类目的只有建立连接并创建交换机
        super(RabbitPublisher, self).__init__(
                                            self.exchange, 
                                            self.exchange_type, 
                                            self.durable)


    def start_publish(self):
        try:
            # 连接服务器，创建频道以及交换机
            self.reconnect()
            # 声明队列
            self.channel.queue_declare(
                    queue=self.queue,
                    exclusive=False, 
                    durable = True,
                    )
            # 绑定队列
            if len(self.exchange) > 0:
                self.channel.queue_bind(
                            exchange=self.exchange, 
                            queue=self.queue, 
                            routing_key=self.queue,
                            )
            # 此处应进行生产者的动作 self.action
            result = getattr(PublishActinon1(self.channel, self.exchange, self.queue), self.action)(self.data)
            print(result)
            return result
        except ConnectionClosed as e:
            self.reconnect()
            print(e)
            time.sleep(2)
        except ChannelClosed as e:
            self.reconnect()
            print(e)
            time.sleep(2)
        except Exception as e:
            self.reconnect()
            print(e)
            time.sleep(2)


    @classmethod
    def run(cls, action = '', data = '', exchange = 'exchange', publisherQueue = 'test', exchange_type = 'direct'):
        publish = cls(action, data, exchange, publisherQueue, exchange_type)
        result = publish.start_publish()
        return result



# 消费者类 若想要创造不同的消费者，需要多建几个消费者类
class RabbitConsumerVideo(RabbitMQServer):
    # 初始化父类：RabbitMq的配置
    def __init__(self,  callback,
                        exchange = 'exchange',
                        queue = 'testQueue', 
                        exchange_type = 'direct',
                        durable = True,
                        ):
        self.consumer_callback = callback
        self.queue = queue
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.durable = durable

        # 创建的RabbitMq类目的只有建立连接并创建交换机
        super(RabbitConsumerVideo, self).__init__(
                                            self.exchange, 
                                            self.exchange_type, 
                                            self.durable)



    # 消费者函数
    def start_consumer(self):
        try:
            # 创建频道以及交换机
            self.reconnect()
            # 声明队列
            self.channel.queue_declare(
                queue=self.queue,
                exclusive=False, 
                durable = True,
                )
            # 绑定队列
            self.channel.queue_bind(
                                exchange=self.exchange, 
                                queue=self.queue, 
                                routing_key=self.queue,
                                )
            # 使用定义的回调函数，现在不使用循环试试，仍然是可以一直收到消息的
            
            self.channel.basic_consume(
                                self.queue,
                                self.consumer_callback,
                                False,
                                        )
            # 消费者开始执行
            self.channel.start_consuming()
        except ConnectionClosed as e:
            self.reconnect()
            time.sleep(2)
        except ChannelClosed as e:
            self.reconnect()
            time.sleep(2)
        except Exception as e:
            self.reconnect()
            time.sleep(2)
    
    def queue_length(self):
        self.reconnect()
        length = self.channel.queue_declare(
                queue=self.queue,
                exclusive=False, 
                durable = True,
                ).method.message_count 
        return length
        


    @classmethod
    def run(cls, callback,exchange = 'exchange', consumerQueue = 'test',  exchange_type = 'direct'):
        consumer = cls(callback,exchange,consumerQueue,exchange_type)
        #while True:
        consumer.start_consumer()
