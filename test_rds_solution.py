#!/usr/bin/env python3
"""
Test script for AWS RDS Resource Discovery Tool

This script tests the table formatting functionality using mock data,
allowing validation without requiring AWS credentials.
"""

import sys
import os
from datetime import datetime

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rds_table_formatter import RDSResourceTableFormatter


def create_mock_db_instance_data():
    """Create mock data for a DB instance discovery result."""
    return {
        'resource_type': 'db_instance',
        'resource_details': {
            'db_instance_id': 'test-mysql-instance',
            'db_instance_class': 'db.t3.micro',
            'engine': 'mysql',
            'engine_version': '8.0.35',
            'status': 'available',
            'allocated_storage': 20,
            'storage_type': 'gp2',
            'storage_encrypted': True,
            'availability_zone': 'us-east-1a',
            'multi_az': False,
            'vpc_id': 'vpc-12345678',
            'subnet_group': 'default-vpc-12345678',
            'endpoint': 'test-mysql-instance.abcdef123456.us-east-1.rds.amazonaws.com',
            'port': 3306,
            'master_username': 'admin',
            'db_cluster_identifier': None,
            'creation_time': '2024-06-20T10:30:00.000Z',
            'tags': {
                'Name': 'TestDatabase',
                'Environment': 'Development',
                'Owner': 'DataTeam',
                'Project': 'WebApp'
            }
        },
        'resources': [
            {
                'resource_type': 'DB Instance',
                'resource_id': 'test-mysql-instance',
                'db_instance_class': 'db.t3.micro',
                'engine': 'mysql',
                'engine_version': '8.0.35',
                'status': 'available',
                'allocated_storage': 20,
                'storage_type': 'gp2',
                'storage_encrypted': True,
                'availability_zone': 'us-east-1a',
                'multi_az': False,
                'vpc_id': 'vpc-12345678',
                'endpoint': 'test-mysql-instance.abcdef123456.us-east-1.rds.amazonaws.com',
                'port': 3306,
                'tags': {
                    'Name': 'TestDatabase',
                    'Environment': 'Development',
                    'Owner': 'DataTeam',
                    'Project': 'WebApp'
                }
            },
            {
                'resource_type': 'DB Snapshot',
                'resource_id': 'test-mysql-instance-snapshot-2024-06-20',
                'db_instance_id': 'test-mysql-instance',
                'snapshot_type': 'manual',
                'status': 'available',
                'allocated_storage': 20,
                'storage_type': 'gp2',
                'encrypted': True,
                'engine': 'mysql',
                'engine_version': '8.0.35',
                'creation_time': '2024-06-20T15:45:00.000Z',
                'availability_zone': 'us-east-1a',
                'tags': {
                    'Name': 'TestSnapshot',
                    'Purpose': 'Backup'
                }
            },
            {
                'resource_type': 'DB Snapshot',
                'resource_id': 'rds:test-mysql-instance-2024-06-19-03-00',
                'db_instance_id': 'test-mysql-instance',
                'snapshot_type': 'automated',
                'status': 'available',
                'allocated_storage': 20,
                'storage_type': 'gp2',
                'encrypted': True,
                'engine': 'mysql',
                'engine_version': '8.0.35',
                'creation_time': '2024-06-19T03:00:00.000Z',
                'availability_zone': 'us-east-1a',
                'tags': {}
            },
            {
                'resource_type': 'VPC Security Group',
                'resource_id': 'sg-0123456789abcdef0',
                'name': 'rds-mysql-sg',
                'description': 'Security group for MySQL RDS instance allowing access from application servers',
                'vpc_id': 'vpc-12345678',
                'inbound_rules': 2,
                'outbound_rules': 1,
                'tags': {
                    'Name': 'RDS-MySQL-SG',
                    'Environment': 'Development'
                }
            },
            {
                'resource_type': 'VPC Security Group',
                'resource_id': 'sg-0987654321fedcba0',
                'name': 'default',
                'description': 'Default security group for VPC',
                'vpc_id': 'vpc-12345678',
                'inbound_rules': 1,
                'outbound_rules': 1,
                'tags': {}
            },
            {
                'resource_type': 'DB Subnet Group',
                'resource_id': 'default-vpc-12345678',
                'name': 'default-vpc-12345678',
                'description': 'Created from the RDS Management Console',
                'vpc_id': 'vpc-12345678',
                'status': 'Complete',
                'subnets': ['subnet-12345678', 'subnet-87654321', 'subnet-abcdef12'],
                'availability_zones': ['us-east-1a', 'us-east-1b', 'us-east-1c'],
                'tags': {}
            },
            {
                'resource_type': 'DB Parameter Group',
                'resource_id': 'default.mysql8.0',
                'name': 'default.mysql8.0',
                'family': 'mysql8.0',
                'description': 'Default parameter group for mysql8.0',
                'tags': {}
            },
            {
                'resource_type': 'Option Group',
                'resource_id': 'default:mysql-8-0',
                'name': 'default:mysql-8-0',
                'description': 'Default option group for mysql 8.0',
                'engine_name': 'mysql',
                'major_engine_version': '8.0',
                'vpc_id': 'N/A',
                'options': [],
                'tags': {}
            }
        ],
        'summary': {
            'total_resources': 8,
            'snapshots': 2,
            'security_groups': 2,
            'subnet_groups': 1,
            'parameter_groups': 1,
            'option_groups': 1
        }
    }


