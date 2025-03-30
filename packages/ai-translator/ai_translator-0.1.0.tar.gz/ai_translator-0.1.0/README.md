# AI Translator

[English](README.md) | [繁體中文](README_zh_TW.md)

An AI-powered translation tool that uses OpenAI's GPT models to translate text and files between different languages.

## Features

- Text translation
- File translation
- Folder translation
- Support for multiple languages
- Customizable language configuration
- JSON configuration support
- Support for different GPT model settings

## Installation

```bash
pip install ai-translator
```

## Usage

### Basic Text Translation

```python
from translator import Translator

translator = Translator(api_key="your-openai-api-key")

# Translate text
text = "Hello, world!"
result = translator.translate(text, target_language="zh-tw")
print(result)  # 你好，世界！
```

### Advanced Initialization Options

```python
# Using different models and parameters
translator = Translator(
    api_key="your-openai-api-key",
    model="gpt-4o-mini",  # Default model
    temperature=0.0,      # Controls creativity, 0 for most deterministic output
    max_tokens=1000       # Maximum output length
)

# View currently available languages
for code, name in translator.available_languages.items():
    print(f"{code}: {name}")
```

### File Translation

```python
# Translate a single file
translator.translate_file(
    file_path="input.txt",
    target_language="es",
    output_path="output.txt"
)

# Translate all files in a folder
translator.translate_folder(
    folder_path="input_folder",
    target_language="ja",
    output_dir="output_folder",
    file_extension=".txt",
    recursive=True  # Set to True to process subdirectories
)
```

### Custom Language Configuration

```python
# Using default configuration
translator = Translator(api_key="your-openai-api-key")

# Using custom configuration
custom_config = {
    "zh-tw": "繁體中文",
    "en": "English",
    "fr": "French"
}
translator = Translator(api_key="your-openai-api-key", language_config=custom_config)

# Update configuration of an existing instance (after initialization)
translator.config(
    model="gpt-4",
    temperature=0.3,
    max_tokens=2000,
    language_config=custom_config
)

# Update language configuration from JSON file
translator.update_language_config_from_json("languages.json")
```

## Configuration

### Default Supported Languages

- zh-tw: 繁體中文
- en: English
- es: Español 
- ja: 日本語
- ko: 한국어

### JSON Configuration File Format

```json
{
    "zh-tw": "繁體中文",
    "en": "English",
    "fr": "French",
    "de": "Deutsch"
}
```

## Error Handling

The translation functions include robust error handling mechanisms for the following situations:

- Files or directories don't exist
- JSON configuration file format errors
- API call failures
- File read/write errors

Error messages are printed via standard output, and translation methods return None when errors occur.

## Requirements

- Python 3.8 or higher
- OpenAI API key
- openai>=1.65.0
- python-dotenv>=1.0.0

## License

[MIT License](LICENSE) 