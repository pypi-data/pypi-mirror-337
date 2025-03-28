import os, uuid, json, subprocess
from gru.utils.constants import TOKEN_ENV_VAR_NAME
from gru.schema.api_response_handler import ApiError


class BaseCommand:

    def read_token(self) -> str:
        """
        Reads the GRU token from environment variables.

        Returns:
            str: The GRU authentication token

        Raises:
            ValueError: If the environment variable is not set
        """
        auth_token = os.getenv(TOKEN_ENV_VAR_NAME)
        if auth_token is None:
            raise ValueError(f"Environment variable {TOKEN_ENV_VAR_NAME} missing")
        return auth_token

    def create_correlation_id(self) -> str:
        """
        Creates a unique correlation ID for tracking API calls.

        Returns:
            str: A UUID string
        """
        return str(uuid.uuid4())

    def execute_operation(
        self, operation_func, *args, skip_correlation_id=False, **kwargs
    ):
        """
        Executes an operation with standardized error handling.

        Args:
            operation_func: The function to execute
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function

        Returns:
            The result of the function or an error message
        """
        correlation_id = self.create_correlation_id()
        file_path = kwargs.pop("file_path", {})
        try:
            auth_token = self.read_token()
            if skip_correlation_id:
                return operation_func(*args, **kwargs)
            else:
                return operation_func(correlation_id, auth_token, *args, **kwargs)
        except FileNotFoundError:
            return f"Error: {file_path} file not found."
        except json.JSONDecodeError as e:
            return f"JSON error: {str(e)}"
        except ApiError as e:
            return f"API error: {e.message}"
        except ValueError as value_error:
            return str(value_error)
        except subprocess.CalledProcessError as value_error:
            return str(value_error)
        except Exception:
            return f"An unexpected error occurred. Correlation ID: {correlation_id}"
