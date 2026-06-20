import sys
from pathlib import Path
from april.config import ConfigManager


def main() -> int:
    """Run the April application."""
    print("April — macOS Voice Assistant")
    print("Version 0.1.0")
    
    # Load configuration
    config_manager = ConfigManager()
    config = config_manager.get()
    
    print(f"Configuration loaded from: {config_manager.config_path}")
    print(f"Wake words: {config.wake_words}")
    print(f"Debug mode: {config.debug_mode}")
    print(f"Vault path: {config.vault_path}")
    
    print("\nApril is ready.")
    print("Listening for wake words...)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())