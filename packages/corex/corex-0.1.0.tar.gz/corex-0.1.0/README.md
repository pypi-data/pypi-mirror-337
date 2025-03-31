# CoreX: The Python Core Interfaces Standard

## What is CoreX?
CoreX is a modular, standardized interface framework for Python applications. It provides a consistent API for essential cross-cutting concerns such as storage, caching, messaging, security, databases, event processing, AI, and more.

By using CoreX, developers can build highly interoperable, pluggable, and maintainable software architectures.

## Why CoreX?
Modern applications depend on multiple third-party services, libraries, and APIs. However, without a unified standard, developers face issues such as:
- Vendor Lock-in – Switching from Redis to Memcached? Migrating from S3 to Azure Blob? CoreX makes this painless.
- Inconsistent APIs – Every library has its own way of doing things. CoreX normalizes them.
- Difficult Code Maintenance – CoreX provides clear abstractions that simplify complex software.

## Key Features
- Modular – Pick and use only the components you need.
- Standardized – Every package follows a strict interface contract.
- Interoperable – Works with multiple libraries (e.g., boto3, redis-py, requests).
- Extendable – Implement your own handlers for any system.
- Pluggable – Swap out any implementation dynamically via configuration.


## Configuration

CoreX supports dynamic backend configuration via YAML files. For each CoreX component (e.g., storage, cache, messaging, AI), define your chosen backend and its initialization parameters directly in a `corex_config.yaml` file. CoreX will dynamically load and instantiate these backends at runtime using the built-in `corex.config_loader`.

### Example YAML Configuration:

~~~yaml
storage:
  backend: "corex_storage_minio.handler.MinioHandler"
  init_args:
    endpoint: "play.min.io"
    bucket: "my-bucket"
    access_key: "your-access-key"
    secret_key: "your-secret-key"

cache:
  backend: "corex_cache_redis.handler.RedisCache"
  init_args:
    host: "localhost"
    port: 6379
    db: 0

messaging:
  backend: "corex_messaging_nats.handler.NatsMessenger"
  init_args:
    url: "nats://localhost:4222"
~~~

### Using the Config Loader:

To dynamically load and use configured backends, import the CoreX config loader in your Python application:

~~~python
from corex.config_loader import (
    load_storage_backend,
    load_cache_backend,
    load_messaging_backend,
)

storage = load_storage_backend("corex_config.yaml")
cache = load_cache_backend("corex_config.yaml")
messenger = load_messaging_backend("corex_config.yaml")

storage.save("local.txt", "remote/path.txt")
cache.set("key", "value")
messenger.send("notifications", "File uploaded successfully.")
~~~

This pattern allows seamless backend swaps without altering your application code—simply update your YAML configuration and restart the app.


## CoreX Modules
Each CoreX module represents a different functional category. Below is the complete list of interfaces and implementations.

### Storage
- [corex-storage-s3](./examples/storage/example_s3.py)  
  ~~~bash
  pip install corex-storage-s3
  ~~~
- [corex-storage-local](./examples/storage/example_local.py)  
  ~~~bash
  pip install corex-storage-local
  ~~~
- [corex-storage-gcs](./examples/storage/example_gcs.py)  
  ~~~bash
  pip install corex-storage-gcs
  ~~~
- [corex-storage-azure_blob](./examples/storage/example_azure_blob.py)  
  ~~~bash
  pip install corex-storage-azure_blob
  ~~~
- [corex-storage-minio](./examples/storage/example_minio.py)  
  ~~~bash
  pip install corex-storage-minio
  ~~~
- [corex-storage-ceph](./examples/storage/example_ceph.py)  
  ~~~bash
  pip install corex-storage-ceph
  ~~~
- [corex-storage-hdfs](./examples/storage/example_hdfs.py)  
  ~~~bash
  pip install corex-storage-hdfs
  ~~~
- [corex-storage-ipfs](./examples/storage/example_ipfs.py)  
  ~~~bash
  pip install corex-storage-ipfs
  ~~~

### Caching
- [corex-cache-redis](./examples/cache/example_redis.py)  
  ~~~bash
  pip install corex-cache-redis
  ~~~
- [corex-cache-memcached](./examples/cache/example_memcached.py)  
  ~~~bash
  pip install corex-cache-memcached
  ~~~
