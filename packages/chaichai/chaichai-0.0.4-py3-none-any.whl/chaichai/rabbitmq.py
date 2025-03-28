import pika
import json
from typing import Callable, Any

# 全局变量
credentials = None
connection_params = None
connection = None
channel = None
found_target = False  # 用于标记是否找到目标消息


def init_rabbitmq(host: str = 'localhost', port: int = 5672, username: str = 'guest', password: str = 'guest'):
    """
    初始化并保持 RabbitMQ 连接
    :param host: RabbitMQ 服务器地址
    :param port: RabbitMQ 服务器端口
    :param username: 用户名
    :param password: 密码
    """
    global credentials, connection_params, connection, channel
    credentials = pika.PlainCredentials(username, password)
    connection_params = pika.ConnectionParameters(
        host=host,
        port=port,
        credentials=credentials
    )
    """建立连接并创建通道"""
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

def close():
    """关闭连接"""
    global connection
    if connection and not connection.is_closed:
        connection.close()

def get_message(queue_name: str, durable: bool = True):
    """
    从指定队列中获取一条消息
    :param queue_name: 队列名称
    :return: 消息内容（字符串格式）或 None（如果没有消息）
    """
    global channel, connection

    # 声明队列（如果不存在则创建）
    channel.queue_declare(queue=queue_name, durable=durable)

    # 获取消息
    method_frame, header_frame, body = channel.basic_get(queue=queue_name, auto_ack=False)

    if method_frame:
        # 如果获取到消息，解码并返回
        message = body.decode('utf-8')
        # 手动确认消息
        # channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return message
    else:
        # 如果没有获取到消息，返回 None
        return ""

def send_message(queue_name: str, message: Any, durable: bool = True):
    """
    发送消息到指定队列
    :param queue_name: 队列名称
    :param message: 消息内容（可以是字典、字符串等）
    :param durable: 是否持久化队列
    """
    global channel, connection

    # 声明队列（如果不存在则创建）
    channel.queue_declare(queue=queue_name, durable=durable)

    # 将消息转换为 JSON 格式
    if isinstance(message, dict):
        message = json.dumps(message)

    # 发送消息
    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2 if durable else 1  # 2 表示消息持久化
        )
    )


def consume_messages(queue_name: str, ack, durable: bool = True,auto_ack: bool = False,timeout: int = 30):
    """
    消费指定队列中的消息
    :param queue_name: 队列名称
    :param callback: 回调函数，用于处理符合条件的消息
    :param durable: 是否持久化队列
    :param auto_ack: 是否自动确认消息
    """
    global channel,found_target,connection

    # 声明队列（如果不存在则创建）
    channel.queue_declare(queue=queue_name, durable=durable)

    # 定义消息处理逻辑
    def on_message(ch, method,properties, body):
        message = json.loads(body.decode('utf-8'))
        print(message)
        print(ack)
        if message.get('id') == ack:
            # callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag) # 确认消息
            ch.stop_consuming()
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True) # 拒绝消息并重新入队

    def timeout_callback():
        global found_target
        if not found_target:
            channel.stop_consuming()

    # 设置消费者
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=on_message,
        auto_ack=auto_ack
    )
    # 设置超时
    connection.add_timeout(timeout, timeout_callback)
    channel.start_consuming()


if __name__ == '__main__':
    # 初始化 RabbitMQ
    init_rabbitmq(host='101.132.137.45', port=5672, username="admin", password="Wise_2021_mq")
    result = get_message("mq_test")
    # print(result)
    # 发送消息
    # send_message(queue_name='mq_test',message={'task': 'data3',"id":"2"})
    consume_messages(queue_name='mq_test', ack=1)