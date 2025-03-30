import json
import os
from typing import Callable, Dict, Optional, Union

import openai

# Default language configuration
DEFAULT_LANGUAGE_CONFIG: Dict[str, str] = {
    "zh-tw": "繁體中文",
    "en": "English",
    "es": "Español",
    "ja": "日本語",
    "ko": "한국어",
}


class Translator:
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        temperature: float = 0.0,
        max_tokens: int = 1000,
        language_config: Optional[Union[Dict[str, str], str]] = None,
    ):
        """
        Initialize the Translator class with OpenAI API key and configuration.
        Uses the config() method to set up translation parameters.

        Parameters:
            api_key (str): OpenAI API key for authentication
            model (str): See config() method, defaults to "gpt-4o-mini"
            temperature (float): See config() method, defaults to 0.0
            max_tokens (int): See config() method, defaults to 1000
            language_config (Optional[Union[Dict[str, str], str]]): See config() method, defaults to DEFAULT_LANGUAGE_CONFIG
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.config(model, temperature, max_tokens, language_config)

    @property
    def available_languages(self) -> Dict[str, str]:
        """
        Return the current language configuration.

        Returns:
            Dict[str, str]: Dictionary mapping language codes to language names
        """
        return self.language_dict.copy()

    def config(
        self,
        model: str,
        temperature: float,
        max_tokens: int,
        language_config: Optional[Union[Dict[str, str], str]],
    ):
        """
        Configure the translation settings.

        Parameters:
            model (str): The OpenAI model to use for translation
            temperature (float): Controls randomness in generation (0.0 to 1.0)
            max_tokens (int): Maximum number of tokens to generate
            language_config (Optional[Union[Dict[str, str], str]]): Language configuration
                as dictionary or path to JSON file

        Raises:
            FileNotFoundError: If language_config is a file path that doesn't exist
            json.JSONDecodeError: If language_config file contains invalid JSON
            ValueError: If language_config has invalid format
        """
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        if isinstance(language_config, str):
            if not self.update_language_config_from_json(language_config):
                print(
                    "You're trying to load a language config from a json file, but something went wrong. Using default language config instead."
                )
                self.language_dict = DEFAULT_LANGUAGE_CONFIG
        else:
            self.language_dict = language_config or DEFAULT_LANGUAGE_CONFIG

    def get_lang(self, lang: str) -> str:
        """
        Retrieve the language name from the dictionary or return the input if not found.

        Parameters:
            lang (str): Language code to look up

        Returns:
            str: Full language name if found in dictionary, original input otherwise
        """
        if lang.lower() in self.language_dict:
            return self.language_dict.get(lang.lower(), lang)
        return lang

    def gen_prompt(self) -> Callable[[str, str], str]:
        """
        Generate a lambda function for creating translation prompts.

        Returns:
            Callable[[str, str], str]: A function that takes text and target language
                and returns a formatted prompt for the translation model
        """
        return (
            lambda text, target_lang: f"Translate the following text into {self.get_lang(target_lang)}. Provide only the translated text, without any additional explanation or commentary.\n\nText to translate:\n```\n{text}\n```"
        )

    def translate(self, text: str, target_language: str = "zh-tw") -> Optional[str]:
        """
        Translate the input text into the target language.

        Parameters:
            text (str): The text to translate
            target_language (str): The target language code, defaults to "zh-tw" (Traditional Chinese)

        Returns:
            Optional[str]: The translated text, or None if translation fails

        Raises:
            Exception: If any error occurs during the API call or translation process
        """
        try:
            prompt_generator = self.gen_prompt()
            prompt = prompt_generator(text, target_language)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt_generator("hello", "zh-tw")},
                    {"role": "assistant", "content": "你好"},
                    {"role": "user", "content": prompt_generator("goodbye", "es")},
                    {"role": "assistant", "content": "adiós"},
                    {"role": "user", "content": prompt_generator("今天天氣真好", "en")},
                    {
                        "role": "assistant",
                        "content": "The weather is really nice today.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            translated_text = response.choices[0].message.content.strip()
            return translated_text

        except Exception as e:
            print(f"Translation failed: {str(e)}")
            return None

    def translate_file(
        self, file_path: str, target_language: str, output_path: Optional[str] = None
    ) -> None:
        """
        Translate a specified file.

        Parameters:
            file_path (str): Path to the file to be translated
            target_language (str): Target language code for translation
            output_path (Optional[str]): Path to save the translated file, defaults to overwriting the original

        Raises:
            FileNotFoundError: If the specified file doesn't exist
            Exception: If any error occurs during translation or file operations
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            translated = self.translate(content, target_language)
            if translated:
                output_path = output_path or file_path
                output_dir = os.path.dirname(output_path)
                if output_dir:
                    os.makedirs(output_dir, exist_ok=True)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(translated)
                print(f"Translation completed: {file_path} -> {output_path}")
        except Exception as e:
            print(f"File translation failed: {file_path}, Error: {str(e)}")

    def translate_folder(
        self,
        folder_path: str,
        target_language: str,
        output_dir: Optional[str] = None,
        file_extension: str = ".txt",
        recursive: bool = False,
    ) -> None:
        """
        Translate files within a folder.

        Parameters:
            folder_path (str): Path to the folder containing files to translate
            target_language (str): Target language code for translation
            output_dir (Optional[str]): Directory to save translated files, defaults to None (overwrite originals)
            file_extension (str): File extension filter for translation, defaults to ".txt"
            recursive (bool): Whether to process subfolders recursively, defaults to False

        Raises:
            NotADirectoryError: If the specified folder doesn't exist
            Exception: If any error occurs during the translation process
        """
        try:
            if not os.path.isdir(folder_path):
                raise NotADirectoryError(f"Folder not found: {folder_path}")

            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith(file_extension):
                        file_path = os.path.join(root, file)
                        output_path = file_path
                        if output_dir:
                            rel_path = os.path.relpath(file_path, folder_path)
                            output_path = os.path.join(output_dir, rel_path)
                            os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        self.translate_file(file_path, target_language, output_path)
                if not recursive:
                    break
            print(f"Folder translation completed: {folder_path}")
        except Exception as e:
            print(f"Folder translation failed: {folder_path}, Error: {str(e)}")

    def update_language_config_from_json(self, json_file_path: str) -> bool:
        """
        Update language configuration from a JSON file.

        Parameters:
            json_file_path (str): Path to the JSON configuration file

        Returns:
            bool: Whether the update was successful

        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the JSON format is invalid
            ValueError: If the configuration format is incorrect
        """
        try:
            if not os.path.exists(json_file_path):
                raise FileNotFoundError(
                    f"Configuration file not found: {json_file_path}"
                )

            with open(json_file_path, "r", encoding="utf-8") as f:
                config = json.load(f)

            if not isinstance(config, dict):
                raise ValueError("Configuration must be a dictionary")

            for key, value in config.items():
                if not isinstance(value, str):
                    raise ValueError(
                        f"Value for language code '{key}' must be a string"
                    )

            self.language_dict.update(config)
            return True

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            return False
        except Exception as e:
            print(f"Error updating language configuration: {str(e)}")
            return False