- [corex-cache-hazelcast](./examples/cache/example_hazelcast.py)  
  ~~~bash
  pip install corex-cache-hazelcast
  ~~~
- [corex-cache-aerospike](./examples/cache/example_aerospike.py)  
  ~~~bash
  pip install corex-cache-aerospike
  ~~~
- [corex-cache-etcd](./examples/cache/example_etcd.py)  
  ~~~bash
  pip install corex-cache-etcd
  ~~~
- [corex-cache-couchbase](./examples/cache/example_couchbase.py)  
  ~~~bash
  pip install corex-cache-couchbase
  ~~~
- [corex-cache-ignite](./examples/cache/example_ignite.py)  
  ~~~bash
  pip install corex-cache-ignite
  ~~~

### Messaging
- [corex-messaging-kafka](./examples/messaging/example_kafka.py)  
  ~~~bash
  pip install corex-messaging-kafka
  ~~~
- [corex-messaging-rabbitmq](./examples/messaging/example_rabbitmq.py)  
  ~~~bash
  pip install corex-messaging-rabbitmq
  ~~~
- [corex-messaging-nats](./examples/messaging/example_nats.py)  
  ~~~bash
  pip install corex-messaging-nats
  ~~~
- [corex-messaging-sns](./examples/messaging/example_sns.py)  
  ~~~bash
  pip install corex-messaging-sns
  ~~~
- [corex-messaging-sqs](./examples/messaging/example_sqs.py)  
  ~~~bash
  pip install corex-messaging-sqs
  ~~~
- [corex-messaging-pulsar](./examples/messaging/example_pulsar.py)  
  ~~~bash
  pip install corex-messaging-pulsar
  ~~~
- [corex-messaging-activemq](./examples/messaging/example_activemq.py)  
  ~~~bash
  pip install corex-messaging-activemq
  ~~~
- [corex-messaging-zeromq](./examples/messaging/example_zeromq.py)  
  ~~~bash
  pip install corex-messaging-zeromq
  ~~~

### Configuration Management
- [corex-config-file](./examples/config/example_file.py)  
  ~~~bash
  pip install corex-config-file
  ~~~
- [corex-config-env](./examples/config/example_env.py)  
  ~~~bash
  pip install corex-config-env
  ~~~
- [corex-config-consul](./examples/config/example_consul.py)  
  ~~~bash
  pip install corex-config-consul
  ~~~
- [corex-config-zookeeper](./examples/config/example_zookeeper.py)  
  ~~~bash
  pip install corex-config-zookeeper
  ~~~
- [corex-config-vault](./examples/config/example_vault.py)  
  ~~~bash
  pip install corex-config-vault
  ~~~
- [corex-config-etcd](./examples/config/example_etcd.py)  
  ~~~bash
  pip install corex-config-etcd
  ~~~
- [corex-config-nacos](./examples/config/example_nacos.py)  
  ~~~bash
  pip install corex-config-nacos
  ~~~

### Metrics & Monitoring
- [corex-metrics-prometheus](./examples/metrics/example_prometheus.py)  
  ~~~bash
  pip install corex-metrics-prometheus
  ~~~
- [corex-metrics-datadog](./examples/metrics/example_datadog.py)  
  ~~~bash
  pip install corex-metrics-datadog
  ~~~
- [corex-metrics-newrelic](./examples/metrics/example_newrelic.py)  
  ~~~bash
  pip install corex-metrics-newrelic
  ~~~
- [corex-metrics-opentelemetry](./examples/metrics/example_opentelemetry.py)  
  ~~~bash
  pip install corex-metrics-opentelemetry
  ~~~
- [corex-metrics-graphite](./examples/metrics/example_graphite.py)  
  ~~~bash
  pip install corex-metrics-graphite
  ~~~
- [corex-metrics-cloudwatch](./examples/metrics/example_cloudwatch.py)  
  ~~~bash
  pip install corex-metrics-cloudwatch
  ~~~
- [corex-metrics-influxdb](./examples/metrics/example_influxdb.py)  
  ~~~bash
  pip install corex-metrics-influxdb
  ~~~

### Security & Authentication
- [corex-security-auth0](./examples/security/example_auth0.py)  
  ~~~bash
  pip install corex-security-auth0
  ~~~
