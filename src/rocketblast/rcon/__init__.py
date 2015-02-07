try:
	__import__('pkg_resources').declare_namespace(__name__)
except:
	from pkgutil import extend_path
	__path__ = extend_path(__path__, __name__)

from frostbite.frostbite import Client as FrostbiteClient
from frostbite.frostbite import FormatClient as FormatFrostbiteClient

__all__ = ['frostbite']
