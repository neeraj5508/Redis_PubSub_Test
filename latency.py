import time
import redis
import string
import random
from PIL import Image
import io

# Connect to Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Subscribe to test channel
pubsub = redis_client.pubsub()
pubsub.subscribe('test_channel')

# Generate a large message (10 MB)
message_size = 10 * 1024 * 1024
large_message = ''.join(random.choice(string.ascii_letters) for _ in range(message_size))

# Publish messages
num_messages = 100
for i in range(num_messages):
    # Integer message
    int_message = {'type': 'integer', 'data': i, 'timestamp': time.time()}
    redis_client.publish('test_channel', str(int_message))

    # String message
    str_message = {'type': 'string', 'data': f'message {i}', 'timestamp': time.time()}
    redis_client.publish('test_channel', str(str_message))

    # Image message
    image_file = 'icon.png'
    with open(image_file, 'rb') as f:
        image_data = f.read()

    # Convert image data to bytes string
    image_bytes = io.BytesIO(image_data)
    image_str = image_bytes.read()

    # Send image message
    image_message = {'type': 'image', 'data': image_str, 'timestamp': time.time()}
    redis_client.publish('test_channel', str(image_message))

# Get messages and calculate latency
latency_sum = 0
for i in range(num_messages * 3):
    message = pubsub.get_message()
    if message and message['type'] == 'message':
        message_data = eval(message['data'])
        latency = (time.time() - float(message_data['timestamp'])) * 1000
        latency_sum += latency

# Calculate average latency
avg_latency = latency_sum / (num_messages * 3)
print(f'Redis pub/sub latency: {avg_latency:.2f} ms')


# Testing throughput
message_size = 100000
total_messages = 1000

start_time = time.time()

for i in range(total_messages):
        message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=message_size))
        redis_client.publish("test", message)

elapsed_time = time.time() - start_time
print(f"Throughput: {total_messages / elapsed_time:.2f} messages per second")

# Testing maximum size of data
message_size = 10000
message = ''.join(random.choices(string.ascii_uppercase + string.digits, k=message_size))

try:
        redis_client.publish("test", message)
        print("Successfully published message of maximum size")
except redis.exceptions.ResponseError:
        print("Failed to publish message of maximum size")



