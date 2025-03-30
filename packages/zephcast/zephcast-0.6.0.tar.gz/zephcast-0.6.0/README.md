<div align="center">

# 🌪️ ZephCast

**A powerful and flexible messaging library for Python**

*Unified interface for Kafka, RabbitMQ, and Redis with both sync and async support*

[![PyPI version](https://badge.fury.io/py/zephcast.svg)](https://badge.fury.io/py/zephcast)
[![Documentation Status](https://readthedocs.org/projects/zephcast/badge/?version=latest)](https://zephcast.readthedocs.io/en/latest/)
[![Python versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![License](https://img.shields.io/github/license/zbytealchemy/zephcast)](https://github.com/zbytealchemy/zephcast/blob/main/LICENSE)
[![Tests](https://github.com/zbytealchemy/zephcast/actions/workflows/test.yml/badge.svg)](https://github.com/zbytealchemy/zephcast/actions/workflows/test.yml)
[![Total Downloads](https://static.pepy.tech/personalized-badge/zephcast?period=total&units=international&left_color=grey&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/zephcast)
[![Monthly Downloads](https://static.pepy.tech/personalized-badge/zephcast?period=month&units=international&left_color=grey&right_color=brightgreen&left_text=Downloads/Month)](https://pepy.tech/project/zephcast)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Type Checking: mypy](https://img.shields.io/badge/type%20checking-mypy-blue)](http://mypy-lang.org/)

</div>

<div align="center">

<h3>🔄 One API, Multiple Brokers, Infinite Possibilities 🔄</h3>

</div>

ZephCast provides a clean, consistent API for working with multiple message brokers, making it easy to switch between them or use them together in your applications. Whether you need the robust features of RabbitMQ, the scalability of Kafka, or the simplicity of Redis, ZephCast has you covered with both synchronous and asynchronous interfaces.

## 📚 Documentation

Full documentation is available at [zephcast.readthedocs.io](https://zephcast.readthedocs.io/en/latest/).

## ✨ Features

<table>
  <tr>
    <td width="33%" align="center">
      <h3>🔄 Unified Interface</h3>
      <p>Consistent API across all message brokers</p>
    </td>
    <td width="33%" align="center">
      <h3>⚡ Async Support</h3>
      <p>Native async/await support for all clients</p>
    </td>
    <td width="33%" align="center">
      <h3>🧩 Modular Design</h3>
      <p>Install only the dependencies you need</p>
    </td>
  </tr>
  <tr>
    <td width="33%" align="center">
      <h3>🛡️ Type Safety</h3>
      <p>Full type hints support with mypy validation</p>
    </td>
    <td width="33%" align="center">
      <h3>🔄 Consumer Groups</h3>
      <p>Support for consumer groups in all brokers</p>
    </td>
    <td width="33%" align="center">
      <h3>🛠️ Error Handling</h3>
      <p>Robust error handling and recovery mechanisms</p>
    </td>
  </tr>
</table>

### Supported Brokers

- **Apache Kafka**: Industry-standard distributed streaming platform
- **RabbitMQ**: Feature-rich message broker supporting multiple messaging patterns
- **Redis Streams**: Lightweight, in-memory data structure store

## 📋 Requirements

- Python 3.10+
- Redis 5.0+ (for Redis Streams support)
- Kafka 2.0+
- RabbitMQ 3.8+

## 🔧 Installation

<details open>
<summary><b>Basic Installation</b></summary>

```bash
# Install with poetry (recommended)
poetry add zephcast

# Install with pip
pip install zephcast
```
</details>

<details open>
<summary><b>Optional Dependencies</b></summary>

ZephCast uses a modular dependency system. You can install only what you need:

```bash
# Install everything
pip install zephcast[all]
```

<details>
<summary>Broker-specific installations</summary>

```bash
# Install with specific broker support
pip install zephcast[kafka]    # Kafka support (sync and async)
pip install zephcast[rabbit]   # RabbitMQ support (sync and async)
pip install zephcast[redis]    # Redis support (sync and async)
```
</details>

<details>
<summary>Async-only installations</summary>

```bash
# Install only async support
pip install zephcast[async]    # All async clients
pip install zephcast[aio]      # Alias for async, all async clients
pip install zephcast[async-kafka]   # Only async Kafka
pip install zephcast[async-rabbit]  # Only async RabbitMQ
pip install zephcast[async-redis]   # Only async Redis
```
</details>

<details>
<summary>Sync-only installations</summary>

```bash
# Install only sync support
pip install zephcast[sync]     # All sync clients
pip install zephcast[sync-kafka]    # Only sync Kafka
pip install zephcast[sync-rabbit]   # Only sync RabbitMQ
pip install zephcast[sync-redis]    # Only sync Redis
```
</details>

</details>

## 🚀 Quick Start

### Async Iterator Pattern

All async clients in ZephCast implement the async iterator pattern, allowing you to use them in async for loops:

```python
async with client:  # Automatically connects and closes
    async for message in client:  # Uses receive() under the hood
        print(f"Received: {message}")
```

### Kafka Example

```python
from zephcast.aio.kafka.client import KafkaClient
from zephcast.aio.kafka.config import KafkaConfig

async def kafka_example():
    # Create a client
    client = KafkaClient(
        stream_name="my-topic",
        config=KafkaConfig(
            bootstrap_servers="localhost:9092"
        )
    )
    
    # Using async context manager
    async with client:
        await client.send("Hello Kafka!")
        
        # Receive messages
        async for message in client:
            print(f"Received: {message}")
            break
```

### RabbitMQ Example

```python
from zephcast.aio.rabbit.client import RabbitClient
from zephcast.aio.rabbit.config import RabbitConfig

async def rabbitmq_example():
    client = RabbitClient(
        stream_name="my-routing-key",
        config=RabbitConfig(
            queue_name="my-queue",
            rabbitmq_url="amqp://guest:guest@localhost:5672/"
        )
    )
    
    # Using async context manager
    async with client:
        # Send messages
        await client.send("Hello RabbitMQ!")
        
        # Receive messages
        async for message in client:
            print(f"Received: {message}")
            break
```

### Redis Example

```python
from zephcast.aio.redis.client import RedisClient
from zephcast.aio.redis.config import RedisConfig

async def redis_example():
    client = RedisClient(
        stream_name="my-stream",
        config=RedisConfig(
            redis_url="redis://localhost:6379"
        )
    )
    
    # Using async context manager
    async with client:
        # Send messages
        await client.send("Hello Redis!")
        
        # Receive messages
        async for message in client:
            print(f"Received: {message}")
            break
```

## ⚙️ Configuration

### Environment Variables

ZephCast automatically reads configuration from environment variables:

- `KAFKA_BOOTSTRAP_SERVERS`: Kafka bootstrap servers (default: "localhost:9092")
- `RABBITMQ_URL`: RabbitMQ connection URL (default: "amqp://guest:guest@localhost:5672/")
- `REDIS_URL`: Redis connection URL (default: "redis://localhost:6379")

### Client Configuration

Each client uses a dedicated config class for type-safe configuration:

#### Kafka Config
```python
from zephcast.aio.kafka.config import KafkaConfig

config = KafkaConfig(
    bootstrap_servers="localhost:9092",
    group_id="my-group",
    auto_offset_reset="earliest",
    security_protocol="PLAINTEXT",
    # SASL authentication
    sasl_mechanism="PLAIN",
    sasl_plain_username="user",
    sasl_plain_password="password"
)
```

#### RabbitMQ Config
```python
from zephcast.aio.rabbit.config import RabbitConfig

config = RabbitConfig(
    rabbitmq_url="amqp://guest:guest@localhost:5672/",
    exchange_name="my-exchange",
    exchange_type="direct",  # direct, fanout, topic, headers
    queue_name="my-queue",
    durable=True,
    auto_delete=False
)
```

#### Redis Config
```python
from zephcast.aio.redis.config import RedisConfig

config = RedisConfig(
    redis_url="redis://localhost:6379",
    stream_max_len=1000,  # Maximum stream length
    consumer_group="my-group",
    consumer_name="consumer-1",
    block_ms=5000  # Blocking time in milliseconds
)
```

## 🔍 Advanced Usage

### Consumer Groups

All clients support consumer groups for distributed message processing:

```python
# Kafka Consumer Group
from zephcast.aio.kafka.client import KafkaClient
from zephcast.aio.kafka.config import KafkaConfig

client = KafkaClient(
    stream_name="my-topic",
    config=KafkaConfig(
        bootstrap_servers="localhost:9092",
        group_id="my-group"
    )
)

# RabbitMQ Consumer Group
from zephcast.aio.rabbit.client import RabbitClient
from zephcast.aio.rabbit.config import RabbitConfig

client = RabbitClient(
    stream_name="my-routing-key",
    config=RabbitConfig(
        queue_name="my-queue",
        rabbitmq_url="amqp://guest:guest@localhost:5672/",
        consumer_group="my-group"
    )
)

# Redis Consumer Group
from zephcast.aio.redis.client import RedisClient
from zephcast.aio.redis.config import RedisConfig

client = RedisClient(
    stream_name="my-stream",
    config=RedisConfig(
        redis_url="redis://localhost:6379",
        consumer_group="my-group"
    )
)
```

### Error Handling

ZephCast provides robust error handling mechanisms:

```python
from zephcast.core.exceptions import ZephCastError, ConnectionError

try:
    async with client:
        await client.send("message")
        async for message in client:
            process_message(message)
except ConnectionError:
    # Handle connection errors
    logger.error("Connection failed")
except TimeoutError:
    # Handle timeout errors
    logger.error("Operation timed out")
except ZephCastError as e:
    # Handle ZephCast-specific errors
    logger.error(f"ZephCast error: {e}")
except Exception as e:
    # Handle other errors
    logger.error(f"Unexpected error: {e}")
```

### Retry Mechanisms

ZephCast includes built-in retry mechanisms for handling transient failures:

```python
from zephcast.aio.retry import RetryConfig

# Configure retry behavior
retry_config = RetryConfig(
    max_retries=3,
    retry_delay=1.0,  # seconds
    backoff_factor=2.0,
    exceptions=(ConnectionError, TimeoutError)
)

# Apply retry to client operations
from zephcast.aio.retry import with_retry

@with_retry(retry_config)
async def send_with_retry(client, message):
    await client.send(message)
```
```

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to all contributors who have helped shape ZephCast
- Inspired by the need for a unified messaging interface across different brokers

## Development

### Prerequisites

- Python 3.10+
- Poetry
- Docker (for running integration tests)

### Setup

```bash
# Clone the repository
git clone https://github.com/zbytealchemy/zephcast.git
cd zephcast

# Install dependencies
make install

# Run unit tests
make unit-test
```

### Running Integration Tests

Start the required services:

```bash
docker-compose up -d
```

Run the integration tests:

```bash
make integration-test
```

## Contributing

We use rebase workflow for pull requests and allow no more then 2 commits per PR.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Apache Kafka](https://kafka.apache.org/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [Redis](https://redis.io/)
- [aiokafka](https://github.com/aio-libs/aiokafka)
- [aio-pika](https://github.com/mosquito/aio-pika)
- [redis-py](https://github.com/redis/redis-py)
