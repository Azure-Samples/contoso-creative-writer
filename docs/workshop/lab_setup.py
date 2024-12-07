#!/bin/env python

import click
import subprocess
import os

@click.command()
@click.option('--username', required=True, help='Azure username/email')
@click.option('--password', required=True, help='Azure password')
@click.option('--azure-env-name', required=True, help='Azure environment name')
@click.option('--subscription', required=True, help='Azure subscription ID')
def setup(username, password, azure_env_name, subscription):
    """Automates Azure environment setup and configuration."""
    try:
        # Azure CLI login
        click.echo("Logging into Azure CLI...")
        subprocess.run(['az', 'login', '-u', username, '-p', password], check=True)

        # Azure Developer CLI environment setup
        click.echo("Creating new AZD environment...")
        subprocess.run([
            'azd', 'env', 'new', azure_env_name,
            '--location', 'canadaeast',
            '--subscription', subscription
        ], check=True)

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

