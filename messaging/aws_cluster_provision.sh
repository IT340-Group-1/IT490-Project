# https://docs.aws.amazon.com/cli/latest/reference/mq/create-broker.html

aws mq create-broker \
--broker-name CRARabbitMQBrokerCluster \
--engine-type ACTIVEMQ \
--engine-version 5.15.9 \
--auto-minor-version-upgrade \
--deployment-mode CLUSTER_MULTI_AZ \
--host-instance-type mq.t2.micro \
--publicly-accessible \
--authentication-strategy SIMPLE \
--users '{"Username":"admin","Password":"RMQ-Pa55w0rd"}'