- [corex-security-ldap](./examples/security/example_ldap.py)  
  ~~~bash
  pip install corex-security-ldap
  ~~~
- [corex-security-oauth2](./examples/security/example_oauth2.py)  
  ~~~bash
  pip install corex-security-oauth2
  ~~~
- [corex-security-saml](./examples/security/example_saml.py)  
  ~~~bash
  pip install corex-security-saml
  ~~~
- [corex-security-kerberos](./examples/security/example_kerberos.py)  
  ~~~bash
  pip install corex-security-kerberos
  ~~~
- [corex-security-jwt](./examples/security/example_jwt.py)  
  ~~~bash
  pip install corex-security-jwt
  ~~~
- [corex-security-mfa](./examples/security/example_mfa.py)  
  ~~~bash
  pip install corex-security-mfa
  ~~~
- [corex-security-tls](./examples/security/example_tls.py)  
  ~~~bash
  pip install corex-security-tls
  ~~~
- [corex-security-openid_connect](./examples/security/example_openid_connect.py)  
  ~~~bash
  pip install corex-security-openid_connect
  ~~~

### Databases
- [corex-database-postgresql](./examples/database/example_postgresql.py)  
  ~~~bash
  pip install corex-database-postgresql
  ~~~
- [corex-database-mysql](./examples/database/example_mysql.py)  
  ~~~bash
  pip install corex-database-mysql
  ~~~
- [corex-database-sqlite](./examples/database/example_sqlite.py)  
  ~~~bash
  pip install corex-database-sqlite
  ~~~
- [corex-database-mongodb](./examples/database/example_mongodb.py)  
  ~~~bash
  pip install corex-database-mongodb
  ~~~
- [corex-database-cassandra](./examples/database/example_cassandra.py)  
  ~~~bash
  pip install corex-database-cassandra
  ~~~
- [corex-database-cockroachdb](./examples/database/example_cockroachdb.py)  
  ~~~bash
  pip install corex-database-cockroachdb
  ~~~
- [corex-database-dynamodb](./examples/database/example_dynamodb.py)  
  ~~~bash
  pip install corex-database-dynamodb
  ~~~
- [corex-database-firestore](./examples/database/example_firestore.py)  
  ~~~bash
  pip install corex-database-firestore
  ~~~
- [corex-database-oracle](./examples/database/example_oracle.py)  
  ~~~bash
  pip install corex-database-oracle
  ~~~
- [corex-database-mssql](./examples/database/example_mssql.py)  
  ~~~bash
  pip install corex-database-mssql
  ~~~
- [corex-database-neo4j](./examples/database/example_neo4j.py)  
  ~~~bash
  pip install corex-database-neo4j
  ~~~
- [corex-database-elasticsearch](./examples/database/example_elasticsearch.py)  
  ~~~bash
  pip install corex-database-elasticsearch
  ~~~

### Events & Pub/Sub
- [corex-events-sns](./examples/events/example_sns.py)  
  ~~~bash
  pip install corex-events-sns
  ~~~
- [corex-events-sqs](./examples/events/example_sqs.py)  
  ~~~bash
  pip install corex-events-sqs
  ~~~
- [corex-events-kafka](./examples/events/example_kafka.py)  
  ~~~bash
  pip install corex-events-kafka
  ~~~
- [corex-events-eventbridge](./examples/events/example_eventbridge.py)  
  ~~~bash
  pip install corex-events-eventbridge
  ~~~
- [corex-events-nats](./examples/events/example_nats.py)  
  ~~~bash
  pip install corex-events-nats
  ~~~
- [corex-events-pulsar](./examples/events/example_pulsar.py)  
  ~~~bash
  pip install corex-events-pulsar
  ~~~
- [corex-events-google_pubsub](./examples/events/example_google_pubsub.py)  
  ~~~bash
  pip install corex-events-google_pubsub
  ~~~

### Logging
- [corex-logging-cloudwatch](./examples/logging/example_cloudwatch.py)  
  ~~~bash
  pip install corex-logging-cloudwatch
  ~~~
- [corex-logging-datadog](./examples/logging/example_datadog.py)  
  ~~~bash
  pip install corex-logging-datadog
  ~~~
