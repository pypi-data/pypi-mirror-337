from functools import wraps
from .config import ConfigManager, parse_cli_args
from .exceptions import ConfigurationError
from .service_locator import ServiceLocator
from ..ml.mlflow_integration import initialize
from datetime import datetime
import mlflow


def sais_foundation(cls):
    parse_cli_args("Override configuration values")
    config = ConfigManager().config

    for section in ["foundation", "unified_data_access", "ml"]:
        if hasattr(config, section):
            setattr(cls, f"_{section}_config", getattr(config, section))

    if not config.foundation.experiment_name:
        raise ConfigurationError(
            "Experiment name is required in foundation config")

    if config.ml.enabled:
        ml = _init_mlflow_integration(cls)
        if hasattr(cls, 'run'):
            original_run = cls.run

            @wraps(original_run)
            def wrapped_run(self, *args, **kwargs):
                mlflow.config.enable_async_logging(True)
                version = datetime.now().strftime("%Y%m%d_%H%M%S")
                run_name = f"{cls.__name__}-v{version}"
                with mlflow.start_run(run_name=run_name, description=cls._foundation_config.experiment_description):
                    try:
                        # Log parameters only once at the beginning of the run
                        params_dict = {}
                        try:
                            params_dict = ConfigManager()._convert_namespace_to_dict(
                                cls._ml_config.parameters)
                            ml.log_params(params_dict)
                        except (AttributeError, ValueError) as e:
                            print(f"Warning: Could not convert parameters: {e}")
                            
                        # Log model repo information if available
                        try:
                            model_repo_dict = ConfigManager()._convert_namespace_to_dict(
                                cls._ml_config.model_repo)
                            if model_repo_dict:
                                ml.log_model(model_repo_dict)
                        except (AttributeError, ValueError) as e:
                            print(f"Warning: Could not convert model repo: {e}")
                            
                        # Execute the original run function
                        result = original_run(self, *args, **kwargs)
                        return result
                    except Exception as e:
                        ml.log_params({"error": str(e)})
                        raise
            cls.run = wrapped_run

    if config.unified_data_access.enabled:
        _init_data_access_client(cls)

    return cls


def _init_mlflow_integration(cls):
    from ..ml import mlflow_integration

    ml_instance = mlflow_integration.initialize(
        experiment_name=cls._foundation_config.experiment_name, 
        experiment_description=cls._foundation_config.experiment_description,
        config=cls._ml_config, mlflow=mlflow)
    ServiceLocator.set_ml_manager(ml_instance)
    return ml_instance


def _init_data_access_client(cls):
    from ..unified_data_access import client

    data_client = client.initialize(
        **vars(cls._unified_data_access_config)
    )
    ServiceLocator.set_data_client(data_client)
    return data_client
