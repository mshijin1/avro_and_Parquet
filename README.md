# avro_and_Parquet
# AVRO and PARQUET for Big Data Storage

Efficient data storage is a critical part of any big data system.  
**Avro** excels in data streaming and schema evolution.  
**Parquet** is optimized for analytics and storage efficiency.

---

## 📊 Comparison Table

| **Features** | **Avro** | **Parquet** |
|--------------|----------|-------------|
| **Storage Format** | Row-based, stores entire records sequentially | Columnar-based, stores entire data by columns |
| **Best for** | Streaming data, event data, schema evolution | Analytical queries, big data analytics |
| **Schema Evolution** | Excellent – schema is stored with data, allowing seamless updates | Limited |
| **Compression** | Compact binary encoding but less optimized for analytics | Highly compressed using columnar compression techniques:<br>1. Dictionary encoding<br>2. Run-length encoding<br>3. Bit packing |
| **Read Performance** | Slow for analytics since entire rows must be read | Faster for analytics since a particular column is read |
| **Write Performance** | Fast – appends entire row quickly | Slow – columnar storage requires additional processing |
| **Query Efficiency** | Inefficient for analytics queries | Highly efficient – only required columns are scanned |
| **File Size** | Larger due to row-based structure | Smaller due to better compression techniques |
| **Use Cases** | Event-driven architecture, Kafka messaging systems, log storage | Data lakes, data warehouses, ETL processes, analytical workloads |
| **Processing Frameworks** | Works well with Apache Kafka, Hadoop, and Spark | Optimized for Apache Spark |
| **Support for Nested Data** | Supports nested data but requires schema definition | Optimized for nested structures (hierarchical data) |
| **Interoperability** | Widely used in streaming platforms | Preferred for big data processing and analytical workloads |
| **File Extension** | `.avro` | `.parquet` |
| **Primary Industry Adoption** | Streaming platforms, logging, real-time pipelines | Analytics, data warehousing, business intelligence |

---

## 📌 Which One Should You Choose?

| **Use Case** | **Preferred Format** |
|--------------|----------------------|
| Real-time streaming (Kafka, logs, messaging) | Avro |
| Frequent schema changes / evolving data structures | Avro |
| Row-based storage for fast writes | Avro |
| Data exchange between applications | Avro |
| Big data analytics and querying | Parquet |
| Efficient storage and compression | Parquet |
| Read-heavy workloads (data lakes, warehousing) | Parquet |
| Columnar-based querying and filtering | Parquet |

---

## 🔍 Row-Based vs. Columnar Storage

**Sample Dataset**:

| ID  | Name  | Age | City      |
|-----|-------|-----|-----------|
| 101 | Alice | 25  | New York  |
| 102 | Bob   | 30  | Chicago   |
| 103 | Carol | 28  | Seattle   |

**Avro (Row-based)**:
[101, Alice, 25, New York]
[102, Bob, 30, Chicago]
[103, Carol, 28, Seattle]

> Each record is stored as an individual row. Slow for querying specific fields.

**Parquet (Columnar-based)**:
ID: [101, 102, 103]
Name: [Alice, Bob, Carol]
Age: [25, 30, 28]
City: [New York, Chicago, Seattle]


> Each column is stored separately, making it faster to retrieve only required columns.

---

## ⚙ How Avro and Parquet Work with Big Data Tools

### Apache Kafka
Kafka is a real-time data streaming platform, and Avro is a standard for message serialization.

**Why Avro is preferred in Kafka**:
- Compact binary format reduces bandwidth and storage costs.
- Schema evolution ensures compatibility between producers and consumers.

#### `avro_producer.py`
```python
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

value_schema_str = """
{
    "namespace": "example.avro",
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"}
    ]
}
"""

schema_registry_conf = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_conf)

avro_serializer = AvroSerializer(
    schema_str=value_schema_str,
    schema_registry_client=schema_registry_client
)

producer = SerializingProducer(
    {'bootstrap.servers': 'localhost:9092',
     'value.serializer': avro_serializer}
)

producer.produce(topic='avro_topic', value={"id": 6, "name": "Shijin"})
producer.flush()
```

#### `avro_consumer.py'
```python
from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

schema_registry_url = {'url': 'http://localhost:8081'}
schema_registry_client = SchemaRegistryClient(schema_registry_url)

value_schema_str = """
{
    "namespace": "example.avro",
    "type": "record",
    "name": "User",
    "fields": [
        {"name": "id", "type": "int"},
        {"name": "name", "type": "string"}
    ]
}
"""

avro_deserializer = AvroDeserializer(schema_registry_client=schema_registry_client)

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'avro-consumer-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
})

consumer.subscribe(['avro_topic'])

print("Starting Avro consumer...")

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        value = avro_deserializer(
            msg.value(),
            SerializationContext(msg.topic(), MessageField.VALUE)
        )
        print("Received value:", value)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()
```

# Apache Spark
Apache Spark supports both Avro and Parquet, but each has advantages depending on the use case.

Using Avro in Spark
Ideal for data ingestion and ETL pipelines.

Allows schema evolution (preferred for Kafka pipelines).

Often used before converting to Parquet for analytics.
```
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("AvroExample").getOrCreate()
```

# Read Avro file
```
df = spark.read.format("avro").load("data.avro")
df.show()
```

# Write DataFrame to Avro
```
df.write.format("avro").save("output.avro")
```

Using Parquet in Spark
Optimized for analytics and batch processing.

Columnar storage reduces I/O and speeds queries.

Default format in many data lakes.

# Read Parquet file
```
df = spark.read.parquet("data.parquet")
df.show()
```

# Write DataFrame to Parquet
```
df.write.mode("overwrite").parquet("output.parquet")
```

🐍 Basic Implementation in Python
Install dependencies:
```
pip install pandas pyarrow
```
```
import pandas as pd

# Sample DataFrame
data = {
    'Name': ['Alice', 'Jacob', 'Charlie'],
    'Age': [25, 30, 35],
    'Salary': [50000, 60000, 70000]
}

df = pd.DataFrame(data)
```
# Save DataFrame to Parquet
```
df.to_parquet('employee.parquet', engine='pyarrow', compression='snappy')
```
# Read the Parquet dataset
```
load_df = pd.read_parquet('employee.parquet', engine='pyarrow')
print(load_df)
```
# Filtering Columns (Parquet Advantage):
```
df.to_parquet('data.parquet', engine='pyarrow', compression='snappy')

df_subset = pd.read_parquet('data.parquet', columns=['Name', 'Age'])
print(df_subset)
```

Parquet shines here – unused columns are not loaded.

📌 Conclusion: 
Use Avro when you need real-time streaming, schema evolution, and row-based storage.

Use Parquet for big data analytics, storage efficiency, and columnar queries.

---

