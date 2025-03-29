from abc import abstractmethod

from jinja2 import BaseLoader

from json2any_plugin.AbstractProvider import AbstractProvider


class AbstractTemplateProvider(AbstractProvider):
    """
    Provides jinja2 template loader.
    """

    @abstractmethod
    def get_loader(self) -> BaseLoader:
        """
        If activated via commandline Creates jinja2 template loader
        :return BaseLoader: instance of jinja2.BaseLoader
        """
        raise NotImplementedError()
