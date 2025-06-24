#!/usr/bin/env python3
"""
Table Formatter for AWS RDS Resource Discovery

This module provides functions to format the discovered AWS RDS resources into various table formats.
"""

import pandas as pd
from tabulate import tabulate
import json
from typing import Dict, List, Any, Optional


class RDSResourceTableFormatter:
    """Class to format discovered AWS RDS resources into tables."""
    
    def __init__(self):
        """Initialize the table formatter."""
        pass
    
    def format_resources_table(self, resources: List[Dict[str, Any]], 
                             table_format: str = "grid") -> str:
        """
        Format the list of resources into a table.
        
        Args:
            resources: List of resource dictionaries
            table_format: Table format for tabulate (grid, simple, fancy_grid, etc.)
            
        Returns:
            Formatted table as string
        """
        if not resources:
            return "No resources found."
        
        # Create a list to hold table rows
        table_data = []
        
        for resource in resources:
            # Extract common fields for all resource types
            row = {
                'Resource Type': resource.get('resource_type', 'Unknown'),
                'Resource ID': resource.get('resource_id', 'N/A'),
                'Details': self._format_resource_details(resource)
            }
            table_data.append(row)
        
        # Convert to DataFrame for better handling
        df = pd.DataFrame(table_data)
        
        # Use tabulate to create the table
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def format_detailed_resources_table(self, resources: List[Dict[str, Any]], 
                                      table_format: str = "grid") -> str:
        """
        Format resources into a detailed table with separate columns for key attributes.
        
        Args:
            resources: List of resource dictionaries
            table_format: Table format for tabulate
            
        Returns:
            Formatted detailed table as string
        """
        if not resources:
            return "No resources found."
        
        # Group resources by type for better organization
        resource_groups = {}
        for resource in resources:
            resource_type = resource.get('resource_type', 'Unknown')
            if resource_type not in resource_groups:
                resource_groups[resource_type] = []
            resource_groups[resource_type].append(resource)
        
        # Create separate tables for each resource type
        formatted_tables = []
        
        for resource_type, resource_list in resource_groups.items():
            formatted_tables.append(f"\n## {resource_type}s\n")
            
            if resource_type == 'DB Instance':
                table = self._format_db_instances_table(resource_list, table_format)
            elif resource_type == 'DB Cluster':
                table = self._format_db_clusters_table(resource_list, table_format)
            elif resource_type == 'DB Cluster Member':
                table = self._format_db_cluster_members_table(resource_list, table_format)
            elif resource_type == 'DB Snapshot':
                table = self._format_db_snapshots_table(resource_list, table_format)
            elif resource_type == 'DB Cluster Snapshot':
                table = self._format_db_cluster_snapshots_table(resource_list, table_format)
            elif resource_type == 'VPC Security Group':
                table = self._format_vpc_security_groups_table(resource_list, table_format)
            elif resource_type == 'DB Security Group':
                table = self._format_db_security_groups_table(resource_list, table_format)
            elif resource_type == 'DB Subnet Group':
                table = self._format_db_subnet_groups_table(resource_list, table_format)
            elif resource_type == 'DB Parameter Group':
                table = self._format_db_parameter_groups_table(resource_list, table_format)
            elif resource_type == 'DB Cluster Parameter Group':
                table = self._format_db_cluster_parameter_groups_table(resource_list, table_format)
            elif resource_type == 'Option Group':
                table = self._format_option_groups_table(resource_list, table_format)
            else:
                table = self._format_generic_table(resource_list, table_format)
            
            formatted_tables.append(table)
        
        return '\n'.join(formatted_tables)
    
    def _format_db_instances_table(self, instances: List[Dict[str, Any]], 
                                 table_format: str) -> str:
        """Format DB instances into a table."""
        table_data = []
        for instance in instances:
            row = {
                'DB Instance ID': instance.get('resource_id', 'N/A'),
                'Instance Class': instance.get('db_instance_class', 'N/A'),
                'Engine': instance.get('engine', 'N/A'),
                'Engine Version': instance.get('engine_version', 'N/A'),
                'Status': instance.get('status', 'N/A'),
                'Storage (GB)': instance.get('allocated_storage', 'N/A'),
                'Storage Type': instance.get('storage_type', 'N/A'),
                'Encrypted': instance.get('storage_encrypted', 'N/A'),
                'Multi-AZ': instance.get('multi_az', 'N/A'),
                'AZ': instance.get('availability_zone', 'N/A'),
                'VPC ID': instance.get('vpc_id', 'N/A'),
                'Endpoint': instance.get('endpoint', 'N/A'),
                'Port': instance.get('port', 'N/A'),
                'Tags': self._format_tags(instance.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_clusters_table(self, clusters: List[Dict[str, Any]], 
                                table_format: str) -> str:
        """Format DB clusters into a table."""
        table_data = []
        for cluster in clusters:
            row = {
                'DB Cluster ID': cluster.get('resource_id', 'N/A'),
                'Engine': cluster.get('engine', 'N/A'),
                'Engine Version': cluster.get('engine_version', 'N/A'),
                'Status': cluster.get('status', 'N/A'),
                'Storage (GB)': cluster.get('allocated_storage', 'N/A'),
                'Encrypted': cluster.get('storage_encrypted', 'N/A'),
                'Availability Zones': ', '.join(cluster.get('availability_zones', [])),
                'VPC ID': cluster.get('vpc_id', 'N/A'),
                'Endpoint': cluster.get('endpoint', 'N/A'),
                'Reader Endpoint': cluster.get('reader_endpoint', 'N/A'),
                'Port': cluster.get('port', 'N/A'),
                'Members': ', '.join(cluster.get('cluster_members', [])),
                'Tags': self._format_tags(cluster.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_cluster_members_table(self, members: List[Dict[str, Any]], 
                                       table_format: str) -> str:
        """Format DB cluster members into a table."""
        table_data = []
        for member in members:
            row = {
                'Instance ID': member.get('resource_id', 'N/A'),
                'Instance Class': member.get('db_instance_class', 'N/A'),
                'Engine': member.get('engine', 'N/A'),
                'Status': member.get('status', 'N/A'),
                'Is Writer': member.get('is_cluster_writer', 'N/A'),
                'Promotion Tier': member.get('promotion_tier', 'N/A'),
                'Availability Zone': member.get('availability_zone', 'N/A'),
                'Tags': self._format_tags(member.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_snapshots_table(self, snapshots: List[Dict[str, Any]], 
                                 table_format: str) -> str:
        """Format DB snapshots into a table."""
        table_data = []
        for snapshot in snapshots:
            row = {
                'Snapshot ID': snapshot.get('resource_id', 'N/A'),
                'DB Instance ID': snapshot.get('db_instance_id', 'N/A'),
                'Type': snapshot.get('snapshot_type', 'N/A'),
                'Status': snapshot.get('status', 'N/A'),
                'Storage (GB)': snapshot.get('allocated_storage', 'N/A'),
                'Storage Type': snapshot.get('storage_type', 'N/A'),
                'Encrypted': snapshot.get('encrypted', 'N/A'),
                'Engine': snapshot.get('engine', 'N/A'),
                'Creation Time': snapshot.get('creation_time', 'N/A')[:19] if snapshot.get('creation_time') else 'N/A',
                'AZ': snapshot.get('availability_zone', 'N/A'),
                'Tags': self._format_tags(snapshot.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_cluster_snapshots_table(self, snapshots: List[Dict[str, Any]], 
                                         table_format: str) -> str:
        """Format DB cluster snapshots into a table."""
        table_data = []
        for snapshot in snapshots:
            row = {
                'Snapshot ID': snapshot.get('resource_id', 'N/A'),
                'DB Cluster ID': snapshot.get('db_cluster_id', 'N/A'),
                'Type': snapshot.get('snapshot_type', 'N/A'),
                'Status': snapshot.get('status', 'N/A'),
                'Storage (GB)': snapshot.get('allocated_storage', 'N/A'),
                'Encrypted': snapshot.get('storage_encrypted', 'N/A'),
                'Engine': snapshot.get('engine', 'N/A'),
                'Creation Time': snapshot.get('creation_time', 'N/A')[:19] if snapshot.get('creation_time') else 'N/A',
                'Availability Zones': ', '.join(snapshot.get('availability_zones', [])),
                'Tags': self._format_tags(snapshot.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_vpc_security_groups_table(self, security_groups: List[Dict[str, Any]], 
                                        table_format: str) -> str:
        """Format VPC security groups into a table."""
        table_data = []
        for sg in security_groups:
            row = {
                'Security Group ID': sg.get('resource_id', 'N/A'),
                'Name': sg.get('name', 'N/A'),
                'Description': sg.get('description', 'N/A')[:40] + '...' if len(sg.get('description', '')) > 40 else sg.get('description', 'N/A'),
                'VPC ID': sg.get('vpc_id', 'N/A'),
                'Inbound Rules': sg.get('inbound_rules', 'N/A'),
                'Outbound Rules': sg.get('outbound_rules', 'N/A'),
                'Tags': self._format_tags(sg.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_security_groups_table(self, security_groups: List[Dict[str, Any]], 
                                       table_format: str) -> str:
        """Format DB security groups into a table."""
        table_data = []
        for sg in security_groups:
            row = {
                'DB Security Group': sg.get('resource_id', 'N/A'),
                'Name': sg.get('name', 'N/A'),
                'Description': sg.get('description', 'N/A'),
                'Status': sg.get('status', 'N/A'),
                'VPC': sg.get('vpc_id', 'N/A')
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_subnet_groups_table(self, subnet_groups: List[Dict[str, Any]], 
                                     table_format: str) -> str:
        """Format DB subnet groups into a table."""
        table_data = []
        for sg in subnet_groups:
            row = {
                'Subnet Group Name': sg.get('resource_id', 'N/A'),
                'Description': sg.get('description', 'N/A')[:40] + '...' if len(sg.get('description', '')) > 40 else sg.get('description', 'N/A'),
                'VPC ID': sg.get('vpc_id', 'N/A'),
                'Status': sg.get('status', 'N/A'),
                'Subnets': ', '.join(sg.get('subnets', [])[:3]) + ('...' if len(sg.get('subnets', [])) > 3 else ''),
                'Availability Zones': ', '.join(sg.get('availability_zones', [])),
                'Tags': self._format_tags(sg.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_parameter_groups_table(self, parameter_groups: List[Dict[str, Any]], 
                                        table_format: str) -> str:
        """Format DB parameter groups into a table."""
        table_data = []
        for pg in parameter_groups:
            row = {
                'Parameter Group Name': pg.get('resource_id', 'N/A'),
                'Family': pg.get('family', 'N/A'),
                'Description': pg.get('description', 'N/A')[:40] + '...' if len(pg.get('description', '')) > 40 else pg.get('description', 'N/A'),
                'Tags': self._format_tags(pg.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_db_cluster_parameter_groups_table(self, parameter_groups: List[Dict[str, Any]], 
                                                table_format: str) -> str:
        """Format DB cluster parameter groups into a table."""
        table_data = []
        for pg in parameter_groups:
            row = {
                'Cluster Parameter Group': pg.get('resource_id', 'N/A'),
                'Family': pg.get('family', 'N/A'),
                'Description': pg.get('description', 'N/A')[:40] + '...' if len(pg.get('description', '')) > 40 else pg.get('description', 'N/A'),
                'Tags': self._format_tags(pg.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_option_groups_table(self, option_groups: List[Dict[str, Any]], 
                                  table_format: str) -> str:
        """Format option groups into a table."""
        table_data = []
        for og in option_groups:
            row = {
                'Option Group Name': og.get('resource_id', 'N/A'),
                'Description': og.get('description', 'N/A')[:40] + '...' if len(og.get('description', '')) > 40 else og.get('description', 'N/A'),
                'Engine': og.get('engine_name', 'N/A'),
                'Engine Version': og.get('major_engine_version', 'N/A'),
                'VPC ID': og.get('vpc_id', 'N/A'),
                'Options': ', '.join(og.get('options', [])),
                'Tags': self._format_tags(og.get('tags', {}))
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_generic_table(self, resources: List[Dict[str, Any]], 
                            table_format: str) -> str:
        """Format generic resources into a table."""
        table_data = []
        for resource in resources:
            row = {
                'Resource ID': resource.get('resource_id', 'N/A'),
                'Details': self._format_resource_details(resource)
            }
            table_data.append(row)
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def _format_resource_details(self, resource: Dict[str, Any]) -> str:
        """Format resource details into a compact string."""
        details = []
        
        # Skip common fields that are already displayed
        skip_fields = {'resource_type', 'resource_id', 'tags'}
        
        for key, value in resource.items():
            if key not in skip_fields and value is not None and value != 'N/A':
                if isinstance(value, (list, dict)):
                    if value:  # Only add if not empty
                        details.append(f"{key}: {str(value)[:50]}...")
                else:
                    details.append(f"{key}: {value}")
        
        return '; '.join(details[:3])  # Limit to first 3 details to keep it readable
    
    def _format_tags(self, tags: Dict[str, str]) -> str:
        """Format tags dictionary into a readable string."""
        if not tags:
            return 'None'
        
        tag_strings = [f"{k}:{v}" for k, v in list(tags.items())[:2]]  # Show first 2 tags
        result = ', '.join(tag_strings)
        
        if len(tags) > 2:
            result += f" (+{len(tags) - 2} more)"
        
        return result
    
    def format_summary_table(self, summary: Dict[str, Any], 
                           table_format: str = "grid") -> str:
        """
        Format the resource summary into a table.
        
        Args:
            summary: Summary dictionary from resource discovery
            table_format: Table format for tabulate
            
        Returns:
            Formatted summary table as string
        """
        table_data = []
        
        for resource_type, count in summary.items():
            if resource_type != 'total_resources':
                row = {
                    'Resource Type': resource_type.replace('_', ' ').title(),
                    'Count': count
                }
                table_data.append(row)
        
        # Add total row
        table_data.append({
            'Resource Type': 'TOTAL',
            'Count': summary.get('total_resources', 0)
        })
        
        df = pd.DataFrame(table_data)
        return tabulate(df, headers='keys', tablefmt=table_format, showindex=False)
    
    def export_to_csv(self, resources: List[Dict[str, Any]], 
                     filename: str) -> str:
        """
        Export resources to CSV file.
        
        Args:
            resources: List of resource dictionaries
            filename: Output CSV filename
            
        Returns:
            Success message with filename
        """
        # Flatten the resources for CSV export
        flattened_resources = []
        
        for resource in resources:
            flattened = {}
            for key, value in resource.items():
                if isinstance(value, dict):
                    # Flatten dictionaries (like tags)
                    for sub_key, sub_value in value.items():
                        flattened[f"{key}_{sub_key}"] = sub_value
                elif isinstance(value, list):
                    # Convert lists to comma-separated strings
                    flattened[key] = ', '.join(map(str, value))
                else:
                    flattened[key] = value
            
            flattened_resources.append(flattened)
        
        df = pd.DataFrame(flattened_resources)
        df.to_csv(filename, index=False)
        
        return f"Resources exported to {filename}"
    
    def export_to_json(self, discovery_result: Dict[str, Any], 
                      filename: str) -> str:
        """
        Export complete discovery result to JSON file.
        
        Args:
            discovery_result: Complete result from resource discovery
            filename: Output JSON filename
            
        Returns:
            Success message with filename
        """
        with open(filename, 'w') as f:
            json.dump(discovery_result, f, indent=2, default=str)
        
        return f"Discovery result exported to {filename}"


def main():
    """Example usage of the RDSResourceTableFormatter."""
    # This is just for testing the formatter
    sample_resources = [
        {
            'resource_type': 'DB Instance',
            'resource_id': 'my-db-instance',
            'db_instance_class': 'db.t3.micro',
            'engine': 'mysql',
            'engine_version': '8.0.35',
            'status': 'available',
            'allocated_storage': 20,
            'storage_type': 'gp2',
            'storage_encrypted': True,
            'multi_az': False,
            'availability_zone': 'us-east-1a',
            'vpc_id': 'vpc-12345678',
            'endpoint': 'my-db-instance.abcdef123456.us-east-1.rds.amazonaws.com',
            'port': 3306,
            'tags': {'Name': 'MyDatabase', 'Environment': 'Production'}
        },
        {
            'resource_type': 'DB Snapshot',
            'resource_id': 'my-db-snapshot',
            'db_instance_id': 'my-db-instance',
            'snapshot_type': 'manual',
            'status': 'available',
            'allocated_storage': 20,
            'storage_type': 'gp2',
            'encrypted': True,
            'engine': 'mysql',
            'creation_time': '2024-06-20T10:30:00.000Z',
            'availability_zone': 'us-east-1a',
            'tags': {'Name': 'MySnapshot'}
        }
    ]
    
    formatter = RDSResourceTableFormatter()
    
    print("Simple Table Format:")
    print(formatter.format_resources_table(sample_resources))
    
    print("\n\nDetailed Table Format:")
    print(formatter.format_detailed_resources_table(sample_resources))


if __name__ == "__main__":
    main()

