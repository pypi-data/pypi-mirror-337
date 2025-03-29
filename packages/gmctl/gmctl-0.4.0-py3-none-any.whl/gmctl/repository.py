from gmctl.gmclient import GitmoxiClient
import logging
logger = logging.getLogger(__name__)

import click
from gmctl.utils import print_table

# Repo group with subcommands
@click.group()
@click.pass_context 
def repo(ctx):
    """Repo related commands."""
    pass

@repo.command()
@click.option('-r', '--repo-url', required=True, help='The repository URL')
@click.option('-b', '--branches', required=True, help='The branches in the repository', multiple=True)
@click.option('-a', '--access-token-arn', required=True, help='The access token ARN')
@click.pass_context
def add(ctx, repo_url, branches, access_token_arn):
    payload = {"repo_url": repo_url, "branches": list(branches), "access_token_arn": access_token_arn}
    gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
    resource_path = "/repositories/add"
    add_response = gmclient.post(resource_path, payload)
    click.echo(f"Add response: {add_response}")

@repo.command()
@click.option('-r', '--repo-url', help='The repository URL')
@click.pass_context
def get(ctx, repo_url):
    try:
        resource_path = "/repositories"
        if repo_url:
            resource_path += f"?repo_url={repo_url}"
        logger.info(f'Getting repository: {resource_path}')
        gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
        # make a GET call to the /repository/get endpoint with the repository URL
        response = gmclient.get(resource_path)
        if not response:
            click.echo(f'Failed to get repositories for: {resource_path}')
        print_table(response)
    except Exception as e:
        click.echo(f"Error: {e}")

@repo.command()
@click.option('-r', '--repo-url', help='The repository URL', required=True)
@click.pass_context
def delete(ctx, repo_url):
    try:
        # make a DELETE call to the /repository/delete endpoint with the repository URL
        resource_path = f"/repositories/delete?repo_url={repo_url}"
        logger.info(f'Deleting repository: {resource_path}')
        gmclient = GitmoxiClient(ctx.obj['ENDPOINT_URL'])
        delete_response = gmclient.delete(resource_path)
        click.echo(f"Delete response: {delete_response}")
    except Exception as e:
        click.echo(f"Error: {e}")
