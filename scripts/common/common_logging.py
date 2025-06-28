import logging

#####################
# Log
#####################

# --- Logging Setup (EARLY) ---
LOG_FORMAT = '[%(asctime)s] [%(levelname)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S (%Z)'

logging.basicConfig(  # Basic config ASAP (for fallback)
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[logging.StreamHandler()]  # Only console for now
)

def print_command(subprocess_command: list):  # 🚀 Used for subprocess command execution
    command = ' '.join(subprocess_command)
    logging.info(f"🚀  {command}")

def print_info(message: str):
    logging.info(f"ℹ️  {message}")

def print_error(message: str):
    logging.error(f"❌  {message}")

def print_success(message: str):
    logging.info(f"✅  {message}")

def print_warning(message: str):
    logging.warning(f"⚠️  {message}")

def print_debug(message: str):
    logging.debug(f"🐞  {message}")

def print_execution(message: str):
    print_headline(message)

def print_headline(message: str):
    emoji = "🔧"
    formatted_message = f"{emoji} {message} {emoji}"
    separator = "=" * (len(formatted_message) + 4)
    
    logging.info(separator)
    logging.info(f"| {formatted_message} |")
    logging.info(separator)