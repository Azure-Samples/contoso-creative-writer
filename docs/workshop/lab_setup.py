#!/bin/env python

import rich_click as click
import subprocess
import os

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
        # Azure CLI login
        click.echo("Logging into Azure CLI...")
        login_cmd = ['az', 'login', '-u', username, '-p', password]
        if tenant:
            login_cmd.extend(['--tenant', tenant])
        subprocess.run(login_cmd, check=True)

        # Azure Developer CLI environment setup
        click.echo("Creating new AZD environment...")
        azd_cmd = [
            'azd', 'env', 'new', azure_env_name,
            '--location', 'canadaeast',
            '--subscription', subscription
        ]
        if tenant:
            azd_cmd.extend(['--tenant', tenant])
        subprocess.run(azd_cmd, check=True)

        # Refresh AZD environment
        click.echo("Refreshing AZD environment...")
        subprocess.run([
            'azd', 'env', 'refresh',
            '-e', azure_env_name,
            '--no-prompt'
        ], check=True)

        # Export environment variables
        click.echo("Exporting environment variables...")
        with open('../../.env', 'w') as env_file:
            subprocess.run(['azd', 'env', 'get-values'], stdout=env_file, check=True)

        # Run roles script
        click.echo("Running roles script...")
        subprocess.run(['../../infra/hooks/roles.sh'], check=True)

        # Run postprovision hook
        click.echo("Running postprovision hook...")
        process = subprocess.Popen(['azd', 'hooks', 'run', 'postprovision', '-e', azure_env_name],
                                stdin=subprocess.PIPE,
                                text=True)
        process.communicate(input='1\n')
        
        click.echo("Setup completed successfully!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error during setup: {str(e)}", err=True)
        raise click.Abort()

if __name__ == '__main__':
    setup()

