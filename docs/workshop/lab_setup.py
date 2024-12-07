#!/bin/env python

import rich_click as click
import subprocess
import os
from functools import wraps
from typing import List, Callable
from click import style

# Step registration
steps: List[tuple[Callable, str]] = []

def blue(text: str):
    return style(text, fg="blue")

def bold(text: str):
    return style(text, fg="bright_white", bold=True)

def step(label: str):

    """Decorator to register and label setup steps"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, step_number, total_steps, **kwargs):
            click.echo(f"\n{bold(f'Step {step_number}/{total_steps}')}: {blue(label)}")
            click.echo()
            return func(*args, **kwargs)
        steps.append((wrapper, label))
        return wrapper
    return decorator

@step("GitHub Authentication")
def github_auth(*, force: bool = False):
    """Authenticate with GitHub using the gh CLI tool"""
    # Only check authentication status if not forcing re-auth
    if not force:
        result = subprocess.run(['gh', 'auth', 'status'], 
                capture_output=True, 
                text=True, 
                check=False)
        if result.returncode == 0:
            click.echo("Already authenticated with GitHub")
            return

    # Proceed with authentication
    process = subprocess.Popen(
        ['gh', 'auth', 'login',
         '--hostname', 'github.com',
         '--git-protocol', 'https',
         '--web',
         '--scopes', 'workflow'],
        stdin=subprocess.PIPE,
        env={**os.environ, 'GITHUB_TOKEN': ''},
        text=True
    )
    process.communicate(input='Y\n')

@step("Fork GitHub Repository")
def fork_repository():
    """Fork the current repository using the gh CLI tool"""
    subprocess.run(['gh', 'repo', 'fork', '--remote'], check=True)

@step("Azure CLI Authentication")
def azure_login(*, username: str = None, password: str = None, tenant: str = None, force: bool = False):
    # Only check authentication status if not forcing re-auth
    if not force:
        result = subprocess.run(['az', 'account', 'show'], 
                              capture_output=True, 
                              text=True, 
                              check=False)
        if result.returncode == 0:
            click.echo("Already authenticated with Azure CLI")
            return

    # Proceed with login if not authenticated or force=True
    login_cmd = ['az', 'login']
    if username and password:
        login_cmd.extend(['-u', username, '-p', password])
    if tenant:
        login_cmd.extend(['--tenant', tenant])
    subprocess.run(login_cmd, check=True)

@step("Azure Developer CLI Authentication")
def azd_login(*, username: str = None, password: str = None, force: bool = False):
    """Authenticate with Azure Developer CLI using device code"""
    # Only check authentication status if not forcing re-auth
    if not force:
        result = subprocess.run(['azd', 'auth', 'status'], 
                              capture_output=True, 
                              text=True, 
                              check=False)
        if result.returncode == 0:
            click.echo("Already authenticated with Azure Developer CLI")
            return

    # Display credentials if provided
    if username and password:
        click.echo(f"Enter the following credentials to authenticate with Azure Developer CLI:")
        click.echo(f"Username: {username}")
        click.echo(f"Password: {password}")
        click.echo()
        click.echo(f"{style('IMPORTANT', fg='red', reverse=True)}: {style('Do not use your personal credentials for this step!', underline=True)}")

        # Wait for user to press Enter
        input("\nPress Enter to start the azd login process...")

    # Proceed with authentication
    subprocess.run([
        'azd', 'auth', 'login',
        '--use-device-code',
        '--no-prompt'
    ], check=True)

@step("Azure Developer CLI Environment Setup")
def create_azd_environment(*, azure_env_name: str, subscription: str):
    azd_cmd = [
        'azd', 'env', 'new', azure_env_name,
        '--location', 'canadaeast',
        '--subscription', subscription
    ]
    subprocess.run(azd_cmd, check=True)

@step("Refresh AZD Environment")
def refresh_environment(*, azure_env_name: str):
    subprocess.run([
        'azd', 'env', 'refresh',
        '-e', azure_env_name,
        '--no-prompt'
    ], check=True)

@step("Export Environment Variables")
def export_variables():
    with open('../../.env', 'w') as env_file:
        subprocess.run(['azd', 'env', 'get-values'], stdout=env_file, check=True)

@step("Run Roles Script")
def run_roles():
    subprocess.run(['../../infra/hooks/roles.sh'], check=True)

@step("Execute Postprovision Hook")
def run_postprovision(*, azure_env_name: str):
    process = subprocess.Popen(
        ['azd', 'hooks', 'run', 'postprovision', '-e', azure_env_name],
        stdin=subprocess.PIPE,
        text=True
    )
    process.communicate(input='1\n')

@click.command()
@click.option('--username', help='Azure username/email for authentication')
@click.option('--password', help='Azure password for authentication', hide_input=True)
@click.option('--azure-env-name', required=True, help='Name for the new Azure environment')
@click.option('--subscription', required=True, help='Azure subscription ID to use')
@click.option('--tenant', help='Optional Azure tenant ID for specific directory')
@click.option('--force', is_flag=True, help='Force re-authentication and re-provisioning')
def setup(username, password, azure_env_name, subscription, tenant, force):
    """
    Automates Azure environment setup and configuration.
    
    This command will:
    * Log into Azure CLI (interactive if no credentials provided)
    * Create a new AZD environment
    * Refresh the environment
    * Export environment variables
    * Run roles script
    * Execute postprovision hook
    """
    try:
        # Create parameters dictionary
        params = {
            'username': username,
            'password': password,
            'azure_env_name': azure_env_name,
            'subscription': subscription,
            'tenant': tenant,
            'force': force
        }
        
        # Execute all registered steps
        for index, entry in enumerate(steps):
            from inspect import signature
            step_func, _ = entry

            # Get the parameter names for this function
            sig = signature(step_func.__wrapped__)
            # Filter params to only include what the function needs
            step_params = {
                name: params[name] 
                for name in sig.parameters
                if name in params
            }
            # Execute step and merge any returned dict into params
            result = step_func(step_number=index + 1, total_steps=len(steps), **step_params)
            if isinstance(result, dict):
                params.update(result)
            
        click.echo("\nSetup completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()