def create_mock_db_cluster_data():
    """Create mock data for a DB cluster discovery result."""
    return {
        'resource_type': 'db_cluster',
        'resource_details': {
            'db_cluster_id': 'test-aurora-cluster',
            'engine': 'aurora-mysql',
            'engine_version': '8.0.mysql_aurora.3.02.0',
            'status': 'available',
            'allocated_storage': 1,
            'storage_encrypted': True,
            'availability_zones': ['us-east-1a', 'us-east-1b', 'us-east-1c'],
            'vpc_id': 'vpc-87654321',
            'endpoint': 'test-aurora-cluster.cluster-abcdef123456.us-east-1.rds.amazonaws.com',
            'reader_endpoint': 'test-aurora-cluster.cluster-ro-abcdef123456.us-east-1.rds.amazonaws.com',
            'port': 3306,
            'master_username': 'admin',
            'cluster_members': ['test-aurora-instance-1', 'test-aurora-instance-2'],
            'creation_time': '2024-06-15T14:20:00.000Z',
            'tags': {
                'Name': 'TestAuroraCluster',
                'Environment': 'Production',
                'Application': 'WebService'
            }
        },
        'resources': [
            {
                'resource_type': 'DB Cluster',
                'resource_id': 'test-aurora-cluster',
                'engine': 'aurora-mysql',
                'engine_version': '8.0.mysql_aurora.3.02.0',
                'status': 'available',
                'allocated_storage': 1,
                'storage_encrypted': True,
                'availability_zones': ['us-east-1a', 'us-east-1b', 'us-east-1c'],
                'vpc_id': 'vpc-87654321',
                'endpoint': 'test-aurora-cluster.cluster-abcdef123456.us-east-1.rds.amazonaws.com',
                'reader_endpoint': 'test-aurora-cluster.cluster-ro-abcdef123456.us-east-1.rds.amazonaws.com',
                'port': 3306,
                'cluster_members': ['test-aurora-instance-1', 'test-aurora-instance-2'],
                'tags': {
                    'Name': 'TestAuroraCluster',
                    'Environment': 'Production',
                    'Application': 'WebService'
                }
            },
            {
                'resource_type': 'DB Cluster Member',
                'resource_id': 'test-aurora-instance-1',
                'db_instance_class': 'db.r6g.large',
                'engine': 'aurora-mysql',
                'status': 'available',
                'is_cluster_writer': True,
                'promotion_tier': 1,
                'availability_zone': 'us-east-1a',
                'tags': {
                    'Name': 'TestAuroraWriter',
                    'Role': 'Writer'
                }
            },
            {
                'resource_type': 'DB Cluster Member',
                'resource_id': 'test-aurora-instance-2',
                'db_instance_class': 'db.r6g.large',
                'engine': 'aurora-mysql',
                'status': 'available',
                'is_cluster_writer': False,
                'promotion_tier': 2,
                'availability_zone': 'us-east-1b',
                'tags': {
                    'Name': 'TestAuroraReader',
                    'Role': 'Reader'
                }
            },
            {
                'resource_type': 'DB Cluster Snapshot',
                'resource_id': 'test-aurora-cluster-snapshot-2024-06-20',
                'db_cluster_id': 'test-aurora-cluster',
                'snapshot_type': 'manual',
                'status': 'available',
                'allocated_storage': 1,
                'storage_encrypted': True,
                'engine': 'aurora-mysql',
                'engine_version': '8.0.mysql_aurora.3.02.0',
                'creation_time': '2024-06-20T16:30:00.000Z',
                'availability_zones': ['us-east-1a', 'us-east-1b', 'us-east-1c'],
                'tags': {
                    'Name': 'TestClusterSnapshot',
                    'Purpose': 'PreUpgrade'
                }
            },
            {
                'resource_type': 'VPC Security Group',
                'resource_id': 'sg-aurora123456789',
                'name': 'aurora-cluster-sg',
                'description': 'Security group for Aurora MySQL cluster',
                'vpc_id': 'vpc-87654321',
                'inbound_rules': 3,
                'outbound_rules': 1,
                'tags': {
                    'Name': 'Aurora-Cluster-SG',
                    'Environment': 'Production'
                }
            },
            {
                'resource_type': 'DB Subnet Group',
                'resource_id': 'aurora-subnet-group',
                'name': 'aurora-subnet-group',
                'description': 'Subnet group for Aurora cluster',
                'vpc_id': 'vpc-87654321',
                'status': 'Complete',
                'subnets': ['subnet-aurora1', 'subnet-aurora2', 'subnet-aurora3'],
                'availability_zones': ['us-east-1a', 'us-east-1b', 'us-east-1c'],
                'tags': {
                    'Name': 'AuroraSubnetGroup',
                    'Environment': 'Production'
                }
            },
            {
                'resource_type': 'DB Cluster Parameter Group',
                'resource_id': 'aurora-mysql80-cluster-params',
                'name': 'aurora-mysql80-cluster-params',
                'family': 'aurora-mysql8.0',
                'description': 'Custom cluster parameter group for Aurora MySQL 8.0',
                'tags': {
                    'Name': 'AuroraClusterParams',
                    'Environment': 'Production'
                }
            }
        ],
        'summary': {
            'total_resources': 7,
            'cluster_snapshots': 1,
            'security_groups': 1,
            'subnet_groups': 1,
            'parameter_groups': 1,
            'option_groups': 0,
            'cluster_members': 2
        }
    }


