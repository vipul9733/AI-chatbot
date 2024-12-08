import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class for the restaurant chatbot application.
    Loads and validates required environment variables and configuration settings.
    """
    # OpenAI API configuration
    OPENAI_API_KEY = os.getenv('YOUR_API_KEY')

    # Database configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'restaurant.db')  

    # Application configuration
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'  
    MENU_CATEGORIES = os.getenv('MENU_CATEGORIES', 'Pizza,Salad,Dessert,Beverages').split(',')

    # RAG configuration
    TRAINING_DATA_PATH = os.getenv('TRAINING_DATA_PATH', 'data/training_data.txt')

    @staticmethod
    def validate():
        """
        Validate that all required configurations are set.
        Raises:
            ValueError: If any required configuration is missing.
        """
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set. Please configure it in the .env file.")
        if not os.path.exists(Config.DATABASE_PATH):
            raise ValueError(f"Database file not found at {Config.DATABASE_PATH}. Please check the path.")
        if not os.path.exists(Config.TRAINING_DATA_PATH):
            raise ValueError(f"Training data file not found at {Config.TRAINING_DATA_PATH}. Please check the path.")

# Call validate to ensure the configuration is correct at startup
Config.validate()
