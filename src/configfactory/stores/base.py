import abc
import base64
import json
import zlib
from collections import OrderedDict
from typing import Dict, Union

from cryptography.fernet import Fernet
from django.utils.functional import cached_property


class ConfigStore(abc.ABC):

    def __init__(self, encode: bool = False):
        self.encode = encode

    def all(self) -> dict:
        """
        Get all settings.
        """
        all_settings = {}
        for environment, component_data in self.all_data().items():
            all_settings[environment] = {}
            for component, data in component_data.items():
                settings = json.loads(
                    self._decode_data(data),
                    object_pairs_hook=OrderedDict
                )
                all_settings[environment][component] = settings
        return all_settings

    def get(self, environment: str, component: str) -> dict:
        """
        Get settings.
        """
        data = self.get_data(environment, component)
        return json.loads(
            self._decode_data(data),
            object_pairs_hook=OrderedDict
        )

    def update(self, environment: str, component: str, settings: dict):
        """
        Update settings.
        """
        # Prepare settings string
        if isinstance(settings, dict):
            settings = json.dumps(settings, separators=(',', ':'))
        data = self._encode_data(settings)
        self.update_data(environment, component, data)

    @abc.abstractmethod
    def all_data(self) -> Dict[str, Dict[str, Union[str, bytes]]]:
        pass

    @abc.abstractmethod
    def get_data(self, environment: str, component: str) -> Union[str, bytes]:
        pass

    @abc.abstractmethod
    def update_data(self, environment: str, component: str, data: str):
        pass

    @cached_property
    def encoder(self):
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
            return self.encoder.encrypt(
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
                self.encoder.decrypt(data)
            )
        if isinstance(data, bytes):
            return data.decode()
        return data
