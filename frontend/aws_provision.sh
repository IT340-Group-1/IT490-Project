aws ec2 run-instances --image-id ami-0557a15b87f6559cf --count 1 --instance-type t2.micro \
    --key-name cra_ssh_key --security-groups cra_security_group \
    --tag-specifications \
        "ResourceType=instance,Tags=[{Key=Name,Value=cra_frontend}]" \
        "ResourceType=volume,Tags=[{Key=Name,Value=cra_frontend_disk1}]"

aws ec2 describe-instances --filters 'Name=tag:Name,Values=cra_frontend' 'Name=instance-state-name, Values=running' \
    --query 'Reservations[*].Instances[*].[PublicIpAddress]' \
    --output text > ip.txt
