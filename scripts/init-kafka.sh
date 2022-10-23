# blocks until kafka is reachable
kafka-topics --bootstrap-server kafka:29092 --list

for topic in ${TOPICS}; do
	kafka-topics \
		--bootstrap-server \
		kafka:29092 \
		--create --if-not-exists \
		--topic ${topic} \
		--replication-factor 1 --partitions 1
done

echo -e 'Successfully created the following topics:'
kafka-topics --bootstrap-server kafka:29092 --list
