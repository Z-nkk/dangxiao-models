#import minio
from minio import Minio




class MinioClass:
    def __init__(self):
        self.client = Minio('192.168.10.93:9000',
            access_key='minio',
            secret_key='miniostorage',
            secure = False)
        self.content_type  = 'application/csv/jpg/png/xlsx'

    def upload(self, object_name, file_path):
        #self.client.fput_object(bucket_name='education',object_name=object_name, file_path=file_path,content_type=self.content_type)
        self.client.fput_object(bucket_name='education',object_name=object_name, file_path=file_path,content_type=self.content_type)


if __name__ == "__main__":
    minioclient = MinioClass()

    ret=minioclient.upload('image/source/testpeng001.jpg','/data/SmartEducationImage/skeleton/20210416140731_cameraid2.jpg')
    print(ret)
