import gnsq

consumer = gnsq.Consumer(
    'ABC', 'channel', 
    # nsqd_tcp_addresses='localhost:4150', 
    lookupd_http_addresses='localhost:4161'
)

@consumer.on_message.connect
def handler(consumer, message):
    print(f"Got Message: {message.body.decode('utf-8')}")

consumer.start()
