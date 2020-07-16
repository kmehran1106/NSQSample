# Working with NSQ

### Legend
- lookup -> nsqlookupd  
- daemon -> nsqd  
- dashboard -> nsqadmin

## Things to Note
1. Do not have multiple nsqd daemons in the same host
2. The broadcast address is pivotal for a distributed nsq system. Check below for more details.

## Direct Communication with nsqd Daemon
The writer needs to directly write to the daemon. Now, the consumer/client can consume by directly connecting to the daemon tcp address. But, this will not work very well for a large scale distributed system.

The second method is to use lookup. This is a type of service discovery tool. The daemons need to connect to the lookup tcp address. This will allow the client/consumer to connect to the lookup http address and consume the data stream. This methodology does however some restrictions, but does not provide any hindrance for a good service. 

1. If there is no topic already created, the client will get a 404 if it wants to connect to the lookup topic. If it connected directly to the daemon tcp address, it wouldn't matter if the topic was there or not in the beginning.

2. From the docs, you'll see that the daemon is providing arguments to connect to the lookup tcp address. But, that's not all. The lookup also needs to connect to the daemon. This is done by using the --broadcast-address flag in the daemon argument. You would put the hostname (dns/ip) as the value for this flag.

3. For our use case in this demo, we could have used 127.0.0.1, and the client/consumer would work as well. However, this did not work properly when we wanted to use the dashboard. But tbh, we need to use the dashboard since it's very informative and also really useful!

4. To fix this, we added the daemons docker-compose service name (for us, it was nsqd) `/etc/hosts`. Basically, we added `127.0.0.1 nsqd` in `/etc/hosts`.

5. Then, we added the daemons docker-compose service name as the broadcast address!

6. For curiosity's sake, I tried to have two daemons in the same host, and that was a bit more complicated. This is not recommended by the docs, so if you really do want to do this, try to find out how to work this out on your own. Just a hint, the ports were creating the problems.

7. The dashboard wasn't working back then, because although it could connect with the lookup service, it wasn't able to fetch the daemon data. The dashboard wants to connect to the daemon's `broadcast-address:http-port`, but it can't with 127.0.0.1 since the dashboard is running inside a container and it can't contact the outside world! So, we connected it with nsqd. But, if we want to use `nsqd` as the broadcast address for nsqd service, we have to allow consumers outside docker-compose can also use the "nsqd" name to get to it. Hence, the addition to `/etc/hosts`.

## Installation Instructions
1. Install docker and pipenv
2. Run docker-compose up --build
3. Run pipenv shell
4. Now, run `python producer.py` to generate topic and messages.
5. Run `python abel.py/cane.py` to consume the topics.

## Production Thoughts
We are probably going to add the daemon to our live compose file, and in a separate server launch the lookup and dashboard services with another compose file. In the daemon broadcast address, we will be usinng the lookup server's Internal IP, while using the self server's Internal IP for broadcast address. Also, we'll make sure the security groups are connected.


