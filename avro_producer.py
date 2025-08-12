from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


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

schema_registry_conf={'url':'http://localhost:8083'}
schema_registry_client=SchemaRegistryClient(schema_registry_conf)

avro_serializer=AvroSerializer(
    schema_str=value_schema_str,
    schema_registry_client=schema_registry_client
)

producer=SerializingProducer({'bootstrap.servers':'localhost:9098',
                            #   'key.serializer':str.encode,
                              'value.serializer':avro_serializer})

producer.produce(topic='avro_topic',value={"id": 1, "name":"hsdfd"})
producer.flush()