- [corex-logging-loki](./examples/logging/example_loki.py)  
  ~~~bash
  pip install corex-logging-loki
  ~~~
- [corex-logging-splunk](./examples/logging/example_splunk.py)  
  ~~~bash
  pip install corex-logging-splunk
  ~~~
- [corex-logging-elasticsearch](./examples/logging/example_elasticsearch.py)  
  ~~~bash
  pip install corex-logging-elasticsearch
  ~~~
- [corex-logging-graylog](./examples/logging/example_graylog.py)  
  ~~~bash
  pip install corex-logging-graylog
  ~~~
- [corex-logging-logstash](./examples/logging/example_logstash.py)  
  ~~~bash
  pip install corex-logging-logstash
  ~~~
- [corex-logging-papertrail](./examples/logging/example_papertrail.py)  
  ~~~bash
  pip install corex-logging-papertrail
  ~~~

### AI & Machine Learning

#### Natural Language Processing (NLP)
- [corex-ai_nlp-openai](./examples/ai_nlp/example_openai.py)  
  ~~~bash
  pip install corex-ai_nlp-openai
  ~~~
- [corex-ai_nlp-huggingface](./examples/ai_nlp/example_huggingface.py)  
  ~~~bash
  pip install corex-ai_nlp-huggingface
  ~~~
- [corex-ai_nlp-llama](./examples/ai_nlp/example_llama.py)  
  ~~~bash
  pip install corex-ai_nlp-llama
  ~~~
- [corex-ai_nlp-mistral](./examples/ai_nlp/example_mistral.py)  
  ~~~bash
  pip install corex-ai_nlp-mistral
  ~~~
- [corex-ai_nlp-falcon](./examples/ai_nlp/example_falcon.py)  
  ~~~bash
  pip install corex-ai_nlp-falcon
  ~~~
- [corex-ai_nlp-bloom](./examples/ai_nlp/example_bloom.py)  
  ~~~bash
  pip install corex-ai_nlp-bloom
  ~~~
- [corex-ai_nlp-jurassic](./examples/ai_nlp/example_jurassic.py)  
  ~~~bash
  pip install corex-ai_nlp-jurassic
  ~~~
- [corex-ai_nlp-cohere](./examples/ai_nlp/example_cohere.py)  
  ~~~bash
  pip install corex-ai_nlp-cohere
  ~~~

#### Computer Vision
- [corex-ai_vision-clip](./examples/ai_vision/example_clip.py)  
  ~~~bash
  pip install corex-ai_vision-clip
  ~~~
- [corex-ai_vision-sam](./examples/ai_vision/example_sam.py)  
  ~~~bash
  pip install corex-ai_vision-sam
  ~~~
- [corex-ai_vision-yolov5](./examples/ai_vision/example_yolov5.py)  
  ~~~bash
  pip install corex-ai_vision-yolov5
  ~~~
- [corex-ai_vision-detectron2](./examples/ai_vision/example_detectron2.py)  
  ~~~bash
  pip install corex-ai_vision-detectron2
  ~~~
- [corex-ai_vision-dino](./examples/ai_vision/example_dino.py)  
  ~~~bash
  pip install corex-ai_vision-dino
  ~~~

#### Speech & Audio Processing
- [corex-ai_audio-whisper](./examples/ai_audio/example_whisper.py)  
  ~~~bash
  pip install corex-ai_audio-whisper
  ~~~
- [corex-ai_audio-nemo](./examples/ai_audio/example_nemo.py)  
  ~~~bash
  pip install corex-ai_audio-nemo
  ~~~
- [corex-ai_audio-torchaudio](./examples/ai_audio/example_torchaudio.py)  
  ~~~bash
  pip install corex-ai_audio-torchaudio
  ~~~
- [corex-ai_audio-deepspeech](./examples/ai_audio/example_deepspeech.py)  
  ~~~bash
  pip install corex-ai_audio-deepspeech
  ~~~
- [corex-ai_audio-coqui_tts](./examples/ai_audio/example_coqui_tts.py)  
  ~~~bash
  pip install corex-ai_audio-coqui_tts
  ~~~

#### Embeddings
- [corex-ai_embeddings-sentence_transformers](./examples/ai_embeddings/example_sentence_transformers.py)  
  ~~~bash
  pip install corex-ai_embeddings-sentence_transformers
  ~~~
