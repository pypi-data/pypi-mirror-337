# Plugin System

The CVInsight tool uses a flexible plugin-based architecture that allows you to extend its functionality by creating custom plugins. This guide explains the plugin system and how to create your own plugins.

## Plugin Architecture Overview

### Core Components

1. **Plugin Manager**
   - Discovers and loads plugins
   - Manages plugin lifecycle
   - Handles plugin dependencies

2. **Base Plugin**
   - Abstract base class for all plugins
   - Defines common interface
   - Provides utility methods

3. **Plugin Resume Processor**
   - Coordinates plugin execution
   - Manages concurrent processing
   - Handles results aggregation

### Built-in Plugins

The system includes several built-in plugins:

1. **ProfileExtractorPlugin**
   - Extracts basic information
   - Name, contact details, email

2. **SkillsExtractorPlugin**
   - Identifies skills from resume
   - Technical and soft skills

3. **EducationExtractorPlugin**
   - Extracts educational history
   - Institutions, degrees, dates

4. **ExperienceExtractorPlugin**
   - Analyzes work experience
   - Companies, roles, dates

5. **YoeExtractorPlugin**
   - Calculates years of experience
   - Total professional experience

### Plugin Types
The system supports multiple types of plugins:
- **Extractor Plugins**: Implement the `ExtractorPlugin` interface to extract specific information from resumes
- **Custom Plugins**: Implement the `BasePlugin` interface for custom functionality
- **Processor Plugins**: Implement post-processing or analysis on extracted data

### Plugin Categories
Plugins are classified into different categories:

- **BASE**: Core functionality plugins (included in the base_plugins directory)
- **EXTRACTOR**: Plugins that extract information from resume text
- **PROCESSOR**: Plugins that process data after extraction
- **ANALYZER**: Plugins that analyze extracted data
- **CUSTOM**: User-created plugins for specific needs
- **UTILITY**: Helper plugins for various operations

## Creating Custom Plugins

### Plugin Structure

A basic plugin structure looks like this:

```python
from base_plugins.base import BasePlugin

class CustomPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "CustomPlugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Description of what this plugin does"

    @property
    def category(self) -> str:
        return "custom"

    def get_model(self) -> str:
        return "gemini-2.0-flash"

    def get_prompt_template(self) -> str:
        return """
        Extract {category} information from the following resume text:

        {resume_text}

        Return the information in the following JSON format:
        {
            "key1": "value1",
            "key2": ["value2", "value3"]
        }
        """

    def process_output(self, output: str) -> dict:
        # Process the LLM output and return structured data
        return self.parse_json(output)
```

### Required Methods

Every plugin must implement these methods:

1. **name**
   - Returns unique plugin name
   - Used for identification and logging

2. **version**
   - Returns plugin version
   - Helps with compatibility tracking

3. **description**
   - Returns plugin description
   - Used in documentation and UI

4. **category**
   - Returns plugin category
   - Groups related plugins

5. **get_model**
   - Returns LLM model name
   - Specifies which model to use

6. **get_prompt_template**
   - Returns prompt template
   - Defines how to query the LLM

7. **process_output**
   - Processes LLM output
   - Returns structured data

### Using a Data Model

If your plugin extracts structured data, define a Pydantic model for it:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

class YourCustomDataModel(BaseModel):
    """Model for your custom data"""
    main_field: str = Field(..., description="Primary data extracted by the plugin")
    secondary_field: Optional[List[str]] = Field(default_factory=list,
                                               description="Secondary data extracted")
```

### Best Practices

1. **Plugin Design**
   - Keep plugins focused and single-purpose
   - Use clear, descriptive names
   - Document all methods and parameters

2. **Error Handling**
   - Implement robust error handling
   - Validate LLM outputs
   - Provide meaningful error messages

3. **Performance**
   - Optimize prompt templates
   - Minimize token usage
   - Handle large inputs efficiently

4. **Testing**
   - Write unit tests
   - Test with various inputs
   - Verify output formats

## Plugin Development Guide

### 1. Create Plugin File

Create a new Python file in the `custom_plugins` directory:

```python
# custom_plugins/custom_extractor.py
from base_plugins.base import BasePlugin

class CustomExtractorPlugin(BasePlugin):
    # Implement required methods
    pass
```

### 2. Register Plugin

Add your plugin to `custom_plugins/__init__.py`:

```python
from .custom_extractor import CustomExtractorPlugin

__all__ = ['CustomExtractorPlugin']
```

### 3. Test Plugin

Create tests in `tests/test_custom_extractor.py`:

```python
import unittest
from custom_plugins.custom_extractor import CustomExtractorPlugin

class TestCustomExtractor(unittest.TestCase):
    def setUp(self):
        self.plugin = CustomExtractorPlugin()

    def test_plugin_initialization(self):
        self.assertEqual(self.plugin.name, "CustomExtractorPlugin")
        self.assertEqual(self.plugin.version, "1.0.0")

    def test_plugin_processing(self):
        # Test plugin processing
        pass

