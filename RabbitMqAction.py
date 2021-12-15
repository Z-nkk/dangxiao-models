import time
import threading


class PublishActinon1(object):
     def __init__(self, channel, exchange, queue):
         self.channel = channel
         self.exchange = exchange
         self.queue = queue

     def testAction1(self, data = ''):
         i = 1
         message = dict()
         message['id'] = i
         message = str(message)
         self.channel.basic_publish(
             exchange=self.exchange,
             routing_key=self.queue,
             body=data,
             )
         processId = threading.current_thread()
         print("当前进程id:%s,生产者生产了消息：%s"%(processId,data))
         #time.sleep(2)
         return 'success'
    
     def testAction2(self, data = ''):
         i = 3
         message = dict()
         message['id'] = i
         message = str(message)
         self.channel.basic_publish(
             exchange=self.exchange,
             routing_key=self.queue,
             body=data,
             )
         processId = threading.current_thread()
         print("当前进程id:%s,生产者生产了消息：%s"%(processId,data))
         #time.sleep(4)
         return 'success'


    
     # 测试发送video信号
     def testVideo(self, data = ''):
         try:
            message = data
            self.channel.basic_publish(
                                        exchange=self.exchange, 
                                        routing_key=self.queue, 
                                        body=message,
                                            )
            processId = threading.current_thread()
            print("生产者生产了消息: %s " %  message)
            return 1
         except Exception as e:
             print(e)
             return []
