#!/bin/env python

import rich_click as click
import subprocess
import os
from functools import wraps
from typing import List, Callable

# Rich-click configuration remains the same...

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

class SetupContext:
    """Context object to hold setup parameters"""
    def __init__(self, username, password, azure_env_name, subscription, tenant):
        self.username = username
        self.password = password
        self.azure_env_name = azure_env_name
        self.subscription = subscription
        self.tenant = tenant

@step("Azure CLI Authentication")
def azure_login(ctx: SetupContext):
    login_cmd = ['az', 'login', '-u', ctx.username, '-p', ctx.password]
    if ctx.tenant:
        login_cmd.extend(['--tenant', ctx.tenant])
    subprocess.run(login_cmd, check=True)

@step("Azure Developer CLI Environment Setup")
def create_azd_environment(ctx: SetupContext):
    azd_cmd = [
        'azd', 'env', 'new', ctx.azure_env_name,
        '--location', 'canadaeast',
        '--subscription', ctx.subscription
    ]
    if ctx.tenant:
        azd_cmd.extend(['--tenant', ctx.tenant])
    subprocess.run(azd_cmd, check=True)

@step("Refresh AZD Environment")
def refresh_environment(ctx: SetupContext):
    subprocess.run([
        'azd', 'env', 'refresh',
        '-e', ctx.azure_env_name,
        '--no-prompt'
    ], check=True)

@step("Export Environment Variables")
def export_variables(ctx: SetupContext):
    with open('../../.env', 'w') as env_file:
        subprocess.run(['azd', 'env', 'get-values'], stdout=env_file, check=True)

@step("Run Roles Script")
def run_roles(ctx: SetupContext):
    subprocess.run(['../../infra/hooks/roles.sh'], check=True)

@step("Execute Postprovision Hook")
def run_postprovision(ctx: SetupContext):
    process = subprocess.Popen(
        ['azd', 'hooks', 'run', 'postprovision', '-e', ctx.azure_env_name],
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
        ctx = SetupContext(username, password, azure_env_name, subscription, tenant)
        
        # Execute all registered steps
        for step_func, _ in steps:
            step_func(ctx)
            
        click.echo("\nSetup completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()

