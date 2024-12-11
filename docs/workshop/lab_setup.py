#!/usr/bin/env python

import rich_click as click
import subprocess
import os
from functools import wraps
from typing import List, Callable
from click import style
from pathlib import Path
from inspect import signature

# Add these constants near the top
TEMP_FILE = Path.home() / '.lab_setup_progress'

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
    # Check if upstream remote already exists
    result = subprocess.run(['git', 'remote', 'get-url', 'upstream'], 
                capture_output=True, 
                text=True, 
                check=False)
    if result.returncode == 0:
        click.echo("Repository already has an upstream remote")
        return

    # Proceed with fork if no upstream remote exists
    process = subprocess.Popen(
        ['gh', 'repo', 'fork', '--remote'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        env={**os.environ, 'GITHUB_TOKEN': ''},
        text=True
    )
    out, err = process.communicate()
    print(out)

@step("Fetch Origin")
def fetch_origin():
    """
    Fetch the latest changes from origin.

    Necessary because after forking repository, main is still tracking upstream and origin has not been fetched.
    """
    subprocess.run(['git', 'fetch', 'origin'], check=True)

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
def azd_login(*, username: str = None, password: str = None, tenant: str = None, force: bool = False):
    """Authenticate with Azure Developer CLI using device code"""

    # Display credentials if provided
    if username and password:
        opts = {'underline': True}
        click.echo(f"{style('When asked to ', **opts)}{style('Pick an account', **opts, bold=True)}{style(', hit the ', **opts)}{style('Use another account', **opts, bold=True)}{style(' button and enter the following:', **opts)}")
        click.echo(f"Username: {style(username, fg='blue', bold=True)}")
        click.echo(f"Password: {style(password, fg='blue', bold=True)}")
        click.echo()
        click.echo(f"{style('IMPORTANT', fg='red', reverse=True)}: {style('DO NOT use your personal credentials for this step!', fg='red', underline=True)}")
        click.echo()

    # Proceed with authentication
    login_cmd = ['azd', 'auth', 'login', '--use-device-code', '--no-prompt']
    if tenant:
        login_cmd.extend(['--tenant-id', tenant])
    subprocess.run(login_cmd, check=True)

@step("Azure Developer CLI Environment Setup")
def create_azd_environment(*, azure_env_name: str, subscription: str):
    # Check if environment already exists
    result = subprocess.run(
        ['azd', 'env', 'list'], 
        capture_output=True, 
        text=True, 
        check=True
    )
    
    if azure_env_name in result.stdout:
        click.echo(f"Environment '{azure_env_name}' already exists")
        return
        
    # Create new environment if it doesn't exist
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
    # Get the directory where the script is located and resolve .env path
    env_path = Path(__file__).parent.parent.parent / '.env'
    
    with open(env_path, 'w') as env_file:
        subprocess.run(['azd', 'env', 'get-values'], stdout=env_file, check=True)

@step("Run Roles Script")
def run_roles():
    # Get the directory where the script is located
    script_dir = Path(__file__).parent
    roles_script = script_dir.parent.parent / 'infra' / 'hooks' / 'roles.sh'
    subprocess.run(['bash', str(roles_script)], check=True)

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
@click.option('--tenant', help='Azure tenant ID')
@click.option('--force', is_flag=True, help='Force re-authentication and start from beginning')
@click.option('--step', type=int, help='Resume from a specific step number (1-based)')
def setup(username, password, azure_env_name, subscription, tenant, force, step):
    """
    Automates Azure environment setup and configuration.
    
    This command will:
    1. GitHub Authentication
    2. Fork GitHub Repository
    3. Azure CLI Authentication
    4. Azure Developer CLI Authentication
    5. Azure Developer CLI Environment Setup
    6. Refresh AZD Environment
    7. Export Environment Variables
    8. Run Roles Script
    9. Execute Postprovision Hook
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
        
        # Determine starting step
        start_step = 0
        if step is not None:
            if not 1 <= step <= len(steps):
                raise click.BadParameter(f"Step must be between 1 and {len(steps)}")
            start_step = step - 1
        elif not force and TEMP_FILE.exists():
            start_step = int(TEMP_FILE.read_text().strip())
            if start_step >= len(steps):
                click.echo("\nAll steps were already successfully executed!")
                click.echo("Use --force to execute all steps from the beginning if needed.")
                return
            click.echo(f"\nResuming from step {blue(start_step + 1)}")
        
        # Execute all registered steps
        for index, entry in enumerate(steps):
            from inspect import signature
            # Skip steps that were already completed
            if index < start_step:
                continue
                
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
            
            # Save progress after each successful step
            TEMP_FILE.write_text(str(index + 1))
            
        # Clean up temp file on successful completion
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()
            
        click.echo("\nSetup completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()
