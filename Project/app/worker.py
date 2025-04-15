import json
import time
import pika
from database.database import get_session, engine
from models.crud.prediction_task import create as create_prediction_task


def callback(ch, method, properties, body):
    print("Получено сообщение:", body)
    try:
        # Предположим, сообщение приходит как JSON
        message = json.loads(body)
        user_id = message.get("user_id")
        budget_amount = message.get("budget_amount")
        preferences = message.get("preferences")
    except Exception as e:
        print("Ошибка обработки сообщения:", e)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    # Создаем сессию для работы с БД; используем context manager для автоматического закрытия
    session = next(get_session())
    # Поскольку алгоритм предсказания отсутствует, мы просто формируем фиктивный результат:
    simulated_result = f"Simulated result for budget {budget_amount} and preferences {preferences}"

    # Вызываем функцию, которая обрабатывает задачу предсказания:
    print(create_prediction_task(session, user_id, budget_amount, preferences, simulated_result))

    # Подтверждаем получение сообщения
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("\n\n\n\n\n\n\n\nЗадача обработана, баланс обновлен, транзакция и результат сохранены.\n\n\n\n\n\n")


def create_connection(max_attempts=10):
    for attempt in range(max_attempts):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq", heartbeat=100))
            print("Соединение установлено.")
            return connection
        except pika.exceptions.AMQPConnectionError as err:
            print(f"Попытка {attempt+1}: не удалось установить соединение с RabbitMQ, повтор через 5 секунд...")
            time.sleep(5)
    raise Exception("Не удалось установить соединение с RabbitMQ после нескольких попыток.")


def main():
    # Настраиваем подключение к RabbitMQ. Обратите внимание, что хост должен быть именем сервиса RabbitMQ (например, "rabbitmq")
    connection = create_connection()
    channel = connection.channel()

    # Объявляем очередь (durable означает, что сообщения сохраняются при перезапуске сервера)
    channel.queue_declare(queue="prediction_tasks", durable=True)

    # Ограничиваем количество не подтвержденных сообщений
    channel.basic_qos(prefetch_count=1)

    # Подписываемся на очередь
    channel.basic_consume(queue="prediction_tasks", on_message_callback=callback)

    print("Worker запущен. Ожидаем сообщений...")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Worker остановлен вручную.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    print('\n\n\nworker is here\n\n\n')
    main()