if __name__ == '__main__':
    unittest.main()
```

## Plugin Examples

### 1. Skills Extractor Plugin

```python
from base_plugins.base import BasePlugin

class SkillsExtractorPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "SkillsExtractorPlugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Extracts skills from resume text"

    @property
    def category(self) -> str:
        return "skills"

    def get_model(self) -> str:
        return "gemini-2.0-flash"

    def get_prompt_template(self) -> str:
        return """
        Extract skills from the following resume text.
        Include both technical and soft skills.

        Resume text:
        {resume_text}

        Return a JSON array of skills:
        ["skill1", "skill2", ...]
        """

    def process_output(self, output: str) -> dict:
        skills = self.parse_json(output)
        return {"skills": skills}
```

### 2. Experience Extractor Plugin

```python
from base_plugins.base import BasePlugin

class ExperienceExtractorPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

    @property
    def name(self) -> str:
        return "ExperienceExtractorPlugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Extracts work experience from resume"

    @property
    def category(self) -> str:
        return "experience"

    def get_model(self) -> str:
        return "gemini-2.0-flash"

    def get_prompt_template(self) -> str:
        return """
        Extract work experience from the resume text.
        For each position, include:
        - Company name
        - Role/title
        - Start date
        - End date
        - Location

        Resume text:
        {resume_text}

        Return a JSON array of experiences:
        [
            {
                "company": "Company Name",
                "role": "Job Title",
                "start_date": "YYYY-MM",
                "end_date": "YYYY-MM",
                "location": "City, Country"
            },
            ...
        ]
        """

    def process_output(self, output: str) -> dict:
        experiences = self.parse_json(output)
        return {"work_experiences": experiences}
```

### 3. Keyword Matcher Plugin

```python
from plugins.base import BasePlugin, PluginMetadata, PluginCategory
from models.resume_models import Resume

class KeywordMatcherPlugin(BasePlugin):
    """Plugin to match keywords in a resume against a job description."""

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="keyword_matcher",
            version="1.0.0",
            description="Matches resume keywords against job requirements",
            category=PluginCategory.ANALYZER,
            author="Resume Analysis Team"
        )

    def initialize(self) -> None:
        # Initialize any resources needed
        self.job_keywords = {
            "technical": ["python", "javascript", "sql", "aws", "machine learning"],
            "soft": ["communication", "leadership", "teamwork", "problem solving"]
        }

    def process_resume(self, resume: Resume, extracted_text: str = None) -> Dict[str, Any]:
        """Match resume skills against keyword lists."""
        matches = {
            "technical": [],
            "soft": []
        }

        # Get skills from the resume
        skills = [s.lower() for s in resume.skills]

        # Match against technical keywords
        for keyword in self.job_keywords["technical"]:
            if any(keyword in skill.lower() for skill in skills):
                matches["technical"].append(keyword)

        # Match against soft skills
        for keyword in self.job_keywords["soft"]:
            if any(keyword in skill.lower() for skill in skills):
                matches["soft"].append(keyword)

        # Calculate match percentage
        total_keywords = len(self.job_keywords["technical"]) + len(self.job_keywords["soft"])
        total_matches = len(matches["technical"]) + len(matches["soft"])
        match_percentage = (total_matches / total_keywords) * 100 if total_keywords > 0 else 0

        return {
            "matched_keywords": matches,
            "match_percentage": round(match_percentage, 2)
        }