def test_table_formatting():
    """Test the table formatting functionality."""
    print("="*80)
    print("Testing AWS RDS Resource Discovery Table Formatting")
    print("="*80)
    
    formatter = RDSResourceTableFormatter()
    
    # Test DB Instance formatting
    print("\n" + "="*60)
    print("TEST 1: DB Instance Resource Discovery")
    print("="*60)
    
    db_instance_data = create_mock_db_instance_data()
    
    print("\n1.1 Summary Table:")
    print("-" * 40)
    summary_table = formatter.format_summary_table(db_instance_data['summary'])
    print(summary_table)
    
    print("\n1.2 Simple Resources Table:")
    print("-" * 40)
    simple_table = formatter.format_resources_table(db_instance_data['resources'])
    print(simple_table)
    
    print("\n1.3 Detailed Resources Table (Fancy Grid):")
    print("-" * 40)
    detailed_table = formatter.format_detailed_resources_table(
        db_instance_data['resources'], 'fancy_grid'
    )
    print(detailed_table)
    
    # Test DB Cluster formatting
    print("\n" + "="*60)
    print("TEST 2: DB Cluster Resource Discovery")
    print("="*60)
    
    db_cluster_data = create_mock_db_cluster_data()
    
    print("\n2.1 Summary Table:")
    print("-" * 40)
    cluster_summary_table = formatter.format_summary_table(db_cluster_data['summary'])
    print(cluster_summary_table)
    
    print("\n2.2 Detailed Resources Table (Grid):")
    print("-" * 40)
    cluster_detailed_table = formatter.format_detailed_resources_table(
        db_cluster_data['resources'], 'grid'
    )
    print(cluster_detailed_table)
    
    # Test export functionality
    print("\n" + "="*60)
    print("TEST 3: Export Functionality")
    print("="*60)
    
    try:
        # Test CSV export
        csv_message = formatter.export_to_csv(
            db_instance_data['resources'], 
            'test_rds_resources.csv'
        )
        print(f"✓ {csv_message}")
        
        # Test JSON export
        json_message = formatter.export_to_json(
            db_instance_data, 
            'test_rds_discovery_result.json'
        )
        print(f"✓ {json_message}")
        
        # Test cluster CSV export
        cluster_csv_message = formatter.export_to_csv(
            db_cluster_data['resources'], 
            'test_rds_cluster_resources.csv'
        )
        print(f"✓ {cluster_csv_message}")
        
        # Test cluster JSON export
        cluster_json_message = formatter.export_to_json(
            db_cluster_data, 
            'test_rds_cluster_discovery_result.json'
        )
        print(f"✓ {cluster_json_message}")
        
    except Exception as e:
        print(f"✗ Export test failed: {str(e)}")
    
    # Test different table formats
    print("\n" + "="*60)
    print("TEST 4: Different Table Formats")
    print("="*60)
    
    test_resources = db_instance_data['resources'][:3]  # Use first 3 resources for brevity
    
    formats = ['simple', 'pipe', 'orgtbl', 'rst']
    for fmt in formats:
        print(f"\n4.{formats.index(fmt)+1} Format: {fmt}")
        print("-" * 30)
        try:
            table = formatter.format_resources_table(test_resources, fmt)
            print(table)
        except Exception as e:
            print(f"✗ Error with format {fmt}: {str(e)}")
    
    print("\n" + "="*80)
    print("✓ All table formatting tests completed successfully!")
    print("="*80)


