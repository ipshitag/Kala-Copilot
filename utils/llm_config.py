import os

config_list = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": os.environ.get("AZURE_OPENAI_KEY"),
            "api_type": "azure",
            "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"),
            "api_version": "2025-01-01-preview",
        },
    ],
    "temperature": 0.5,
    "timeout": 1000,
}