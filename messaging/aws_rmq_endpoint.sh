aws mq describe-broker --broker-id $(aws mq list-brokers --query 'BrokerSummaries[?BrokerName==`CRARabbitMQBroker`].BrokerId' --output text) --query 'BrokerInstances[?ConsoleURL!=`null`].Endpoints[0]' --output text > ip.txt

echo "def rmq_url(): return '$(<ip.txt)'" > ../backend/bermq/rmq_url.py
echo "def rmq_url(): return '$(<ip.txt)'" > ../frontend/craui/rmq_url.py
echo "def rmq_url(): return '$(<ip.txt)'" > ../database/rmq_url.py
