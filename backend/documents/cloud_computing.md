# Cloud Computing

## What is Cloud Computing?

Cloud computing is the on-demand delivery of IT resources (computing power, storage, databases, networking, software, analytics, and intelligence) over the internet with pay-as-you-go pricing. Instead of buying and maintaining physical data centers, you can access technology services on an as-needed basis from a cloud provider.

## Service Models

### Infrastructure as a Service (IaaS)
Provides virtualized computing resources over the internet:
- Raw infrastructure: VMs, networks, storage
- You manage: OS, runtime, applications, data
- Providers manage: Physical hardware, networking
- **Examples**: AWS EC2, Google Compute Engine, Azure VMs

### Platform as a Service (PaaS)
Provides a platform for developing and deploying applications:
- You manage: Applications and data
- Provider manages: Infrastructure, OS, runtime
- **Examples**: AWS Elastic Beanstalk, Google App Engine, Heroku

### Software as a Service (SaaS)
Provides complete software applications over the internet:
- Provider manages everything
- You just use the software
- **Examples**: Gmail, Salesforce, Microsoft 365

### Function as a Service (FaaS) / Serverless
Run code without managing servers:
- Event-driven execution
- Auto-scaling
- Pay only for execution time
- **Examples**: AWS Lambda, Google Cloud Functions, Azure Functions

## Major Cloud Providers

### Amazon Web Services (AWS)
- Largest cloud provider (~33% market share)
- 200+ services
- Key services: EC2, S3, RDS, Lambda, EKS, SageMaker

### Microsoft Azure
- Second largest (~22% market share)
- Deep integration with Microsoft products
- Key services: Azure VMs, Blob Storage, Azure AI, AKS

### Google Cloud Platform (GCP)
- Third largest (~10% market share)
- Strong in AI/ML and data analytics
- Key services: Compute Engine, Cloud Storage, BigQuery, GKE, Vertex AI

### Others
- **Oracle Cloud**: Strong in database services
- **IBM Cloud**: Enterprise focus
- **Alibaba Cloud**: Dominant in Asia

## Key Cloud Services

### Compute
- Virtual Machines / EC2 instances
- Container services (ECS, EKS, GKE, AKS)
- Serverless (Lambda, Cloud Functions)

### Storage
- **Object Storage**: S3, Google Cloud Storage, Azure Blob — for files, media
- **Block Storage**: EBS, Persistent Disk — for databases, file systems
- **File Storage**: EFS, Filestore — shared file systems

### Database
- **Relational**: Amazon RDS, Cloud SQL, Azure SQL
- **NoSQL**: DynamoDB, Firestore, Cosmos DB
- **Cache**: ElastiCache (Redis/Memcached)
- **Data Warehouse**: Redshift, BigQuery, Synapse

### Networking
- Virtual Private Cloud (VPC)
- Load Balancers
- CDN (CloudFront, Cloud CDN)
- DNS (Route 53, Cloud DNS)

### AI/ML
- Managed ML platforms: SageMaker, Vertex AI, Azure ML
- Pre-built AI APIs: Vision, Speech, Translation, NLP

## Cloud Deployment Models

### Public Cloud
- Infrastructure shared among multiple organizations
- Pay-as-you-go model
- Examples: AWS, Azure, GCP

### Private Cloud
- Dedicated infrastructure for one organization
- More control and security
- Higher cost

### Hybrid Cloud
- Combination of public and private
- Workloads can move between environments
- Best of both worlds

### Multi-Cloud
- Uses multiple cloud providers
- Avoids vendor lock-in
- More complexity

## Key Benefits

- **Scalability**: Scale up or down based on demand
- **Cost Efficiency**: Pay only for what you use
- **Global Reach**: Deploy worldwide with low latency
- **Reliability**: Built-in redundancy and high availability
- **Security**: Enterprise-grade security features
- **Innovation**: Access to cutting-edge services

## Cloud-Native Concepts

### Microservices
Break applications into small, independently deployable services.

### Kubernetes (K8s)
Container orchestration platform:
- Auto-scaling
- Self-healing
- Rolling deployments
- Load balancing

### CI/CD Pipelines
Automate building, testing, and deploying code.

### Infrastructure as Code (IaC)
Manage infrastructure using code:
- **Terraform**: Multi-cloud IaC tool
- **AWS CloudFormation**: AWS-specific
- **Pulumi**: Code-first approach
