from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from gmctl.gmclient import GitmoxiClient
from gmctl.db_functions import get_deployments
import re
import logging

logger = logging.getLogger(__name__)

import click
from gmctl.utils import print_table, print_status

@click.group()
@click.pass_context
def ecs(ctx):
    pass

@ecs.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.option('-c', '--commit-hash', help='The commit hash')
@click.option('-a', '--account-id', help='The AWS account ID')
@click.option('-re', '--region', help='The AWS region')
@click.option('-s', '--service', help='The ECS service')
@click.option('-cl', '--cluster', help='The ECS cluster')
@click.option('-st', '--status', type=click.Choice(["PROCESSING", "PROCESSED_ERROR", "PROCESSED_SUCCESS"]), help='The deployment status')
@click.option('-n', '--number-of-records', help='Number of records', default=10)
@click.option('-v', '--verbose', is_flag=True, help='Verbose output')
@click.option('-A', '--show-all', is_flag=True, help='Verbose for all deployments')
@click.pass_context
def get(ctx, repo_url, commit_hash, account_id, region, 
        service, cluster, status, number_of_records, verbose, show_all):        
    try:
        
        gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
        conditions = {"repo_url": repo_url, "commit_hash": commit_hash, "account_id": account_id,
                      "region": region, "service": service, "cluster": cluster, "status": status}
        deployments = get_deployments("ecs", gmclient, conditions, number_of_records)
        to_display = []
        summary_keys = ["repo_url", "commit_hash", "account_id", "region", "service", 
                        "cluster", "create_timestamp", "status", "file_prefix"]
        for deployment in deployments:
            to_display.append({k: deployment.get(k) for k in summary_keys})
            
        print_table(to_display)
        if verbose:
            for deployment in deployments:
                if not show_all and deployment.get("status") != "PROCESSED_ERROR":
                    continue
                print("-------------------------------")
                print(f"\n{deployment.get('status')}, {deployment.get('repo_url')}, {deployment.get('file_prefix')}, "
                    f"{deployment.get('service')}, {deployment.get('cluster')}, {deployment.get('account_id')}, {deployment.get('region')}: \n")             
                print_status(deployment.get("status_details", []))
                print("-------------------------------")
    except Exception as e:
        click.echo(f"Error: {e}")