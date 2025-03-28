import pika
import json
from typing import Callable, Any


class RabbitMQTool:
    def __init__(self, host: str = 'localhost', port: int = 5672, username: str = 'guest', password: str = 'guest'):
        """
        初始化 RabbitMQ 连接
        :param host: RabbitMQ 服务器地址
        :param port: RabbitMQ 服务器端口
        :param username: 用户名
        :param password: 密码
        """
        self.credentials = pika.PlainCredentials(username, password)
        self.connection_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def connect(self):
        """建立连接并创建通道"""
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()

    def close(self):
        """关闭连接"""
        if self.connection and not self.connection.is_closed:
            self.connection.close()

    def send_message(self, queue_name: str, message: Any, durable: bool = True):
        """
        发送消息到指定队列
        :param queue_name: 队列名称
        :param message: 消息内容（可以是字典、字符串等）
        :param durable: 是否持久化队列
        """
        if not self.connection or self.connection.is_closed:
            self.connect()

        # 声明队列（如果不存在则创建）
        self.channel.queue_declare(queue=queue_name, durable=durable)

        # 将消息转换为 JSON 格式
        if isinstance(message, dict):
            message = json.dumps(message)

        # 发送消息
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2 if durable else 1  # 2 表示消息持久化
            )
        )
        # print(f" [x] Sent message to '{queue_name}': {message}")

    def consume_messages(self, queue_name: str, callback: Callable[[str], None], durable: bool = True,
                         auto_ack: bool = False):
        """
        消费指定队列中的消息
        :param queue_name: 队列名称
        :param callback: 回调函数，用于处理消息
        :param durable: 是否持久化队列
        :param auto_ack: 是否自动确认消息
        """
        if not self.connection or self.connection.is_closed:
            self.connect()

        # 声明队列（如果不存在则创建）
        self.channel.queue_declare(queue=queue_name, durable=durable)

        # 定义消息处理逻辑
        def on_message(ch, method, properties, body):
            try:
                message = body.decode('utf-8')
                print(f" [x] Received message from '{queue_name}': {message}")
                callback(message)
            except Exception as e:
                print(f"Error processing message: {e}")
            finally:
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)  # 手动确认消息

        # 设置消费者
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message,
            auto_ack=auto_ack
        )

        print(f" [*] Waiting for messages in '{queue_name}'. To exit press CTRL+C")
        self.channel.start_consuming()

    @staticmethod
    def send_msg_to_queue(queue_name, data):
        # 创建 RabbitMQ 实例
        rabbitmqObj = RabbitMQTool(host='101.132.137.45', username="admin", password="Wise_2021_mq")
        # 发送消息
        rabbitmqObj.send_message(queue_name=queue_name, message={"task": data}, durable=True)
        # 关闭连接
        rabbitmqObj.close()


if __name__ == '__main__':
    # 创建 RabbitMQ 实例
    rabbitmq = RabbitMQTool(host='101.132.137.45', username="admin", password="Wise_2021_mq")
    # 发送消息
    rabbitmq.send_msg_to_queue(queue_name='test_queue', data={'key': 'value'})
    # 关闭连接
    rabbitmq.close()
