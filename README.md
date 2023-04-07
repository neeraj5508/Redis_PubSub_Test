# Redis_PubSub_Test
Calculating and Testing Latency, Throughput and maximum size of data

The script first connects to Redis and subscribes to a test channel. It then generates a large message of 10 MB and publishes 100 messages to the channel, consisting of integer, string, and image data. After publishing the messages, it gets each message from the channel and calculates the latency between the time the message was sent and the time it was received. It then calculates the average latency.

The script then tests the throughput of publishing messages by generating 1000 messages of 100 KB each and publishing them to the "test" channel. It measures the elapsed time and calculates the throughput as the number of messages per second.

Finally, the script tests the maximum size of data that can be published to Redis by attempting to publish a message of 10 KB. If the message is successfully published, it prints a message indicating success; otherwise, it prints a message indicating failure.
