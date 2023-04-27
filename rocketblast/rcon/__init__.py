__import__('pkg_resources').declare_namespace(__name__)
from .frostbite.frostbite import Client as FrostbiteClient
from .frostbite.frostbite import FormatClient as FormatFrostbiteClient

__all__ = ['frostbite']