- [corex-ai_embeddings-fasttext](./examples/ai_embeddings/example_fasttext.py)  
  ~~~bash
  pip install corex-ai_embeddings-fasttext
  ~~~
- [corex-ai_embeddings-gensim](./examples/ai_embeddings/example_gensim.py)  
  ~~~bash
  pip install corex-ai_embeddings-gensim
  ~~~
- [corex-ai_embeddings-tiktoken](./examples/ai_embeddings/example_tiktoken.py)  
  ~~~bash
  pip install corex-ai_embeddings-tiktoken
  ~~~
- [corex-ai_embeddings-faiss](./examples/ai_embeddings/example_faiss.py)  
  ~~~bash
  pip install corex-ai_embeddings-faiss
  ~~~
- [corex-ai_embeddings-weaviate](./examples/ai_embeddings/example_weaviate.py)  
  ~~~bash
  pip install corex-ai_embeddings-weaviate
  ~~~

#### Retrieval & Indexing
- [corex-ai_retrieval-llama_index](./examples/ai_retrieval/example_llama_index.py)  
  ~~~bash
  pip install corex-ai_retrieval-llama_index
  ~~~
- [corex-ai_retrieval-haystack](./examples/ai_retrieval/example_haystack.py)  
  ~~~bash
  pip install corex-ai_retrieval-haystack
  ~~~
- [corex-ai_retrieval-qdrant](./examples/ai_retrieval/example_qdrant.py)  
  ~~~bash
  pip install corex-ai_retrieval-qdrant
  ~~~
- [corex-ai_retrieval-pinecone](./examples/ai_retrieval/example_pinecone.py)  
  ~~~bash
  pip install corex-ai_retrieval-pinecone
  ~~~
- [corex-ai_retrieval-milvus](./examples/ai_retrieval/example_milvus.py)  
  ~~~bash
  pip install corex-ai_retrieval-milvus
  ~~~

#### AI Runtimes & Execution
- [corex-ai_runtimes-vllm](./examples/ai_runtimes/example_vllm.py)  
  ~~~bash
  pip install corex-ai_runtimes-vllm
  ~~~
- [corex-ai_runtimes-text_generation_webui](./examples/ai_runtimes/example_text_generation_webui.py)  
  ~~~bash
  pip install corex-ai_runtimes-text_generation_webui
  ~~~
- [corex-ai_runtimes-ollama](./examples/ai_runtimes/example_ollama.py)  
  ~~~bash
  pip install corex-ai_runtimes-ollama
  ~~~
- [corex-ai_runtimes-ray](./examples/ai_runtimes/example_ray.py)  
  ~~~bash
  pip install corex-ai_runtimes-ray
  ~~~
- [corex-ai_runtimes-tensor_rt](./examples/ai_runtimes/example_tensor_rt.py)  
  ~~~bash
  pip install corex-ai_runtimes-tensor_rt
  ~~~





## Installation
Each CoreX module can be installed individually based on your needs.

Example (Installing Storage & Cache Modules):
~~~bash
pip install corex-storage-s3 corex-cache-redis
~~~

For all available modules, check [PyPI](https://pypi.org/).

## Configuration
CoreX supports dynamic configuration via YAML. Define your corex_config.yaml and specify your preferred implementations.

Example Configuration:
~~~yaml
storage:
  backend: "corex_storage_s3.handler.S3Handler"
  init_args:
    bucket: "my-bucket"

cache:
  backend: "corex_cache_redis.handler.RedisCache"
  init_args:
    host: "localhost"
    port: 6379
~~~

Use the configuration loader to initialize CoreX dynamically:
~~~python
from corex.config_loader import load_storage_backend, load_cache_backend

storage = load_storage_backend("corex_config.yaml")
cache = load_cache_backend("corex_config.yaml")
~~~

## Contributing
We welcome contributions.
To contribute:
1. Fork the repository.
2. Implement improvements or new handlers.
3. Submit a Pull Request.

Follow our CONTRIBUTING.md for guidelines.

## License



## Contact & Support
- Email: js@intelligent-intern.com
- GitHub Issues: https://github.com/intelligent-intern/corex/issues

CoreX – The Future of Standardized Python Interfaces.
