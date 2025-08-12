from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField

schema_registry_url={'url':'http://localhost:8083'}
schema_registry_client=SchemaRegistryClient(schema_registry_url)

value_schema_str="""
{
    "namespace":"example.avro",
    "type":"record",
    "name":"User",
    "fields":[
        {"name":"id", "type":"int"},
        {"name":"name", "type":"string"}
    ]
}
"""
# Define deserializer 
avro_deserializer=AvroDeserializer(schema_registry_client=schema_registry_client)

# Kafka consumer configuration
consumer=Consumer(
    {
        'bootstrap.servers':'localhost:9098',
        'group.id':'avro-consumer-group',
        'auto.offset.reset':'earliest',
        'enable.auto.commit':True,
        # 'key.deserializer':str,
        # 'value.deserializer':avro_deserializer
    }
)

# Use your topic
consumer.subscribe(['avro_topic'])

print("Starting Avro consumer....")

try:
    while True:
        msg=consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        
        # Deserialize value
        value=avro_deserializer(msg.value(), SerializationContext(msg.topic(),MessageField.VALUE))
        print("Recieved value: ",value)
except KeyboardInterrupt:
    pass
finally:
    consumer.close()