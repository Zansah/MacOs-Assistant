import sys
from pathlib import Path
from april.config import ConfigManager
from april.utils.logger import setup_logger, get_logger


def main() -> int:
    """Run the April application."""
    config_manager = ConfigManager()
    config = config_manager.get()
    
    log_file = Path(config.log_file).expanduser()
    setup_logger(
        name="april",
        log_level=config.log_level,
        log_file=log_file,
    )
    logger = get_logger()
    
    logger.info("=" * 60)
    logger.info("April — macOS Voice Assistant")
    logger.info(f"Version 0.1.0")
    logger.info("=" * 60)
    
    logger.debug(f"Configuration loaded from: {config_manager.config_path}")
    logger.debug(f"Wake words: {config.wake_words}")
    logger.debug(f"Debug mode: {config.debug_mode}")
    logger.debug(f"Vault path: {config.vault_path}")
    logger.debug(f"Log file: {log_file}")
    
    print("\nApril — macOS Voice Assistant")
    print("Version 0.1.0")
    print(f"Configuration loaded from: {config_manager.config_path}")
    print(f"Wake words: {config.wake_words}")
    print(f"Debug mode: {config.debug_mode}")
    print(f"Vault path: {config.vault_path}")
    
    logger.info("April is ready.")
    print("\nApril is ready.")
    print("(Listening for wake words...)")
    print("Press Ctrl+C to exit.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())