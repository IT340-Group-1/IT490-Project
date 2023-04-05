aws mq delete-broker \
--broker-id $(aws mq list-brokers --query 'BrokerSummaries[?BrokerName==`CRARabbitMQBroker`].BrokerId' --output text)
