#!/usr/bin/env python3
"""
AWS RDS Billable Resource Discovery CLI Tool

This is the main command-line interface for discovering and displaying all billable resources
associated with AWS RDS DB instances and DB clusters.
"""

import argparse
import sys
import os
from typing import Dict, Any, Optional

# Import our modules
from rds_resource_discovery import RDSResourceDiscovery
from rds_table_formatter import RDSResourceTableFormatter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Discover and list all billable resources associated with an AWS RDS DB instance or cluster',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-db-instance
  %(prog)s my-aurora-cluster --cluster
  %(prog)s my-db-instance --region us-west-2 --profile production
  %(prog)s my-db-instance --detailed --format fancy_grid
  %(prog)s my-db-instance --export-csv resources.csv --export-json results.json
        """
    )
    
    parser.add_argument(
        'identifier',
        help='RDS DB instance identifier or DB cluster identifier'
    )
    
    parser.add_argument(
        '--cluster',
        action='store_true',
        help='Treat the identifier as a DB cluster identifier instead of DB instance'
    )
    
    parser.add_argument(
        '--region',
        help='AWS region name (default: use AWS CLI default or environment)'
    )
    
    parser.add_argument(
        '--profile',
        help='AWS profile name (default: use AWS CLI default)'
    )
    
    parser.add_argument(
        '--format',
        choices=['grid', 'simple', 'fancy_grid', 'pipe', 'orgtbl', 'rst', 'mediawiki', 'html', 'latex'],
        default='grid',
        help='Table format for output (default: grid)'
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='Show detailed tables grouped by resource type'
    )
    
    parser.add_argument(
        '--summary-only',
        action='store_true',
        help='Show only the resource summary table'
    )
    
    parser.add_argument(
        '--export-csv',
        metavar='FILENAME',
        help='Export resources to CSV file'
    )
    
    parser.add_argument(
        '--export-json',
        metavar='FILENAME',
        help='Export complete results to JSON file'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='AWS RDS Resource Discovery Tool v1.0.0'
    )
    
    return parser.parse_args()


def display_resource_info(discovery_result: Dict[str, Any], args) -> None:
    """
    Display the resource information based on the command line arguments.
    
    Args:
        discovery_result: Result from resource discovery
        args: Parsed command line arguments
    """
    formatter = RDSResourceTableFormatter()
    
    # Display basic information
    resource_details = discovery_result['resource_details']
    resource_type = discovery_result['resource_type']
    
    print(f"\n{'='*80}")
    print(f"AWS RDS Resource Discovery Results")
    print(f"{'='*80}")
    
    if resource_type == 'db_instance':
        print(f"DB Instance ID: {resource_details['db_instance_id']}")
        print(f"Instance Class: {resource_details['db_instance_class']}")
        print(f"Engine: {resource_details['engine']} {resource_details['engine_version']}")
        print(f"Status: {resource_details['status']}")
        print(f"Storage: {resource_details['allocated_storage']} GB ({resource_details['storage_type']})")
        print(f"Encrypted: {resource_details['storage_encrypted']}")
        print(f"Multi-AZ: {resource_details['multi_az']}")
        print(f"Availability Zone: {resource_details['availability_zone']}")
        print(f"VPC ID: {resource_details['vpc_id']}")
        print(f"Endpoint: {resource_details['endpoint']}:{resource_details['port']}")
        if resource_details['db_cluster_identifier']:
            print(f"DB Cluster: {resource_details['db_cluster_identifier']}")
    else:  # db_cluster
        print(f"DB Cluster ID: {resource_details['db_cluster_id']}")
        print(f"Engine: {resource_details['engine']} {resource_details['engine_version']}")
        print(f"Status: {resource_details['status']}")
        print(f"Storage: {resource_details['allocated_storage']} GB")
        print(f"Encrypted: {resource_details['storage_encrypted']}")
        print(f"Availability Zones: {', '.join(resource_details['availability_zones'])}")
        print(f"VPC ID: {resource_details['vpc_id']}")
        print(f"Endpoint: {resource_details['endpoint']}:{resource_details['port']}")
        print(f"Reader Endpoint: {resource_details['reader_endpoint']}")
        print(f"Cluster Members: {', '.join(resource_details['cluster_members'])}")
    
    print(f"Creation Time: {resource_details['creation_time']}")
    
    # Display tags if any
    if resource_details['tags']:
        print(f"Tags: {', '.join([f'{k}:{v}' for k, v in resource_details['tags'].items()])}")
    
    print(f"\nRegion: {args.region or 'default'}")
    print(f"Total Resources Found: {discovery_result['summary']['total_resources']}")
    
    # Display summary table
    print(f"\n{'='*80}")
    print("Resource Summary:")
    print(f"{'='*80}")
    summary_table = formatter.format_summary_table(discovery_result['summary'], args.format)
    print(summary_table)
    
    # Display detailed information if not summary-only
    if not args.summary_only:
        if args.detailed:
            print(f"\n{'='*80}")
            print("Detailed Resource Information:")
            print(f"{'='*80}")
            detailed_table = formatter.format_detailed_resources_table(
                discovery_result['resources'], args.format
            )
            print(detailed_table)
        else:
            print(f"\n{'='*80}")
            print("All Resources:")
            print(f"{'='*80}")
            resources_table = formatter.format_resources_table(
                discovery_result['resources'], args.format
            )
            print(resources_table)


def export_results(discovery_result: Dict[str, Any], args) -> None:
    """
    Export results to files if requested.
    
    Args:
        discovery_result: Result from resource discovery
        args: Parsed command line arguments
    """
    formatter = RDSResourceTableFormatter()
    
    if args.export_csv:
        try:
            message = formatter.export_to_csv(discovery_result['resources'], args.export_csv)
            print(f"\n✓ {message}")
        except Exception as e:
            print(f"\n✗ Error exporting to CSV: {str(e)}")
    
    if args.export_json:
        try:
            message = formatter.export_to_json(discovery_result, args.export_json)
            print(f"\n✓ {message}")
        except Exception as e:
            print(f"\n✗ Error exporting to JSON: {str(e)}")


def main():
    """Main function."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Initialize the discovery tool
        print(f"Initializing AWS RDS Resource Discovery...")
        print(f"Target: {'DB Cluster' if args.cluster else 'DB Instance'} '{args.identifier}'")
        if args.region:
            print(f"Region: {args.region}")
        if args.profile:
            print(f"Profile: {args.profile}")
        
        discovery = RDSResourceDiscovery(region_name=args.region, profile_name=args.profile)
        
        # Discover resources
        if args.cluster:
            discovery_result = discovery.discover_db_cluster_resources(args.identifier)
        else:
            discovery_result = discovery.discover_db_instance_resources(args.identifier)
        
        if not discovery_result:
            print(f"\n✗ Failed to discover resources for {args.identifier}")
            sys.exit(1)
        
        # Display results
        display_resource_info(discovery_result, args)
        
        # Export results if requested
        export_results(discovery_result, args)
        
        print(f"\n{'='*80}")
        print("✓ Resource discovery completed successfully!")
        print(f"{'='*80}")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

