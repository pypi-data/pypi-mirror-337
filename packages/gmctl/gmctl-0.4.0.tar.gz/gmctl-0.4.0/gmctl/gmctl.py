from dotenv import load_dotenv
load_dotenv() 

import logging
logging.basicConfig(level=logging.ERROR, format='gmctl - %(name)s - %(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import click
from gmctl.repository import repo
from gmctl.commit import commit
from gmctl.ecs_deployment import ecs
from gmctl.lambda_deployment import faas
from gmctl.user import user
from gmctl.utils import print_table
from gmctl.db_functions import get_deployments
from gmctl.gmclient import GitmoxiClient
import os

@click.group()
@click.option('-e', '--endpoint-url', default="env(GITMOXI_ENDPOINT_URL), fallback to http://127.0.0.1:8080", help='The Gitmoxi FastAPI endpoint URL', show_default=True)
@click.option('-l', '--log-level', default="ERROR", type=click.Choice(["DEBUG","INFO","WARNING","ERROR","CRITICAL"], case_sensitive=False), help='The log level', show_default=True)
@click.pass_context
def cli(ctx, endpoint_url ,log_level):
    logging.getLogger().setLevel(getattr(logging, log_level.upper()))
    ctx.ensure_object(dict)
    endpoint_url = ctx.obj.get('ENDPOINT_URL', None)
    if not endpoint_url:
        endpoint_url = os.getenv('GITMOXI_ENDPOINT_URL', 'http://127.0.0.1:8080')
    ctx.obj['ENDPOINT_URL'] = endpoint_url

cli.add_command(commit)
cli.add_command(repo)


# Deployment group with subcommands
@cli.group()
@click.pass_context
def deployment(ctx):
    """User related commands."""
    pass

deployment.add_command(ecs)
deployment.add_command(faas)

@deployment.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.option('-c', '--commit-hash', help='The commit hash', required=True)
@click.pass_context
def get(ctx, repo_url, commit_hash):
    try:
        gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
        keys = {}
        keys["ecs"] = ["repo_url", "commit_hash", "account_id", "region", "service", 
                        "cluster", "create_timestamp", "status", "file_prefix"]
        keys["lambda"] = ["repo_url", "commit_hash", "account_id", "region", 
                          "function_name", "create_timestamp", "status", "file_prefix"]
        for service in ["ecs", "lambda"]:
            click.echo(f"{service.upper()} deployments for {repo_url} commit {commit_hash}:")
            conditions = {"repo_url": repo_url, "commit_hash": commit_hash}
            deployments = get_deployments(service, gmclient, conditions, 10)
            to_display = []
            for deployment in deployments:
                to_display.append({k: deployment.get(k) for k in keys[service]})
            print_table(to_display)
    except Exception as e:
        click.echo(f"Error: {e}")