import pika, time, json

def process_task(ch, method, properties, body):
    from people_detector import get_photo_from_web, people_detector

    task = json.loads(body)
    url = task.get("url")
    print(f"Processing image from URL: {url}")

    try:
        image = get_photo_from_web(url)
        people_count = people_detector(image)
        print(f"People count: {people_count}")
    except Exception as e:
        print(f"Error processing task: {e}")
    
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='people_detector', durable=True)

    channel.basic_consume(queue='people_detector', on_message_callback=process_task)

    print("Worker started. Waiting for tasks...")
    channel.start_consuming()

start_worker()