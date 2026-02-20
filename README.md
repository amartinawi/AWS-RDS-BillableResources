# AWS RDS Billable Resource Discovery Tool

Discover all billable resources associated with AWS RDS DB instances and Aurora clusters.

## Quick Start

### Prerequisites
- Python 3.7+
- AWS credentials configured
- Required permissions: RDS and EC2 read access

### Installation
```bash
pip3 install boto3 tabulate pandas
```

### Basic Usage
```bash
# Discover resources for an RDS instance
python3 aws_rds_resource_discovery.py my-db-instance

# For an Aurora cluster
python3 aws_rds_resource_discovery.py my-aurora-cluster --cluster

# With specific region
python3 aws_rds_resource_discovery.py my-db-instance --region us-west-2

# Export to CSV and JSON
python3 aws_rds_resource_discovery.py my-db-instance --export-csv resources.csv --export-json results.json
```

## What It Discovers

| Resource Type | Description |
|---------------|-------------|
| DB Instance/Cluster | Primary database with configuration |
| DB Snapshots | Manual and automated backups |
| Cluster Snapshots | Aurora cluster backups |
| Security Groups | VPC and EC2-Classic security groups |
| Subnet Groups | Network placement and AZs |
| Parameter Groups | Engine configuration |
| Option Groups | Database features/extensions |
| Cluster Members | Aurora instance members |

## Sample Output

```
================================================================================
AWS RDS Resource Discovery Results
================================================================================
DB Instance ID: my-mysql-instance
Instance Class: db.t3.micro
Engine: mysql 8.0.35
Status: available
Storage: 20 GB (gp2)
Encrypted: True
Multi-AZ: False

Region: us-east-1
Total Resources Found: 8

Resource Summary:
+--------------------+-------+
| Resource Type      | Count |
+====================+=======+
| Snapshots          |     2 |
| Security Groups    |     2 |
| Subnet Groups      |     1 |
| Parameter Groups   |     1 |
| Option Groups      |     1 |
| TOTAL              |     8 |
+--------------------+-------+
```

## Command Options

| Option | Description |
|--------|-------------|
| `identifier` | RDS instance or cluster identifier (required) |
| `--cluster` | Treat as DB cluster instead of instance |
| `--region REGION` | AWS region |
| `--profile PROFILE` | AWS profile |
| `--format FORMAT` | Table format (grid, fancy_grid, simple, etc.) |
| `--detailed` | Show detailed tables by resource type |
| `--summary-only` | Show only resource summary |
| `--export-csv FILE` | Export to CSV |
| `--export-json FILE` | Export to JSON |

## Required IAM Permissions

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "rds:DescribeDBSnapshots",
        "rds:DescribeDBClusterSnapshots",
        "rds:DescribeDBSecurityGroups",
        "rds:DescribeDBSubnetGroups",
        "rds:DescribeDBParameterGroups",
        "rds:DescribeDBClusterParameterGroups",
        "rds:DescribeOptionGroups",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs"
      ],
      "Resource": "*"
    }
  ]
}
```

## Use Cases

- **Cost Analysis** - Understand all billable RDS components
- **Security Audits** - Review security groups and network configs
- **Compliance Reporting** - Document database infrastructure
- **Disaster Recovery** - Identify snapshots and backup resources
- **Migration Planning** - Inventory all dependencies before migration

## Testing

```bash
python3 test_rds_solution.py
```

## Files

| File | Description |
|------|-------------|
| `aws_rds_resource_discovery.py` | Main CLI tool |
| `rds_resource_discovery.py` | Discovery engine |
| `rds_table_formatter.py` | Table formatting |
| `test_rds_solution.py` | Test suite |
| `AWS_RDS_Resource_Discovery_Documentation.pdf` | Full documentation |

## License

MIT License - see [LICENSE](LICENSE)
