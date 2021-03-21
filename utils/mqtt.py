"""
基于Python的第三方库paho-mqtt，与mqtt broker通信。
需要安装：pip install paho-mqtt==1.4.0
"""

import json

from paho.mqtt.client import *

from ._log import Logger


class _Client(Client):
    """
    继承paho.mqtt.client(version 3.1/3.1.1)，修改其中部分代码：
     - 修改了_send_publish()中的self._easy_log()，使其在日志中记录发送消息的payload。
     - 修改了_handle_publish()中的self._easy_log()，使其在日志中记录接收消息的payload。
    """

    def _send_publish(self, mid, topic, payload=b'', qos=0, retain=False, dup=False, info=None):
        # we assume that topic and payload are already properly encoded
        assert not isinstance(topic, unicode) and not isinstance(
            payload, unicode) and payload is not None

        if self._sock is None:
            return MQTT_ERR_NO_CONN

        command = PUBLISH | ((dup & 0x1) << 3) | (qos << 1) | retain
        packet = bytearray()
        packet.append(command)

        payloadlen = len(payload)
        remaining_length = 2 + len(topic) + payloadlen

        if payloadlen == 0:
            self._easy_log(
                MQTT_LOG_DEBUG,
                "Sending PUBLISH (d%d, q%d, r%d, m%d), '%s' (NULL payload)",
                dup, qos, retain, mid, topic
            )
        else:
            self._easy_log(
                MQTT_LOG_DEBUG,
                'Sending PUBLISH (d%d, q%d, r%d, m%d), topic: "%s", payload: "%s" (%d bytes)',
                dup, qos, retain, mid, topic, payload, payloadlen
            )

        if qos > 0:
            # For message id
            remaining_length += 2

        self._pack_remaining_length(packet, remaining_length)
        self._pack_str16(packet, topic)

        if qos > 0:
            # For message id
            packet.extend(struct.pack("!H", mid))

        packet.extend(payload)

        return self._packet_queue(PUBLISH, packet, mid, qos, info)

    def _handle_publish(self):
        rc = 0

        header = self._in_packet['command']
        message = MQTTMessage()
        message.dup = (header & 0x08) >> 3
        message.qos = (header & 0x06) >> 1
        message.retain = (header & 0x01)

        pack_format = "!H" + str(len(self._in_packet['packet']) - 2) + 's'
        (slen, packet) = struct.unpack(
            pack_format, self._in_packet['packet'])
        pack_format = '!' + str(slen) + 's' + str(len(packet) - slen) + 's'
        (topic, packet) = struct.unpack(pack_format, packet)

        if len(topic) == 0:
            return MQTT_ERR_PROTOCOL

        # Handle topics with invalid UTF-8
        # This replaces an invalid topic with a message and the hex
        # representation of the topic for logging. When the user attempts to
        # access message.topic in the callback, an exception will be raised.
        try:
            print_topic = topic.decode('utf-8')
        except UnicodeDecodeError:
            print_topic = "TOPIC WITH INVALID UTF-8: " + str(topic)

        message.topic = topic

        if message.qos > 0:
            pack_format = "!H" + str(len(packet) - 2) + 's'
            (message.mid, packet) = struct.unpack(pack_format, packet)

        message.payload = packet

        self._easy_log(
            MQTT_LOG_DEBUG,
            'Received PUBLISH (d%d, q%d, r%d, m%d), topic: "%s", payload: "%s"  (%d bytes)',
            message.dup, message.qos, message.retain, message.mid,
            print_topic, message.payload, len(message.payload)
        )

        message.timestamp = time_func()
        if message.qos == 0:
            self._handle_on_message(message)
            return MQTT_ERR_SUCCESS
        elif message.qos == 1:
            rc = self._send_puback(message.mid)
            self._handle_on_message(message)
            return rc
        elif message.qos == 2:
            rc = self._send_pubrec(message.mid)
            message.state = mqtt_ms_wait_for_pubrel
            with self._in_message_mutex:
                self._in_messages[message.mid] = message
            return rc
        else:
            return MQTT_ERR_PROTOCOL


