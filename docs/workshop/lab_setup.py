#!/bin/env python

import rich_click as click
import subprocess
import os
from functools import wraps
from typing import List, Callable

# Step registration
steps: List[tuple[Callable, str]] = []

def blue(text: str):
    return click.style(text, fg="blue")

def bold(text: str):
    return click.style(text, fg="bright_white", bold=True)

def step(label: str):
    """Decorator to register and label setup steps"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            step_number = len([s for s in steps if s[0] == func]) + 1
            click.echo(f"\n{bold(f'Step {step_number}')}: {blue(label)}")
            click.echo()
            return func(*args, **kwargs)
        steps.append((wrapper, label))
        return wrapper
    return decorator

@step("Azure CLI Authentication")
def azure_login(*, username: str, password: str, tenant: str = None):
    login_cmd = ['az', 'login', '-u', username, '-p', password]
    if tenant:
        login_cmd.extend(['--tenant', tenant])
    subprocess.run(login_cmd, check=True)

@step("Azure Developer CLI Environment Setup")
def create_azd_environment(*, azure_env_name: str, subscription: str, tenant: str = None):
    azd_cmd = [
        'azd', 'env', 'new', azure_env_name,
        '--location', 'canadaeast',
        '--subscription', subscription
    ]
    if tenant:
        azd_cmd.extend(['--tenant', tenant])
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
@click.option('--username', required=True, help='Azure username/email for authentication')
@click.option('--password', required=True, help='Azure password for authentication', hide_input=True)
@click.option('--azure-env-name', required=True, help='Name for the new Azure environment')
@click.option('--subscription', required=True, help='Azure subscription ID to use')
@click.option('--tenant', help='Optional Azure tenant ID for specific directory')
def setup(username, password, azure_env_name, subscription, tenant):
    """
    Automates Azure environment setup and configuration.
    
    This command will:
    * Log into Azure CLI
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
            'tenant': tenant
        }
        
        # Execute all registered steps
        for step_func, _ in steps:
            # Get the parameter names for this function
            from inspect import signature
            sig = signature(step_func.__wrapped__)
            # Filter params to only include what the function needs
            step_params = {
                name: params[name] 
                for name in sig.parameters
                if name in params
            }
            # Execute step and merge any returned dict into params
            result = step_func(**step_params)
            if isinstance(result, dict):
                params.update(result)
            
        click.echo("\nSetup completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()

