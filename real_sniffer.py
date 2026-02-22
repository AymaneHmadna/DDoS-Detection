import time
import json
import random
from scapy.all import sniff, IP, TCP, UDP
from kafka import KafkaProducer
KAFKA_SERVER = 'localhost:9092' 
print(f"Connecting to Kafka {KAFKA_SERVER}...")
try:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    print("Connected! Sending real-time traffic...")
except Exception as e:
    print(f"Kafka Error : {e}")
    exit()
def process_packet(packet):
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        p_len = len(packet)
        port = 0
        if TCP in packet: port = packet[TCP].dport
        elif UDP in packet: port = packet[UDP].dport
        errs = 0
        if port > 1024 and port != 443:
             errs = random.choices([0, 1], weights=[0.9, 0.1])[0]
        data = {
            "ip": src,
            "ports_accessed": int(port),
            "session_duration": round(p_len/1000, 3),
            "errors": errs,
            "timestamp": time.time(),
            "target": dst
        }
        producer.send('network-traffic', data)
        print(f"[KAFKA] {src} -> :{port}")
try:
    sniff(filter="ip", prn=process_packet, store=0)
except PermissionError:
    print("RUN AS ADMINISTRATOR")