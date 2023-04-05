# https://docs.aws.amazon.com/cli/latest/reference/mq/create-broker.html

aws mq create-broker \
--broker-name CRARabbitMQBroker \
--engine-type RABBITMQ \
--engine-version 3.10.10 \
--auto-minor-version-upgrade \
--deployment-mode SINGLE_INSTANCE \
--host-instance-type mq.t3.micro \
--publicly-accessible \
--authentication-strategy SIMPLE \
--users '{"Username":"admin","Password":"RMQ-Pa55w0rd"}'