```

## Plugin Management

### Loading Plugins

The system automatically loads plugins from:
1. `base_plugins/` directory
2. `custom_plugins/` directory

### Plugin Configuration

Plugins can be configured through:
1. Environment variables
2. Configuration files
3. Command-line arguments

### Plugin Dependencies

Handle plugin dependencies by:
1. Declaring dependencies in plugin metadata
2. Checking dependencies during initialization
3. Loading dependencies in correct order

### Enabling and Disabling Plugins

#### Disabling Specific Custom Plugins
To disable a specific custom plugin, comment it out or remove it from the `__all__` list in custom_plugins/__init__.py:

```python
# Define the list of all custom plugins
__all__: List[str] = [
    # "YourCustomExtractorPlugin"  # Commented out to disable this plugin
]
```

#### Disabling All Custom Plugins
To disable all custom plugins, set `ENABLE_CUSTOM_PLUGINS = False` in config.py:

```python
# Plugin system configuration
PLUGINS_DIR = os.environ.get("PLUGINS_DIR", "./plugins")
CUSTOM_PLUGINS_DIR = os.environ.get("CUSTOM_PLUGINS_DIR", "./custom_plugins")
ENABLE_CUSTOM_PLUGINS = False  # Set to False to disable all custom plugins
```

## Advanced Plugin Development

### LLM Interaction Options

Plugins can interact with the LLM in various ways:

1. **Direct Extraction**: Using a prompt template and the extract_with_llm function
2. **Chained Extraction**: Making multiple LLM calls in sequence to refine results
3. **Batched Processing**: Processing data in batches to handle larger resumes
4. **Custom LLM Call**: Making custom calls to the LLM service for specialized needs

Example of a chained extraction:

```python
def extract(self, text: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    # First extraction for basic data
    first_result, token_usage = self.extract_basic_info(text)

    # Second extraction with more context
    enhanced_prompt = f"""
    Based on the following information extracted from a resume:
    {first_result}

    Please provide a detailed analysis of...
    """
    enhanced_result, enhanced_token_usage = self.extract_detailed_info(enhanced_prompt)

    # Combine token usage
    combined_token_usage = {
        "total_tokens": token_usage.get("total_tokens", 0) + enhanced_token_usage.get("total_tokens", 0),
        "prompt_tokens": token_usage.get("prompt_tokens", 0) + enhanced_token_usage.get("prompt_tokens", 0),
        "completion_tokens": token_usage.get("completion_tokens", 0) + enhanced_token_usage.get("completion_tokens", 0),
        "extractor": self.metadata.name
    }

    # Combine results
    combined_result = {**first_result, "detailed_analysis": enhanced_result}

    return combined_result, combined_token_usage
```

### Using Results from Other Plugins

Your custom plugin can use data already extracted by other plugins:

```python
def process_resume(self, resume: Resume, extracted_text: str = None) -> Dict[str, Any]:
    # Access data from another plugin
    skills = resume.skills
    work_experience = resume.work_experiences

    # Use this data in your custom processing
    # ...
```

For more complex dependencies, you can request the plugin manager in your initialize method:

```python
def initialize(self, plugin_manager=None) -> None:
    self.plugin_manager = plugin_manager

def process_resume(self, resume: Resume, extracted_text: str = None) -> Dict[str, Any]:
    # Get results from another plugin if needed
    if self.plugin_manager:
        other_plugin = self.plugin_manager.get_plugin("other_plugin_name")
        if other_plugin:
            # Use the other plugin directly
            pass
```

## Plugin Lifecycle

1. **Discovery**: The Plugin Manager scans both base_plugins and custom_plugins directories
2. **Filtering**: Only plugins listed in the `__all__` list in each directory's __init__.py are considered
3. **Instantiation**: Each plugin class is instantiated
4. **Initialization**: The `initialize()` method is called on each plugin
5. **Registration**: Plugins are registered with the Plugin Manager by name
6. **Extraction**: For resume processing, extractor plugins are called to extract data
7. **Processing**: After extraction, processor plugins are called to process the extracted data
8. **Integration**: Results are combined into a unified Resume object
9. **Storage**: The processed resume is saved to JSON

## Troubleshooting

### Common Issues

1. **Plugin Not Loading**
   - Ensure your plugin class is listed in the `__all__` list in custom_plugins/__init__.py
   - Check that ENABLE_CUSTOM_PLUGINS is True in config.py
   - Verify that your plugin class inherits from BasePlugin or ExtractorPlugin
   - Check the logs for any error messages during plugin discovery and loading

2. **LLM API Errors**
   - Verify your API key is correctly set in the .env file
   - Check if you've reached API rate limits
   - Ensure your prompt template is properly formatted

3. **Result Formatting Issues**
   - Validate that your Pydantic model matches the expected output format
   - Ensure the format_instructions in your prompt template is included
   - Check that the LLM understands how to format the output correctly

4. **Performance Issues**
   - Consider batching or chunking large resumes
   - Implement caching for expensive operations
   - Use concurrent processing where appropriate

### Advanced Troubleshooting

If you encounter issues with the plugin system:

1. Enable verbose logging with `--verbose`
2. Check the log file (cvinsight.log) for detailed error messages
3. Verify that all required Python packages are installed
4. Check for circular imports in your plugin code
5. Ensure your plugin follows the correct interface
6. Verify the file doesn't contain null bytes (clean with `python -m utils.cleanup`)
7. Check Python version compatibility (recommended: Python 3.8+)

## Benefits of the Plugin Architecture

1. **Modularity**: Each extraction functionality is encapsulated
2. **Extensibility**: New extractors can be added without modifying core code
3. **Maintainability**: Easier to update individual components
4. **Customization**: Users can develop specialized extractors
5. **Reusability**: Plugins can be shared and reused across projects
6. **Isolation**: Errors in one plugin don't affect others
7. **Scalability**: New capabilities can be added incrementally

## Next Steps

- Review the [Technical Documentation](Technical-Documentation) for detailed technical documentation
- Check out the [Examples & Tutorials](Examples-and-Tutorials) for more plugin examples
- Join the community to share and learn about plugins
