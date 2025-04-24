import yaml

_config = None  # Private module-level variable

def load_config(config_file):
    """Loads the configuration from the specified YAML file."""
    global _config
    
    with open(config_file, 'r') as f:
        _config = yaml.safe_load(f)
        
    return _config

def get_config():
    """Returns the loaded configuration."""
    global _config
    if _config is None:
        raise ValueError("Configuration has not been loaded yet.  Call load_config() first.")
    return _config