import time
import io
from PIL import Image
import redis

# Configuration
topic = "Test"
num_messages = 10000
message_size = 1024  # in bytes
interval = 1  # in seconds

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Subscribe to the topic
subscriber = redis_client.pubsub()
subscriber.subscribe(topic)

# Wait for the subscriber to connect
time.sleep(1)

# Send messages from the publisher and calculate latency, throughput, and max message size
latency_total = 0
start_time = time.time()
max_message_size = 0
for i in range(num_messages):
    # Integer message
    message_int = i
    message_start_time = time.time()
    redis_client.publish(topic, message_int)
    message_end_time = time.time()
    latency = (message_end_time - message_start_time) * 1000  # convert to milliseconds
    latency_total += latency
    if len(str(message_int).encode()) > max_message_size:
        max_message_size = len(str(message_int).encode())

    # String message
    message_str = "This is a string message #" + str(i)
    message_start_time = time.time()
    redis_client.publish(topic, message_str)
    message_end_time = time.time()
    latency = (message_end_time - message_start_time) * 1000  # convert to milliseconds
    latency_total += latency
    if len(message_str.encode()) > max_message_size:
        max_message_size = len(message_str.encode())

    # Image message
    image_file = "icon.png"
    with open(image_file, "rb") as f:
        image_bytes = f.read()
    image = Image.open(io.BytesIO(image_bytes))
    message_start_time = time.time()
    redis_client.publish(topic, image_bytes)
    message_end_time = time.time()
    latency = (message_end_time - message_start_time) * 1000  # convert to milliseconds
    latency_total += latency
    if len(image_bytes) > max_message_size:
        max_message_size = len(image_bytes)

end_time = time.time()
elapsed_time = end_time - start_time
throughput = num_messages / elapsed_time
avg_latency = latency_total / (3*num_messages) # 3 messages are sent in each iteration of the loop (integer, string, and image)

# Print results
print("Test results:")
print("-" * 70)
print("Elapsed time: {:.3f} seconds".format(elapsed_time))
print("Number of messages: {}".format(num_messages))
print("Interval between messages: {} seconds".format(interval))
print("Throughput: {:.3f} messages per second".format(throughput))
print("Average latency: {:.3f} milliseconds".format(avg_latency))
print("Maximum message size: {} bytes".format(max_message_size))

# Unsubscribe from the topic and close the Redis connection
subscriber.unsubscribe(topic)
redis_client.close()