class MqttClient:
    """
    创建一个mqtt client，实现底层的mqtt通信功能。
      - 实例化该类之后，首先，要调用`mqtt_connect()`连接到mqtt broker。
      - 连接成功后，可以调用公有方法进行通信：`subscribe()`、`publish()`
      - 用户应该根据自身需求，重载该类的回调函数：`connect_callback()`、
      `disconnect_callback()`、`receive_callback()`、`publish_callback()`
    """
    log = print  # 设置记录日志的函数

    def __init__(self, name):
        self.name = str(name)
        self.is_connected = False

        # 创建MQTT连接的客户端
        self.client = _Client(client_id=self.name)
        self.client.name = self.name

        # 设置MQTT的回调函数（mqtt模块会为每个client创建一个线程，来启动回调函数）
        self.client.on_connect = self.__connect_callback
        self.client.on_disconnect = self.__disconnect_callback
        self.client.on_message = self.__receive_callback
        self.client.on_publish = self.__publish_callback
        self.client.on_log = self.__log_callback

        self.msg_id = 0  # 每个消息中包含一个id，依次递增，便于判断消息是否过时

        self.pub_count = 0  # 发送成功的次数
        self.pub_failed_count = 0  # 发送失败的次数
        self.rec_count = 0  # 接收消息的次数

    def get_user_pwd(self):
        """ 获取mqtt连接的帐号和密码，用户应该自行重载该函数。 """
        # user, pwd = "admin", "123456"
        # return user, pwd

    def get_addr_port(self):
        """ 获取mqtt broker的ip地址和端口号，用户应该自行重载该函数。 """
        # addr, port = "127.0.0.1", 1883
        # return addr, port

    def mqtt_connect(self):
        self.log("DEBUG", "connecting to mqtt broker ...")
        self.client.username_pw_set(*self.get_user_pwd())
        self.client.connect(*self.get_addr_port())
        self.loop_start()

    def __connect_callback(self, client, userdata, flags, rc):
        """
        客户端连接到MQTT后的回调函数，被mqtt.Client调用。
        详见mqtt.Client.on_connect的定义。
        """
        replies = {0: "Connection successful",
                   1: "Connection refused - incorrect protocol version",
                   2: "Connection refused - invalid client identifier",
                   3: "Connection refused - server unavailable",
                   4: "Connection refused - bad username or password",
                   5: "Connection refused - not authorised"
                   # 6-255: Currently unused.
                   }
        self.log("INFO", replies[rc])

        if rc == 0:
            self.is_connected = True

        self.connect_callback(client, userdata, flags, rc)

    def connect_callback(self, client, userdata, flags, rc):
        """ 供子类重载 """
        pass

    def disconnect(self):
        self.client.disconnect()

    def __disconnect_callback(self, client, userdata, rc):
        """ 断开连接时的回调函数 """
        self.is_connected = False
        self.log("INFO", "Disconnected")
        self.disconnect_callback(client, userdata, rc)

    def disconnect_callback(self, client, userdata, rc):
        """ 供子类重载 """
        pass

    def loop_start(self):
        """ 开启mqtt的通信循环线程 """
        self.client.loop_start()
        self.client._thread.setName(self.device_name + "(mqtt)")
        self.log("INFO", "start mqtt loop")

    def loop_stop(self, force=False):
        """ 关闭mqtt的通信循环线程 """
        self.client.loop_stop(force)
        self.log("INFO", "stop mqtt loop")

    def subscribe(self, topic, qos=0):
        """ 订阅一个topic。 """
        self.client.subscribe(topic, qos)

    def __receive_callback(self, client, userdata, message):
        """
        客户端收到消息后的回调函数。
        message is a class with members topic, payload, qos, retain.
        详见mqtt.Client.on_message的定义。
        """
        self.rec_count += 1
        self.receive_callback(client, userdata, message)

    def receive_callback(self, client, userdata, message):
        """ 供子类重载 """
        pass

    def publish(self, topic, payload, qos=0, retain=False):
        """
        发送一条消息到指定的topic。
          `payload`: 要发送的消息内容，为字典类型。
          qos=0 时，消息最多发布一次，可能一次都没收到。
          qos=1 时，消息至少发布一次，可能收到多次。
          qos=0 时，消息仅发布一次，保证收到且只收到一次。
        """
        self.msg_id += 1
        try:
            payload["id"] = str(self.msg_id)  # 设置消息的id，转换成字符串类型
            # 将payload转换成json格式发布，并获得这次publish的信息
            info = self.client.publish(topic, json.dumps(payload), qos, retain)

            # 同步工作，等待消息成功发出或超过timeout
            info.wait_for_publish()
            if info.is_published():
                self.pub_count += 1
            else:
                raise RuntimeError("waiting for publish but timeout")

        except RuntimeError as e:
            self.msg_id -= 1
            self.pub_failed_count += 1
            self.log("ERROR", "publish failed, {}".format(str(e)))

    def __publish_callback(self, client, userdata, mid):
        """
        客户端发布消息后的回调函数。
          - 对于qos为0的消息，这只意味着消息离开了客户端。
          - 对于qos为1或2的消息，这意味着已经完成了与mqtt broker的握手。
        """
        self.publish_callback(client, userdata, mid)

    def publish_callback(self, client, userdata, mid):
        """ 供子类重载 """
        pass

    def __log_callback(self, client, userdata, level, buf):
        """
        定义记录日志的函数，每次mqtt模块产生日志时会自动调用该函数。
          - mqtt模块生成的日志级别与logging模块不同，要进行转换。
        """
        self.log(LOGGING_LEVEL[level], buf)
        # mqtt模块生成的日志格式大致为
        # "Sending PUBLISH (d%d, q%d, r%d, m%d), '%s', ... (%d bytes)",
        # dup, qos, retain, mid, topic, payloadlen


if __name__ == "__main__":
    import time

    class Device(MqttClient):

        def get_user_pwd(self):
            user, pwd = "admin", "123456"
            return user, pwd

        def get_addr_port(self):
            addr, port = "127.0.0.1", 1883
            return addr, port

        def run(self):
            self.log("DEBUG", "start threading: {}".format(self.name))

            # 连接到mqtt broker，并计算连接耗时
            start_time = time.time()
            self.mqtt_connect()
            while not self.is_connected:
                pass
            self.log("DEBUG", "This connection takes {}s".format(
                time.time() - start_time))

            # 发布和订阅
            msg = {"text": "This is for test."}
            self.publish("/test/post", msg)
            self.subscribe("/test/reply")

            # self.disconnect()

            # 保持循环
            while 1:
                time.sleep(1)

    # 设置日志器（不设置的话默认用print打印在终端上）
    logger = Logger(__file__, "DEBUG")
    logger.to_console("DEBUG")
    Device.log = logger.log

    # 创建一个设备
    d1 = Device("d1")
    d1.run()