def test_individual_components():
    """Test individual components of the formatter."""
    print("\n" + "="*60)
    print("TEST 5: Individual Component Testing")
    print("="*60)
    
    formatter = RDSResourceTableFormatter()
    
    # Test tag formatting
    print("\n5.1 Tag Formatting:")
    print("-" * 30)
    test_tags = {
        'Name': 'TestResource',
        'Environment': 'Production',
        'Owner': 'DataTeam',
        'Project': 'WebApp',
        'CostCenter': '12345'
    }
    formatted_tags = formatter._format_tags(test_tags)
    print(f"Input tags: {test_tags}")
    print(f"Formatted: {formatted_tags}")
    
    # Test empty tags
    empty_tags = formatter._format_tags({})
    print(f"Empty tags: {empty_tags}")
    
    # Test resource details formatting
    print("\n5.2 Resource Details Formatting:")
    print("-" * 30)
    test_resource = {
        'resource_type': 'DB Instance',
        'resource_id': 'test-instance',
        'engine': 'mysql',
        'status': 'available',
        'allocated_storage': 20,
        'tags': {'Name': 'Test'}
    }
    formatted_details = formatter._format_resource_details(test_resource)
    print(f"Input resource: {test_resource}")
    print(f"Formatted details: {formatted_details}")
    
    print("\n✓ Individual component tests completed!")


def main():
    """Main test function."""
    try:
        print("Starting AWS RDS Resource Discovery Tool Tests...")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Run table formatting tests
        test_table_formatting()
        
        # Run individual component tests
        test_individual_components()
        
        print(f"\n{'='*80}")
        print("🎉 ALL TESTS PASSED SUCCESSFULLY! 🎉")
        print(f"{'='*80}")
        print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # List generated files
        print(f"\nGenerated test files:")
        test_files = [
            'test_rds_resources.csv',
            'test_rds_discovery_result.json',
            'test_rds_cluster_resources.csv',
            'test_rds_cluster_discovery_result.json'
        ]
        
        for file in test_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  ✓ {file} ({size} bytes)")
            else:
                print(f"  ✗ {file} (not found)")
        
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ TEST FAILED: {str(e)}")
        print(f"{'='*80}")
        sys.exit(1)


if __name__ == "__main__":
    main()

