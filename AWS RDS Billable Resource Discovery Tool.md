# AWS RDS Billable Resource Discovery Tool

A comprehensive Python solution to discover and list all billable resources associated with AWS RDS DB instances and clusters.

## Quick Start

### Prerequisites
- Python 3.7+
- AWS credentials configured
- Required permissions: RDS and EC2 read access

### Installation
```bash
# Install dependencies
pip3 install boto3 tabulate pandas

# Make scripts executable
chmod +x aws_rds_resource_discovery.py
```

### Basic Usage
```bash
# Discover resources for an RDS DB instance
python3 aws_rds_resource_discovery.py my-db-instance

# Discover resources for an RDS DB cluster
python3 aws_rds_resource_discovery.py my-aurora-cluster --cluster

# With specific region
python3 aws_rds_resource_discovery.py my-db-instance --region us-west-2

# Detailed output with fancy formatting
python3 aws_rds_resource_discovery.py my-db-instance --detailed --format fancy_grid

# Export to CSV and JSON
python3 aws_rds_resource_discovery.py my-db-instance --export-csv resources.csv --export-json results.json
```

## What It Discovers

The tool identifies all billable resources associated with an RDS instance or cluster:

- **RDS DB Instance/Cluster** - The primary database resource with configuration details
- **DB Snapshots** - Manual and automated snapshots with storage information
- **DB Cluster Snapshots** - Aurora cluster snapshots and backups
- **VPC Security Groups** - Network access controls and firewall rules
- **DB Security Groups** - Legacy EC2-Classic security groups
- **DB Subnet Groups** - Network placement and availability zone configuration
- **DB Parameter Groups** - Database engine configuration parameters
- **DB Cluster Parameter Groups** - Aurora cluster-level parameters
- **Option Groups** - Database engine features and extensions
- **Cluster Members** - Individual instances within Aurora clusters

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
Availability Zone: us-east-1a
VPC ID: vpc-12345678
Endpoint: my-mysql-instance.abcdef123456.us-east-1.rds.amazonaws.com:3306

Region: us-east-1
Total Resources Found: 8

================================================================================
Resource Summary:
================================================================================
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

- `identifier` - RDS DB instance or cluster identifier (required)
- `--cluster` - Treat identifier as DB cluster instead of DB instance
- `--region REGION` - Specify AWS region
- `--profile PROFILE` - Use specific AWS profile
- `--format FORMAT` - Table format (grid, fancy_grid, simple, pipe, etc.)
- `--detailed` - Show detailed tables grouped by resource type
- `--summary-only` - Show only the resource summary
- `--export-csv FILE` - Export to CSV file
- `--export-json FILE` - Export to JSON file
- `--help` - Show all options and examples

## Required AWS Permissions

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
                "rds:ListTagsForResource",
                "ec2:DescribeSecurityGroups"
            ],
            "Resource": "*"
        }
    ]
}
```

## Files Included

- `aws_rds_resource_discovery.py` - Main CLI tool
- `rds_resource_discovery.py` - Resource discovery engine
- `rds_table_formatter.py` - Table formatting module
- `test_rds_solution.py` - Test with mock data
- `documentation.md` - Comprehensive documentation
- `solution_design.md` - Architecture and design details

## Testing

Test the solution without AWS credentials:
```bash
python3 test_rds_solution.py
```

## Troubleshooting

**Credentials Error:**
```bash
aws configure  # Configure AWS CLI
```

**Permission Error:**
Ensure your IAM user/role has the required RDS and EC2 read permissions listed above.

**Instance/Cluster Not Found:**
- Verify the identifier format and spelling
- Check you're using the correct region with `--region`
- For clusters, use the `--cluster` flag

**Import Error:**
```bash
pip3 install boto3 tabulate pandas
```

## Use Cases

- **Cost Analysis** - Understand all billable resources for RDS deployments
- **Security Audits** - Review associated security groups and network configs
- **Compliance Reporting** - Document infrastructure components and relationships
- **Resource Cleanup** - Identify orphaned or unused resources
- **Disaster Recovery** - Document dependencies for backup planning
- **Migration Planning** - Catalog existing configurations for migration projects

## Examples

### Basic Discovery
```bash
# Single RDS instance
python3 aws_rds_resource_discovery.py prod-mysql-01

# Aurora cluster
python3 aws_rds_resource_discovery.py prod-aurora-cluster --cluster
```

### Advanced Usage
```bash
# Detailed view with custom formatting
python3 aws_rds_resource_discovery.py prod-mysql-01 \
  --detailed \
  --format fancy_grid \
  --region us-west-2 \
  --profile production

# Export for analysis
python3 aws_rds_resource_discovery.py prod-mysql-01 \
  --export-csv mysql_resources.csv \
  --export-json mysql_discovery.json

# Summary only for quick overview
python3 aws_rds_resource_discovery.py prod-mysql-01 --summary-only
```

### Batch Processing
```bash
# Process multiple instances
for instance in $(aws rds describe-db-instances --query 'DBInstances[].DBInstanceIdentifier' --output text); do
  python3 aws_rds_resource_discovery.py $instance --export-csv "${instance}_resources.csv"
done

# Process all clusters
for cluster in $(aws rds describe-db-clusters --query 'DBClusters[].DBClusterIdentifier' --output text); do
  python3 aws_rds_resource_discovery.py $cluster --cluster --export-json "${cluster}_discovery.json"
done
```

## Architecture

The solution consists of three main components:

1. **Resource Discovery Engine** (`rds_resource_discovery.py`)
   - Discovers all RDS-related resources using Boto3
   - Handles both DB instances and DB clusters
   - Implements comprehensive error handling and retry logic

2. **Table Formatter** (`rds_table_formatter.py`)
   - Formats discovered resources into readable tables
   - Supports multiple output formats and export options
   - Provides both summary and detailed views

3. **CLI Interface** (`aws_rds_resource_discovery.py`)
   - Command-line interface with comprehensive options
   - Integrates discovery and formatting components
   - Provides user-friendly output and error handling

## Contributing

The solution is designed with extensibility in mind. To add support for additional resource types:

1. Add discovery methods to `RDSResourceDiscovery` class
2. Add formatting methods to `RDSResourceTableFormatter` class
3. Update the CLI interface to handle new options
4. Add test cases to validate new functionality

## Support

For detailed documentation, see `documentation.md`.

For technical details and architecture information, see `solution_design.md`.

To test functionality without AWS credentials, run `test_rds_solution.py`.

## Version History

- **v1.0.0** - Initial release with comprehensive RDS resource discovery
  - Support for DB instances and clusters
  - Multiple output formats and export options
  - Comprehensive documentation and testing

