import abc
import base64
import zlib
from typing import Dict, Union

from cryptography.fernet import Fernet
from django.utils.functional import cached_property

from configfactory.utils import json_dumps, json_loads


class ConfigStore(abc.ABC):

    def __init__(self, encode: bool = False):
        self.encode = encode

    def all(self) -> dict:
        """
        Get all settings.
        """
        all_settings = {}
        for environment, component_data in self.all_impl().items():
            all_settings[environment] = {}
            for component, data in component_data.items():
                settings = json_loads(self._decode_data(data))
                all_settings[environment][component] = settings
        return all_settings

    def get(self, component: str, environment: str) -> dict:
        """
        Get settings.
        """
        data = self.get_impl(component, environment)
        return json_loads(self._decode_data(data))

    def update(self, component: str, environment: str, settings: dict):
        """
        Update settings.
        """
        # Prepare settings string
        if isinstance(settings, dict):
            settings = json_dumps(settings)
        data = self._encode_data(settings)
        self.update_impl(component, environment, data)

    @abc.abstractmethod
    def all_impl(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        pass

    @abc.abstractmethod
    def get_impl(self, component: str, environment: str) -> Union[str, bytes]:
        pass

    @abc.abstractmethod
    def update_impl(self, component: str, environment: str, data: str):
        pass

    @cached_property
    def _encoder(self):
        from django.conf import settings
        key = base64.urlsafe_b64encode(
            settings.SECRET_KEY[:32].encode()
        )
        return Fernet(key)

    def _encode_data(self, data: str) -> str:
        """
        Encode and compress data.
        """
        if self.encode:
            return self._encoder.encrypt(
                zlib.compress(data.encode())
            ).decode()
        return data

    def _decode_data(self, data: Union[str, bytes]) -> str:
        """
        Decompress and decrypt data.
        """
        if self.encode:
            if isinstance(data, str):
                data = data.encode()
            data = zlib.decompress(
                self._encoder.decrypt(data)
            )
        if isinstance(data, bytes):
            return data.decode()
        return data
