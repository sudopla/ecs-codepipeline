Configure ECS and CodePipeline with CloudFormation
--------------------

In this repository you can learn how to deploy a container application in ECS and automate the deployment of new releases using CodePipeline. The entire architecture is configure with CloudFormation. 

<img src="img/pipeline_1.png" width="80%">


You first should run the template [ecs_app.yaml](ecs_app.yaml) to configure the ECS cluster, task definition and services. A new VPC, subnets, ALB and security groups are also created with this template. 






