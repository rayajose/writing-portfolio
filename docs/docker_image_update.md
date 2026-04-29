# Deploy latest aws image:

## launch docker app

from C:\myProjects\partner-catalog-api

## build image
```bash
docker build -t partner-catalog-api .
```
## tag image

```bash
docker tag partner-catalog-api:latest 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```
## authenticate docker to ecr
```bash
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 792233688886.dkr.ecr.us-east-2.amazonaws.com
```
## push image
```bash
docker push 792233688886.dkr.ecr.us-east-2.amazonaws.com/partner-catalog-api:latest
```

Next step is to redeploy the ECS service with the new latest image