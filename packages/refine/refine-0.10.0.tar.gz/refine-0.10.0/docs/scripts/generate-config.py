from pathlib import Path
from configparser import ConfigParser
import toml
from recode.config import Config

DOC_ROOT = Path(__file__).parent.parent


def generate_toml_example(config_class, as_pyproject_tool: bool = False):
    config_dict = {'re-code': {field: getattr(config_class, field, '') for field in config_class.__fields__}}
    if as_pyproject_tool:
        return toml.dumps({'tool': config_dict})
    return toml.dumps(config_dict)

def save_example(file_path, content):
    print(content)
    #with open(file_path, 'w') as file:
    #    file.write(content)

if __name__ == "__main__":
    config_class = Config()
    re_code_toml_example = generate_toml_example(config_class, {})
    pyproject_toml_example = generate_toml_example(config_class, {'tool': {}})

    save_example(DOC_ROOT / 'configuration/.re-code.toml', re_code_toml_example)
    save_example(DOC_ROOT / 'configuration/pyproject.toml', pyproject_toml_example)