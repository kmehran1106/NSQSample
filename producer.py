import gnsq

p1 = gnsq.Producer('127.0.0.1:4150')
p1.start()

p1.publish('ABC', 'hello ABC!'.encode('utf-8'))


p2 = gnsq.Producer('127.0.0.1:4150')
p2.start()

p2.publish('XYZ', 'hello XYZ!'.encode('utf-8'))

p1.close()
p2.close()