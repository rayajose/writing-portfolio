# deploy latest aws image:

launch docker app

from C:\myProjects\partner-catalog-api

run: docker build -t partner-catalog-api .

1. get ecr repo uri
In AWS:

Go to Amazon ECR
Click your repo (likely: partner-catalog-api)
Copy the URI: 

792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest

2. tag image
run: 
docker tag partner-catalog-api:latest 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest

3. authenticate docker to ecr
run:
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 792233688886.dkr.ecr.us-east-2.amazonaws.com

4. push image
run: docker push 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest

Next step is to redeploy the ECS service with the new latest image