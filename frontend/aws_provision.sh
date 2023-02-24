aws ec2 import-key-pair --key-name "cra_ssh_key" \
    --public-key-material fileb://~/.ssh/cra_ssh_key.pub

aws ec2 create-security-group --group-name cra_security_group \
    --description "Security group used by CRA project"

aws ec2 authorize-security-group-ingress --group-name cra_security_group \
    --protocol tcp --port 22 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress --group-name cra_security_group \
    --protocol tcp --port 7007 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress --group-name cra_security_group \
    --protocol tcp --port 80 --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress --group-name cra_security_group \
    --protocol tcp --port 443 --cidr 0.0.0.0/0

aws ec2 run-instances --image-id ami-0557a15b87f6559cf --count 1 --instance-type t2.micro \
    --key-name cra_ssh_key --security-groups cra_security_group \
    --tag-specifications \
        "ResourceType=instance,Tags=[{Key=Name,Value=cra_frontend}]" \
        "ResourceType=volume,Tags=[{Key=Name,Value=cra_frontend_disk1}]"

aws ec2 describe-instances --filters 'Name=tag:Name,Values=cra_frontend' \
    --query 'Reservations[*].Instances[*].[PublicIpAddress]' \
    --output text > ip.txt