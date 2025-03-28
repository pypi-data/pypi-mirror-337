import os
import fire
from gru._cli import BaseCommand
from gru.agents.apis import (
    AGENT_CONFIG_FILE_NAME,
    ai_agent_templates_setup,
    converse_agent,
    delete_agent,
    deploy_agent,
    read_prompt_file,
    register_agent,
    update_agent,
)
from gru.agents.apis import prompt_agent
from gru.components.apis import setup as component_setup


class ComponentCommands(BaseCommand):
    """Commands for managing components"""

    def setup(self, cluster_name: str, config_file: str):
        """
        Set up components based on configuration.

        Args:
            cluster_name (str): Name of the cluster
            config_file (str): Path to the configuration file

        Returns:
            str: Result of the setup operation
        """
        return self.execute_operation(
            component_setup, cluster_name, config_file, file_path=config_file
        )


class AgentCommands(BaseCommand):
    def create_bootstrap(self):
        """
        Create a bootstrap project for an AI agent.

        Returns:
            str: Success or error message
        """
        return self.execute_operation(
            ai_agent_templates_setup, skip_correlation_id=True
        )

    def register(self, agent_folder, cluster_name, image, image_pull_secret):
        """
        Register an agent with the system.

        Args:
            agent_folder: Folder containing agent configuration
            cluster_name: Name of the cluster
            image: Docker image for the agent
            image_pull_secret: Secret for pulling the image

        Returns:
            str: Result of the registration
        """
        config_path = os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)
        return self.execute_operation(
            register_agent,
            agent_folder,
            cluster_name,
            image,
            image_pull_secret,
            file_path=config_path,
        )

    def deploy(self, agent_name):
        """
        Deploy an agent to the system.

        Args:
            agent_name: Name of the agent to deploy

        Returns:
            str: Result of the deployment
        """
        return self.execute_operation(deploy_agent, agent_name)

    def update(self, agent_folder, image=None, image_pull_secret=None):
        """
        Update an existing agent.

        Args:
            agent_folder: Folder containing agent configuration
            image: Docker image for the agent (optional)
            image_pull_secret: Secret for pulling the image (optional)

        Returns:
            str: Result of the update
        """
        config_path = os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)
        return self.execute_operation(
            update_agent, agent_folder, image, image_pull_secret, file_path=config_path
        )

    def delete(self, agent_name: str):
        """
        Delete an agent from the system.

        Args:
            agent_name: Name of the agent to delete

        Returns:
            str: Result of the deletion
        """
        return self.execute_operation(delete_agent, agent_name)

    def prompt(self, agent_name: str, prompt_file: str) -> str:
        """
        Send a prompt to a deployed agent.

        Args:
            agent_name (str): Name of the deployed agent
            prompt_file (str): Path to JSON file containing the prompt

        Returns:
            str: Success or error message
        """
        prompt_data = read_prompt_file(prompt_file)
        return self.execute_operation(
            prompt_agent, agent_name, prompt_data, file_path=prompt_file
        )

    def converse(self, agent_name: str, conversation_id: str | None = None):
        """
        Start or continue a conversation with an agent.

        Args:
            agent_name: Name of the agent
            conversation_id: ID of an existing conversation (optional)

        Returns:
            str: Result of the conversation
        """
        return self.execute_operation(converse_agent, agent_name, conversation_id)


class GruCommands(object):
    def __init__(self):
        self.component = ComponentCommands()
        self.agent = AgentCommands()


def main():
    fire.Fire(GruCommands)
