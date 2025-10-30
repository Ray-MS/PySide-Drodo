from pathlib import Path

import yaml


class URLManager:
    def __init__(self, config_path: str = "config/urls.yaml") -> None:
        self.config_path = Path(config_path)
        self._load_config()

    def _get_nested_value(self, data_dict, key_path: str):
        keys = key_path.split('.')
        current = data_dict
        for key in keys:
            current = current[key]
        return current

    def _load_config(self) -> None:
        with open(self.config_path, 'r', encoding='utf-8') as fp:
            self.config = yaml.safe_load(fp)
        self.default_source = self.config['default_source']

    def build_url(self,  endpoint_path: str, source: str = None, **params) -> str:
        source = source or self.default_source
        base_url = self.config['sources'][source]['base']
        endpoint = self._get_nested_value(self.config['sources'][source]['endpoints'], endpoint_path)
        if params and isinstance(endpoint, str):
            endpoint = endpoint.format(**params)
        return f'{base_url}{endpoint}'


url_manager = URLManager()
