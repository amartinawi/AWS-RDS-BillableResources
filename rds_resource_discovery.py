#!/usr/bin/env python3
"""
AWS RDS Billable Resource Discovery Tool

This script discovers and lists all billable resources associated with a selected RDS DB instance or DB cluster.
It identifies snapshots, security groups, subnet groups, parameter groups, option groups, and other related resources.
"""

import boto3
import json
import sys
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError


class RDSResourceDiscovery:
    """Class to discover and collect RDS-related billable resources."""
    
    def __init__(self, region_name: str = None, profile_name: str = None):
        """
        Initialize the RDS Resource Discovery tool.
        
        Args:
            region_name: AWS region name (optional, uses default if not provided)
            profile_name: AWS profile name (optional, uses default if not provided)
        """
        try:
            session = boto3.Session(profile_name=profile_name)
            self.rds_client = session.client('rds', region_name=region_name)
            self.ec2_client = session.client('ec2', region_name=region_name)
            self.region = region_name or session.region_name
        except NoCredentialsError:
            print("Error: AWS credentials not found. Please configure your credentials.")
            sys.exit(1)
        except Exception as e:
            print(f"Error initializing AWS session: {str(e)}")
            sys.exit(1)
    
    def get_db_instance_details(self, db_instance_id: str) -> Dict[str, Any]:
        """
        Get basic details about the RDS DB instance.
        
        Args:
            db_instance_id: The RDS DB instance identifier
            
        Returns:
            Dictionary containing DB instance details
        """
        try:
            response = self.rds_client.describe_db_instances(
                DBInstanceIdentifier=db_instance_id
            )
            
            if not response['DBInstances']:
                raise ValueError(f"DB Instance {db_instance_id} not found")
            
            db_instance = response['DBInstances'][0]
            
            return {
                'db_instance_id': db_instance['DBInstanceIdentifier'],
                'db_instance_class': db_instance['DBInstanceClass'],
                'engine': db_instance['Engine'],
                'engine_version': db_instance['EngineVersion'],
                'status': db_instance['DBInstanceStatus'],
                'allocated_storage': db_instance.get('AllocatedStorage', 0),
                'storage_type': db_instance.get('StorageType', 'N/A'),
                'storage_encrypted': db_instance.get('StorageEncrypted', False),
                'availability_zone': db_instance.get('AvailabilityZone', 'N/A'),
                'multi_az': db_instance.get('MultiAZ', False),
                'vpc_id': db_instance.get('DBSubnetGroup', {}).get('VpcId', 'N/A'),
                'subnet_group': db_instance.get('DBSubnetGroup', {}).get('DBSubnetGroupName', 'N/A'),
                'endpoint': db_instance.get('Endpoint', {}).get('Address', 'N/A'),
                'port': db_instance.get('Endpoint', {}).get('Port', 'N/A'),
                'master_username': db_instance.get('MasterUsername', 'N/A'),
                'db_cluster_identifier': db_instance.get('DBClusterIdentifier', None),
                'creation_time': db_instance.get('InstanceCreateTime', '').isoformat() if db_instance.get('InstanceCreateTime') else 'N/A',
                'tags': self._get_resource_tags(db_instance.get('DBInstanceArn', ''))
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'DBInstanceNotFoundFault':
                raise ValueError(f"DB Instance {db_instance_id} not found")
            else:
                raise e
    
    def get_db_cluster_details(self, db_cluster_id: str) -> Dict[str, Any]:
        """
        Get basic details about the RDS DB cluster.
        
        Args:
            db_cluster_id: The RDS DB cluster identifier
            
        Returns:
            Dictionary containing DB cluster details
        """
        try:
            response = self.rds_client.describe_db_clusters(
                DBClusterIdentifier=db_cluster_id
            )
            
            if not response['DBClusters']:
                raise ValueError(f"DB Cluster {db_cluster_id} not found")
            
            db_cluster = response['DBClusters'][0]
            
            return {
                'db_cluster_id': db_cluster['DBClusterIdentifier'],
                'engine': db_cluster['Engine'],
                'engine_version': db_cluster['EngineVersion'],
                'status': db_cluster['Status'],
                'allocated_storage': db_cluster.get('AllocatedStorage', 0),
                'storage_encrypted': db_cluster.get('StorageEncrypted', False),
                'availability_zones': db_cluster.get('AvailabilityZones', []),
                'vpc_id': db_cluster.get('DBSubnetGroup', 'N/A'),
                'endpoint': db_cluster.get('Endpoint', 'N/A'),
                'reader_endpoint': db_cluster.get('ReaderEndpoint', 'N/A'),
                'port': db_cluster.get('Port', 'N/A'),
                'master_username': db_cluster.get('MasterUsername', 'N/A'),
                'cluster_members': [member['DBInstanceIdentifier'] for member in db_cluster.get('DBClusterMembers', [])],
                'creation_time': db_cluster.get('ClusterCreateTime', '').isoformat() if db_cluster.get('ClusterCreateTime') else 'N/A',
                'tags': self._get_resource_tags(db_cluster.get('DBClusterArn', ''))
            }
        except ClientError as e:
            if e.response['Error']['Code'] == 'DBClusterNotFoundFault':
                raise ValueError(f"DB Cluster {db_cluster_id} not found")
            else:
                raise e
    
    def get_associated_db_snapshots(self, db_instance_id: str) -> List[Dict[str, Any]]:
        """
        Get all DB snapshots associated with the RDS DB instance.
        
        Args:
            db_instance_id: The RDS DB instance identifier
            
        Returns:
            List of dictionaries containing DB snapshot details
        """
        snapshots = []
        
        try:
            response = self.rds_client.describe_db_snapshots(
                DBInstanceIdentifier=db_instance_id
            )
            
            for snapshot in response['DBSnapshots']:
                snapshot_info = {
                    'resource_type': 'DB Snapshot',
                    'resource_id': snapshot['DBSnapshotIdentifier'],
                    'db_instance_id': snapshot['DBInstanceIdentifier'],
                    'snapshot_type': snapshot['SnapshotType'],
                    'status': snapshot['Status'],
                    'allocated_storage': snapshot.get('AllocatedStorage', 0),
                    'storage_type': snapshot.get('StorageType', 'N/A'),
                    'encrypted': snapshot.get('Encrypted', False),
                    'engine': snapshot.get('Engine', 'N/A'),
                    'engine_version': snapshot.get('EngineVersion', 'N/A'),
                    'creation_time': snapshot.get('SnapshotCreateTime', '').isoformat() if snapshot.get('SnapshotCreateTime') else 'N/A',
                    'availability_zone': snapshot.get('AvailabilityZone', 'N/A'),
                    'tags': self._get_resource_tags(snapshot.get('DBSnapshotArn', ''))
                }
                snapshots.append(snapshot_info)
                
        except ClientError as e:
            print(f"Error retrieving DB snapshots: {str(e)}")
        
        return snapshots
    
    def get_associated_db_cluster_snapshots(self, db_cluster_id: str) -> List[Dict[str, Any]]:
        """
        Get all DB cluster snapshots associated with the RDS DB cluster.
        
        Args:
            db_cluster_id: The RDS DB cluster identifier
            
        Returns:
            List of dictionaries containing DB cluster snapshot details
        """
        snapshots = []
        
        try:
            response = self.rds_client.describe_db_cluster_snapshots(
                DBClusterIdentifier=db_cluster_id
            )
            
            for snapshot in response['DBClusterSnapshots']:
                snapshot_info = {
                    'resource_type': 'DB Cluster Snapshot',
                    'resource_id': snapshot['DBClusterSnapshotIdentifier'],
                    'db_cluster_id': snapshot['DBClusterIdentifier'],
                    'snapshot_type': snapshot['SnapshotType'],
                    'status': snapshot['Status'],
                    'allocated_storage': snapshot.get('AllocatedStorage', 0),
                    'storage_encrypted': snapshot.get('StorageEncrypted', False),
                    'engine': snapshot.get('Engine', 'N/A'),
                    'engine_version': snapshot.get('EngineVersion', 'N/A'),
                    'creation_time': snapshot.get('SnapshotCreateTime', '').isoformat() if snapshot.get('SnapshotCreateTime') else 'N/A',
                    'availability_zones': snapshot.get('AvailabilityZones', []),
                    'tags': self._get_resource_tags(snapshot.get('DBClusterSnapshotArn', ''))
                }
                snapshots.append(snapshot_info)
                
        except ClientError as e:
            print(f"Error retrieving DB cluster snapshots: {str(e)}")
        
        return snapshots
    
    def get_associated_security_groups(self, vpc_security_groups: List[Dict], db_security_groups: List[Dict] = None) -> List[Dict[str, Any]]:
        """
        Get all security groups associated with the RDS instance/cluster.
        
        Args:
            vpc_security_groups: List of VPC security groups from DB instance/cluster
            db_security_groups: List of DB security groups (for EC2-Classic)
            
        Returns:
            List of dictionaries containing security group details
        """
        security_groups = []
        
        # Handle VPC Security Groups
        if vpc_security_groups:
            sg_ids = [sg['VpcSecurityGroupId'] for sg in vpc_security_groups]
            
            try:
                response = self.ec2_client.describe_security_groups(
                    GroupIds=sg_ids
                )
                
                for sg in response['SecurityGroups']:
                    sg_info = {
                        'resource_type': 'VPC Security Group',
                        'resource_id': sg['GroupId'],
                        'name': sg['GroupName'],
                        'description': sg['Description'],
                        'vpc_id': sg.get('VpcId', 'N/A'),
                        'inbound_rules': len(sg.get('IpPermissions', [])),
                        'outbound_rules': len(sg.get('IpPermissionsEgress', [])),
                        'tags': {tag['Key']: tag['Value'] for tag in sg.get('Tags', [])}
                    }
                    security_groups.append(sg_info)
                    
            except ClientError as e:
                print(f"Error retrieving VPC security groups: {str(e)}")
        
        # Handle DB Security Groups (EC2-Classic)
        if db_security_groups:
            for db_sg in db_security_groups:
                sg_info = {
                    'resource_type': 'DB Security Group',
                    'resource_id': db_sg['DBSecurityGroupName'],
                    'name': db_sg['DBSecurityGroupName'],
                    'description': 'DB Security Group (EC2-Classic)',
                    'vpc_id': 'N/A (EC2-Classic)',
                    'status': db_sg.get('Status', 'N/A'),
                    'tags': {}
                }
                security_groups.append(sg_info)
        
        return security_groups
    
    def get_associated_subnet_group(self, subnet_group_name: str) -> List[Dict[str, Any]]:
        """
        Get details about the DB subnet group.
        
        Args:
            subnet_group_name: The DB subnet group name
            
        Returns:
            List containing DB subnet group details (single item)
        """
        subnet_groups = []
        
        if not subnet_group_name or subnet_group_name == 'N/A':
            return subnet_groups
        
        try:
            response = self.rds_client.describe_db_subnet_groups(
                DBSubnetGroupName=subnet_group_name
            )
            
            for subnet_group in response['DBSubnetGroups']:
                subnet_info = {
                    'resource_type': 'DB Subnet Group',
                    'resource_id': subnet_group['DBSubnetGroupName'],
                    'name': subnet_group['DBSubnetGroupName'],
                    'description': subnet_group['DBSubnetGroupDescription'],
                    'vpc_id': subnet_group['VpcId'],
                    'status': subnet_group['SubnetGroupStatus'],
                    'subnets': [subnet['SubnetIdentifier'] for subnet in subnet_group.get('Subnets', [])],
                    'availability_zones': list(set([subnet['SubnetAvailabilityZone']['Name'] for subnet in subnet_group.get('Subnets', [])])),
                    'tags': self._get_resource_tags(subnet_group.get('DBSubnetGroupArn', ''))
                }
                subnet_groups.append(subnet_info)
                
        except ClientError as e:
            print(f"Error retrieving DB subnet group: {str(e)}")
        
        return subnet_groups
    
    def get_associated_parameter_groups(self, parameter_groups: List[Dict]) -> List[Dict[str, Any]]:
        """
        Get details about the DB parameter groups.
        
        Args:
            parameter_groups: List of parameter groups from DB instance/cluster
            
        Returns:
            List of dictionaries containing parameter group details
        """
        param_groups = []
        
        for pg in parameter_groups:
            param_group_name = pg.get('DBParameterGroupName') or pg.get('DBClusterParameterGroupName')
            
            if not param_group_name:
                continue
            
            try:
                # Determine if it's a cluster parameter group or instance parameter group
                if 'DBClusterParameterGroupName' in pg:
                    response = self.rds_client.describe_db_cluster_parameter_groups(
                        DBClusterParameterGroupName=param_group_name
                    )
                    param_group_type = 'DB Cluster Parameter Group'
                    param_groups_list = response['DBClusterParameterGroups']
                else:
                    response = self.rds_client.describe_db_parameter_groups(
                        DBParameterGroupName=param_group_name
                    )
                    param_group_type = 'DB Parameter Group'
                    param_groups_list = response['DBParameterGroups']
                
                for param_group in param_groups_list:
                    pg_info = {
                        'resource_type': param_group_type,
                        'resource_id': param_group_name,
                        'name': param_group_name,
                        'family': param_group.get('DBParameterGroupFamily') or param_group.get('DBClusterParameterGroupFamily'),
                        'description': param_group['Description'],
                        'tags': self._get_resource_tags(param_group.get('DBParameterGroupArn') or param_group.get('DBClusterParameterGroupArn', ''))
                    }
                    param_groups.append(pg_info)
                    
            except ClientError as e:
                print(f"Error retrieving parameter group {param_group_name}: {str(e)}")
        
        return param_groups
    
    def get_associated_option_groups(self, option_groups: List[Dict]) -> List[Dict[str, Any]]:
        """
        Get details about the option groups.
        
        Args:
            option_groups: List of option groups from DB instance/cluster
            
        Returns:
            List of dictionaries containing option group details
        """
        opt_groups = []
        
        for og in option_groups:
            option_group_name = og.get('OptionGroupName') or og.get('DBClusterOptionGroupName')
            
            if not option_group_name:
                continue
            
            try:
                response = self.rds_client.describe_option_groups(
                    OptionGroupName=option_group_name
                )
                
                for option_group in response['OptionGroupsList']:
                    og_info = {
                        'resource_type': 'Option Group',
                        'resource_id': option_group_name,
                        'name': option_group_name,
                        'description': option_group['OptionGroupDescription'],
                        'engine_name': option_group['EngineName'],
                        'major_engine_version': option_group['MajorEngineVersion'],
                        'vpc_id': option_group.get('VpcId', 'N/A'),
                        'options': [option['OptionName'] for option in option_group.get('Options', [])],
                        'tags': self._get_resource_tags(option_group.get('OptionGroupArn', ''))
                    }
                    opt_groups.append(og_info)
                    
            except ClientError as e:
                print(f"Error retrieving option group {option_group_name}: {str(e)}")
        
        return opt_groups
    
    def _get_resource_tags(self, resource_arn: str) -> Dict[str, str]:
        """
        Get tags for a resource using its ARN.
        
        Args:
            resource_arn: The ARN of the resource
            
        Returns:
            Dictionary of tags
        """
        if not resource_arn:
            return {}
        
        try:
            response = self.rds_client.list_tags_for_resource(
                ResourceName=resource_arn
            )
            return {tag['Key']: tag['Value'] for tag in response.get('TagList', [])}
        except ClientError:
            return {}
    
    def discover_db_instance_resources(self, db_instance_id: str) -> Dict[str, Any]:
        """
        Discover all billable resources associated with an RDS DB instance.
        
        Args:
            db_instance_id: The RDS DB instance identifier
            
        Returns:
            Dictionary containing all discovered resources
        """
        print(f"Discovering resources for RDS DB instance: {db_instance_id}")
        
        try:
            # Get DB instance details first to validate it exists
            instance_details = self.get_db_instance_details(db_instance_id)
            
            # Discover all associated resources
            all_resources = []
            
            # Add DB instance itself as a resource
            instance_resource = {
                'resource_type': 'DB Instance',
                'resource_id': db_instance_id,
                'db_instance_class': instance_details['db_instance_class'],
                'engine': instance_details['engine'],
                'engine_version': instance_details['engine_version'],
                'status': instance_details['status'],
                'allocated_storage': instance_details['allocated_storage'],
                'storage_type': instance_details['storage_type'],
                'storage_encrypted': instance_details['storage_encrypted'],
                'availability_zone': instance_details['availability_zone'],
                'multi_az': instance_details['multi_az'],
                'vpc_id': instance_details['vpc_id'],
                'endpoint': instance_details['endpoint'],
                'port': instance_details['port'],
                'tags': instance_details['tags']
            }
            all_resources.append(instance_resource)
            
            # Get the full DB instance details for extracting associated resources
            response = self.rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
            db_instance = response['DBInstances'][0]
            
            # Discover associated resources
            snapshots = self.get_associated_db_snapshots(db_instance_id)
            security_groups = self.get_associated_security_groups(
                db_instance.get('VpcSecurityGroups', []),
                db_instance.get('DBSecurityGroups', [])
            )
            subnet_groups = self.get_associated_subnet_group(instance_details['subnet_group'])
            parameter_groups = self.get_associated_parameter_groups(db_instance.get('DBParameterGroups', []))
            option_groups = self.get_associated_option_groups(db_instance.get('OptionGroupMemberships', []))
            
            # Combine all resources
            all_resources.extend(snapshots)
            all_resources.extend(security_groups)
            all_resources.extend(subnet_groups)
            all_resources.extend(parameter_groups)
            all_resources.extend(option_groups)
            
            return {
                'resource_type': 'db_instance',
                'resource_details': instance_details,
                'resources': all_resources,
                'summary': {
                    'total_resources': len(all_resources),
                    'snapshots': len(snapshots),
                    'security_groups': len(security_groups),
                    'subnet_groups': len(subnet_groups),
                    'parameter_groups': len(parameter_groups),
                    'option_groups': len(option_groups)
                }
            }
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None
    
    def discover_db_cluster_resources(self, db_cluster_id: str) -> Dict[str, Any]:
        """
        Discover all billable resources associated with an RDS DB cluster.
        
        Args:
            db_cluster_id: The RDS DB cluster identifier
            
        Returns:
            Dictionary containing all discovered resources
        """
        print(f"Discovering resources for RDS DB cluster: {db_cluster_id}")
        
        try:
            # Get DB cluster details first to validate it exists
            cluster_details = self.get_db_cluster_details(db_cluster_id)
            
            # Discover all associated resources
            all_resources = []
            
            # Add DB cluster itself as a resource
            cluster_resource = {
                'resource_type': 'DB Cluster',
                'resource_id': db_cluster_id,
                'engine': cluster_details['engine'],
                'engine_version': cluster_details['engine_version'],
                'status': cluster_details['status'],
                'allocated_storage': cluster_details['allocated_storage'],
                'storage_encrypted': cluster_details['storage_encrypted'],
                'availability_zones': cluster_details['availability_zones'],
                'vpc_id': cluster_details['vpc_id'],
                'endpoint': cluster_details['endpoint'],
                'reader_endpoint': cluster_details['reader_endpoint'],
                'port': cluster_details['port'],
                'cluster_members': cluster_details['cluster_members'],
                'tags': cluster_details['tags']
            }
            all_resources.append(cluster_resource)
            
            # Get the full DB cluster details for extracting associated resources
            response = self.rds_client.describe_db_clusters(DBClusterIdentifier=db_cluster_id)
            db_cluster = response['DBClusters'][0]
            
            # Discover associated resources
            cluster_snapshots = self.get_associated_db_cluster_snapshots(db_cluster_id)
            security_groups = self.get_associated_security_groups(db_cluster.get('VpcSecurityGroups', []))
            subnet_groups = self.get_associated_subnet_group(db_cluster.get('DBSubnetGroup', ''))
            
            # For clusters, parameter groups are handled differently
            cluster_param_groups = []
            if db_cluster.get('DBClusterParameterGroup'):
                cluster_param_groups = self.get_associated_parameter_groups([{
                    'DBClusterParameterGroupName': db_cluster['DBClusterParameterGroup']
                }])
            
            cluster_option_groups = self.get_associated_option_groups(db_cluster.get('DBClusterOptionGroupMemberships', []))
            
            # Get cluster member instances
            member_instances = []
            for member in db_cluster.get('DBClusterMembers', []):
                try:
                    member_details = self.get_db_instance_details(member['DBInstanceIdentifier'])
                    member_resource = {
                        'resource_type': 'DB Cluster Member',
                        'resource_id': member['DBInstanceIdentifier'],
                        'db_instance_class': member_details['db_instance_class'],
                        'engine': member_details['engine'],
                        'status': member_details['status'],
                        'is_cluster_writer': member.get('IsClusterWriter', False),
                        'promotion_tier': member.get('PromotionTier', 0),
                        'availability_zone': member_details['availability_zone'],
                        'tags': member_details['tags']
                    }
                    member_instances.append(member_resource)
                except Exception as e:
                    print(f"Error getting details for cluster member {member['DBInstanceIdentifier']}: {str(e)}")
            
            # Combine all resources
            all_resources.extend(cluster_snapshots)
            all_resources.extend(security_groups)
            all_resources.extend(subnet_groups)
            all_resources.extend(cluster_param_groups)
            all_resources.extend(cluster_option_groups)
            all_resources.extend(member_instances)
            
            return {
                'resource_type': 'db_cluster',
                'resource_details': cluster_details,
                'resources': all_resources,
                'summary': {
                    'total_resources': len(all_resources),
                    'cluster_snapshots': len(cluster_snapshots),
                    'security_groups': len(security_groups),
                    'subnet_groups': len(subnet_groups),
                    'parameter_groups': len(cluster_param_groups),
                    'option_groups': len(cluster_option_groups),
                    'cluster_members': len(member_instances)
                }
            }
            
        except ValueError as e:
            print(f"Error: {str(e)}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


def main():
    """Main function to run the resource discovery tool."""
    if len(sys.argv) < 2:
        print("Usage: python rds_resource_discovery.py <db-instance-id|db-cluster-id> [--cluster] [region] [profile]")
        print("Examples:")
        print("  python rds_resource_discovery.py my-db-instance")
        print("  python rds_resource_discovery.py my-db-cluster --cluster")
        print("  python rds_resource_discovery.py my-db-instance us-east-1 default")
        sys.exit(1)
    
    identifier = sys.argv[1]
    is_cluster = '--cluster' in sys.argv
    
    # Remove --cluster from args to get region and profile
    args = [arg for arg in sys.argv[2:] if arg != '--cluster']
    region = args[0] if len(args) > 0 else None
    profile = args[1] if len(args) > 1 else None
    
    # Initialize the discovery tool
    discovery = RDSResourceDiscovery(region_name=region, profile_name=profile)
    
    # Discover all resources
    if is_cluster:
        result = discovery.discover_db_cluster_resources(identifier)
    else:
        result = discovery.discover_db_instance_resources(identifier)
    
    if result:
        print(f"\nResource discovery completed successfully!")
        print(f"Region: {discovery.region}")
        print(f"Total resources found: {result['summary']['total_resources']}")
        
        # Print summary
        print("\nResource Summary:")
        for resource_type, count in result['summary'].items():
            if resource_type != 'total_resources':
                print(f"  {resource_type.replace('_', ' ').title()}: {count}")
        
        # Return the result for further processing
        return result
    else:
        print("Resource discovery failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()

