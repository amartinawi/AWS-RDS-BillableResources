# AWS RDS Billable Resource Discovery Solution Design

## 1. Introduction
This document outlines the design for an AWS solution to identify and list all billable resources associated with a selected Amazon RDS DB instance or DB cluster. The solution will leverage the AWS SDK for Python (Boto3) to interact with AWS services and retrieve relevant resource information. The output will be presented in a clear, tabular format for easy readability and analysis.

## 2. Overall Architecture
The solution will be implemented as a Python script that takes an RDS DB instance identifier or DB cluster identifier as input. It will then use Boto3 to query various AWS services to gather information about associated resources. The collected data will be structured and then presented in a table.

## 3. Resource Discovery Workflow

### 3.1. Input: RDS DB Instance/Cluster Identifier
The script will require either an RDS DB instance identifier (e.g., `my-db-instance`) or an RDS DB cluster identifier (e.g., `my-db-cluster`) as a command-line argument or user input.

### 3.2. Initialize Boto3 RDS Client
We will initialize a Boto3 RDS client. The client provides low-level access to RDS API actions.

```python
import boto3

rds_client = boto3.client("rds")
```

### 3.3. Retrieve RDS DB Instance/Cluster Details
Based on the input identifier, we will retrieve detailed information about the DB instance or DB cluster, which will be crucial for identifying associated resources.

- For DB Instances: `rds_client.describe_db_instances`
- For DB Clusters: `rds_client.describe_db_clusters`

### 3.4. Discover Associated Resources
For each billable resource type, we will implement a dedicated function to discover and collect relevant information. The following resource types will be covered:

#### 3.4.1. DB Instances
These are the primary compute resources for relational databases in RDS. We will retrieve details such as instance class, engine, status, storage, and associated security groups.

#### 3.4.2. DB Clusters
For Aurora and Multi-AZ DB clusters, we will retrieve cluster-specific details such as engine, status, endpoint, and associated DB instances.

#### 3.4.3. DB Snapshots
Snapshots are point-in-time backups of DB instances or DB clusters. We will identify snapshots associated with the given instance or cluster.

#### 3.4.4. DB Cluster Snapshots
Similar to DB Snapshots, but specifically for Aurora DB clusters.

#### 3.4.5. DB Security Groups
These control access to DB instances in EC2-Classic. While less common now, they are still billable resources.

#### 3.4.6. VPC Security Groups
For DB instances and clusters in a VPC, these security groups control network access. We will identify the VPC security groups associated with the DB instance or cluster.

#### 3.4.7. DB Subnet Groups
These define a collection of subnets that you can designate for your DB instances in a VPC. We will retrieve details about the subnet group associated with the DB instance or cluster.

#### 3.4.8. Option Groups
Option groups enable and configure features for your DB instances. We will retrieve details about the option group associated with the DB instance.

#### 3.4.9. Parameter Groups
DB parameter groups act as a container for engine configuration values that are applied to one or more DB instances. We will retrieve details about the parameter group associated with the DB instance.

## 4. Data Structure for Output
The collected information for each resource type will be stored in a structured format, likely a list of dictionaries or a Pandas DataFrame, to facilitate easy table generation.

## 5. Output Formatting
The final output will be a well-formatted table, displaying the discovered resources and their relevant attributes. We will use a library like `tabulate` or `pandas` to achieve this.

## 6. Error Handling
The solution will include error handling for scenarios such as invalid identifiers, API call failures, and missing permissions.

## 7. Future Enhancements (Out of Scope for initial delivery)
- Support for multiple RDS instance/cluster inputs.
- Integration with AWS Cost Explorer to retrieve billing information directly.
- Exporting output to different formats (CSV, JSON).


