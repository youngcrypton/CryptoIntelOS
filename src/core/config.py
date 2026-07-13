from dotenv import load_dotenv

def load_configuration():
    """Load environment variables from the .env file."""
    load_dotenv()
    print("✓ Configuration loaded")