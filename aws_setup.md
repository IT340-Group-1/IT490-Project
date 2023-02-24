- In order to be able to deploy our code to something more durable than virtual machines running on our laptops, CRA will run on 1 mq.t3.micro Amazon MQ RabbitMQ broker (messaging server), and 3 Ubuntu Server 22.04 LTS t2.micro Amazon EC2 instances (database, frontend and backend servers).  
- The course requirement is that they need to be in 4 separate AWS accounts.  
- This is the simplest way to accomplish that. Other ways may be more secure, repeatable and sophisticated, and we may improve this if there is time.  
-  
- We need to install and configure AWS CLI  
	-  
	- Everyone needs to have an AWS account. Instructions to sign up for one can be found here: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-prereqs.html#getting-started-prereqs-signup  
	- In each AWS account, there should be an IAM user with AdministratorAccess permissions policy attached directly, and an access key. The console will recommend more secure alternatives, but they will make it harder to accomplish what we need.  
		- Go to IAM service in AWS Management Console  
		- Click on Access management > Users in the left menu.  
		- Click on Add users  
		- In Specify user details  
			- Enter User name (cra-messaging-admin, cra-database-admin, cra-frontend-admin and cra-backend-admin recommended)  
			- Optionally Provide user access to the AWS Management Console, so you don't need to use the root user. (Or you can create another user for console access.)  
			- Click on Next  
		- In Set permissions  
			- Select Attach policies directly  
			- Check AdministratorAccess  
			- Click on Next  
		- In Review and create  
			- Make sure AdministratorAccess is in Permissions summary, and everything else looks right  
			- Click on Create user  
		- Click on the newly created user  
			- Click on Security credentials  
			- Click on Create access key  
			- In Access key best practices & alternatives  
				- Select Other, and click on Next  
			- In Set description tag  
				- Click on Create access key  
			- In Retrieve access keys  
				- Click on Download .csv file (The data in this file is required to configure AWS CLI and access the AWS account programmatically. It should not be stored anywhere where it may be accessed by other people like in GitHub.)  
				- Click on Done  
	-  
	- Install AWS CLI  
		- Follow instructions for your operating system at https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html  
		- It may be best to do this in a Linux virtual machine, so that we can put scripts that use AWS CLI in our GitHub repository that will run on any of our development machines  
	-  
	- Configure AWS CLI  
	-  
	  ```
	  	  $ aws configure
	  	  AWS Access Key ID [None]: <copy from the access key .csv file downloaded earlier>
	  	  AWS Secret Access Key [None]: <copy from the access key .csv file downloaded earlier>
	  	  Default region name [None]: us-east-1
	  	  Default output format [None]: 
	  	  $ 
	  ```
	- This should create config and credentials files in ~/.aws folder  
	- To verify that AWS CLI is configured  
	-  
	  ```
	  	  $ aws ec2 describe-instances
	  	  {
	  	      "Reservations": []
	  	  }
	  	  $ 
	  ```
-  
- Import SSH key  
	- Download the emailed cra_ssh_key.zip to the folder containing `import_ssh_key.sh`  
	- In the terminal, change to that folder, and execute  
	  `source ./import_ssh_key.sh`  
-  
- Launch RabbitMQ broker and EC2 instances  
	- This could be done in the AWS Management Console, but we will try to script it using AWS CLI  
	- In the terminal, change to `messaging`,  `database`, `frontend` or `backend` folder, and execute  
	  `source ./aws_provision.sh`  
	- Commit and push the `ip.txt` file, so that the script that will start all services can connect to all of these servers  
	-  
- SSH into database, frontend or backend servers  
	- In the terminal, change to `database`, `frontend` or `backend` folder, and execute  
	  `source ./aws_ssh.sh`  
-  