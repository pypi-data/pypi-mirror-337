"""
Configuration files
"""

import collections
import configparser
import copy
import functools
import os
from os.path import exists as _path_exists

from .. import errors, utils

import logging  # isort:skip
_log = logging.getLogger(__name__)


def _is_iterable_type(cls):
    return issubclass(cls, collections.abc.Iterable) and not issubclass(cls, str)

def _is_iterable(value):
    return isinstance(value, collections.abc.Iterable) and not isinstance(value, str)

def _any2iterable(value):
    return tuple(value) if _is_iterable(value) else tuple(str(value).split())

def _any2string(value):
    return ' '.join(str(v) for v in value) if _is_iterable(value) else str(value)


def config_value(value, *, description=''):
    """
    Add keyword arguments as attributes to `value`

    :param value: Any object
    :param str description: Explains what `value` is for and/or the possible
        values it can have
    """
    clsname = type(value).__name__
    bases = (type(value),)
    attrs = {
        'description': str(description),
    }
    cls = type(clsname, bases, attrs)
    return cls(value)


class ConfigFiles(collections.abc.MutableMapping):
    """
    Combine multiple INI-style configuration files into nested dictionaries

    Each top-level dictionary represents one INI file. It maps section names to
    subsections. Subsections (which are sections in the INI file) contain pairs
    of options and values.

    Sections, subsections and options can be accessed like dictionaries.

    >>> config["main"]["foo"]["bar"]
    "This is bar's value"
    >>> config["main"]["foo"]
    {'bar': "This is bar's value", 'baz': 'Another value'}
    >>> config["main"]["foo"]["bar"] = 'Zatoichi'

    For convenience, `"."` in the key is used as a delimiter.

    >>> config["main.foo.bar"] = "Ichi"
    >>> config["main.foo.bar"]
    'Ichi'

    :param defaults: Nested directory structure as described above with
        default values
    :param files: Mapping of section names to file paths that are :meth:`read`
        during initialization
    """

    def __init__(self, defaults):
        self._defaults = copy.deepcopy(defaults)
        self._cfg = _ConfigDict(self._defaults, types=self._build_types())
        self._files = {}  # Map section names to file paths

    def _build_types(self):
        def make_config_type(value):
            parent_class = type(value)

            def preconvert(v):
                # Convert non-sequence to sequence if we expect a sequence
                if _is_iterable_type(parent_class):
                    if not _is_iterable(v):
                        return _any2iterable(v)
                # Convert sequence to string if we expect a string
                elif _is_iterable(v):
                    return _any2string(v)
                return v

            # Some types initialize their value in __new__(), e.g. tuple.
            def __new__(cls, v):
                v = preconvert(v)
                self = parent_class.__new__(cls, v)
                return self

            # Some types initialize their value in __init__(), e.g. list.
            def __init__(self, v):
                v = preconvert(v)
                try:
                    super(type(self), self).__init__(v)
                except TypeError:
                    # If the parent class does not implement __init__() (e.g. because it initializes
                    # in __init__()), we end up calling object.__init__(), which doesn't take any
                    # arguments.
                    super(type(self), self).__init__()

            clsname = (
                parent_class.__name__[0].upper()
                + parent_class.__name__[1:]
                + 'ConfigType'
            )
            bases = (parent_class,)
            attrs = {
                '__new__': __new__,
                '__init__': __init__,
            }
            return type(clsname, bases, attrs)

        types = {}
        for section, subsections in self._defaults.items():
            types[section] = {}
            for subsection, options in subsections.items():
                types[section][subsection] = {}
                for option, value in options.items():
                    types[section][subsection][option] = make_config_type(value)

        return types

    @property
    def files(self):
        """
        Map section name to file paths

        This is essentially the same as the keyword arguments from
        instantiation.
        """
        return self._files.copy()

    @functools.cached_property
    def paths(self):
        """Sorted tuple of ``section.subsection.option`` paths"""

        def _get_paths(dct, parents=()):
            paths = []
            for k, v in dct.items():
                k_parents = (*parents, k)
                if isinstance(v, collections.abc.Mapping):
                    paths.extend(_get_paths(v, parents=k_parents))
                else:
                    paths.append('.'.join(str(k) for k in k_parents))
            return tuple(sorted(paths))

        return _get_paths(self._defaults)

    def read(self, section, filepath, *, ignore_missing=False):
        """
        Read `filepath` and make its contents available as `section`

        :raises ConfigError: if reading or parsing a file fails
        """
        if ignore_missing and not _path_exists(filepath):
            self._files[section] = filepath
        else:
            try:
                with open(filepath, 'r') as f:
                    string = f.read()
            except OSError as e:
                raise errors.ConfigError(f'{filepath}: {e.strerror}') from e
            else:
                cfg = self._parse(section, string, filepath)
                for subsection_name, subsection in cfg.items():
                    for option_name, option_value in subsection.items():
                        try:
                            self._set(section, subsection_name, option_name, option_value)
                        except errors.ConfigError as e:
                            raise errors.ConfigError(f'{filepath}: {e}') from e
                self._files[section] = filepath

    def _set(self, section, subsection, option, value):
        if section not in self._cfg:
            raise errors.ConfigError(f'{section}: Unknown section')
        elif subsection not in self._cfg[section]:
            raise errors.ConfigError(f'{section}.{subsection}: Unknown subsection')
        elif option not in self._cfg[section][subsection]:
            raise errors.ConfigError(f'{section}.{subsection}.{option}: Unknown option')
        else:
            try:
                self._cfg[section][subsection][option] = value
            except errors.ConfigError as e:
                raise errors.ConfigError(f'{section}.{subsection}.{option}: {e}') from e

    @staticmethod
    def _parse(section, string, filepath):
        cfg = configparser.ConfigParser(
            default_section=None,
            interpolation=None,
        )
        try:
            cfg.read_string(string, source=filepath)
        except configparser.MissingSectionHeaderError as e:
            raise errors.ConfigError(f'{filepath}: Line {e.lineno}: {e.line.strip()}: Option outside of section') from e
        except configparser.ParsingError as e:
            lineno, msg = e.errors[0]
            # TODO: Remove this when Python 3.12 is deprecated.
            import sys
            if sys.version_info >= (3, 13):
                msg = repr(msg)
            raise errors.ConfigError(f'{filepath}: Line {lineno}: {msg}: Invalid syntax') from e
        except configparser.DuplicateSectionError as e:
            raise errors.ConfigError(f'{filepath}: Line {e.lineno}: {e.section}: Duplicate section') from e
        except configparser.DuplicateOptionError as e:
            raise errors.ConfigError(f'{filepath}: Line {e.lineno}: {e.option}: Duplicate option') from e
        except configparser.Error as e:
            raise errors.ConfigError(f'{filepath}: {e}') from e
        else:
            # Make normal dictionary from ConfigParser instance
            # https://stackoverflow.com/a/28990982
            cfg = {s : dict(cfg.items(s))
                   for s in cfg.sections()}

            # Line breaks are interpreted as list separators
            for section in cfg.values():
                for key in section:
                    if '\n' in section[key]:
                        section[key] = tuple(item for item in section[key].split('\n') if item)

            return cfg

    def __getitem__(self, key):
        if isinstance(key, str) and '.' in key:
            path = key.split('.') if isinstance(key, str) else list(key)
            value = self._cfg
            while path:
                value = value[path.pop(0)]
            return value
        else:
            return self._cfg[key]

    def __setitem__(self, key, value):
        if isinstance(key, str) and '.' in key:
            path = key.split('.') if isinstance(key, str) else list(key)
            target = self._cfg
            while len(path) > 1:
                key = path.pop(0)
                target = target[key]
            key = path.pop(0)
        else:
            target = self._cfg
        target[key] = value

    def __delitem__(self, key):
        self.reset(key)

    def __iter__(self):
        return iter(self._cfg)

    def __len__(self):
        return len(self._cfg)

    def __repr__(self):
        return repr(self._cfg)

    def copy(self):
        """Return deep copy as :class:`dict`"""
        return copy.deepcopy(self)

    def reset(self, path=()):
        """
        Set section, subsection or option to default value(s)

        :param path: Section, section and subsection or section, subsection and
            option as sequence or string with `"."` as delimiter
        """
        path = path.split('.') if isinstance(path, str) else list(path)
        while len(path) < 3:
            path.append('')
        self._reset(*path)

    def _reset(self, section=None, subsection=None, option=None):
        # Rename argument variables to untangle them from loop variables
        section_arg, subsection_arg, option_arg = section, subsection, option
        del section, subsection, option

        sections = (section_arg,) if section_arg else tuple(self._cfg)
        for section in sections:
            subsections = (subsection_arg,) if subsection_arg else tuple(self._cfg[section])
            for subsection in subsections:
                options = (option_arg,) if option_arg else tuple(self._cfg[section][subsection])
                for option in options:
                    self._cfg[section][subsection][option] = \
                        self._defaults[section][subsection][option]

    def write(self, *sections, include_defaults=False):
        """
        Save current configuration to file(s)

        List values use ``"\\n  "`` (newline followed by two spaces) as
        separators between items.

        :param sections: Paths to sections, subsections or options to save. Save
            all sections with no arguments.
        :param bool include_defaults: Whether to include commented defaults

        :raise ConfigError: if writing fails
        """
        if not sections:
            sections = tuple(self._files)
        else:
            sections = tuple(s.split('.')[0] for s in sections)

        for section in sections:
            parentdir = os.path.dirname(self._files[section])
            os.makedirs(parentdir, mode=0o700, exist_ok=True)
            try:
                with open(self._files[section], 'w') as f:
                    f.write(self._as_ini(section, include_defaults=include_defaults))
            except OSError as e:
                raise errors.ConfigError(f'{self._files[section]}: {e.strerror or e}') from e

    def _as_ini(self, section, *, include_defaults=False):
        lines = []
        for subsection, options in sorted(self._cfg.get(section, {}).items()):
            lines_subsection = []
            for option, value in sorted(options.items()):
                if utils.is_sequence(value):
                    if value:
                        values = '\n  '.join(str(v) for v in value)
                        line = f'{option} =\n  {values}'
                    else:
                        line = f'{option} ='
                else:
                    line = f'{option} = {value}'

                if value == self._defaults[section][subsection][option]:
                    # `value` is the default value
                    if include_defaults:
                        # Commented default value
                        lines_subsection.append('# ' + line.replace('\n', '\n# '))
                    else:
                        # Exclude default value
                        continue
                else:
                    # Non-default value
                    lines_subsection.append(line)

            lines.append(f'[{subsection}]')
            lines.extend(lines_subsection)

            # Empty line between subsections
            lines.append('')

        return '\n'.join(lines)


class _ConfigDict(collections.abc.MutableMapping):
    """
    Dictionary that only accepts certain keys and value types

    :param dict dct: Nested mapping of initial values
    :param dict keys: Nested mapping of allowed keys. Leaf values are
        ignored. If omitted, keys from `dct` are used.
    :param dict types: Nested mapping of value converters. Converters get a
        value as a positional argument and return the converted value.

    Getting or setting keys that are not in `keys` raises `KeyError`.

    Setting keys that are dictionaries to non-dictionaries raises `TypeError`.
    Setting keys that are non-dictionaries to dictionaries raises `TypeError`.

    Subdictionaries are always instances of this class with the appropriate
    `keys` and `types`.

    Setting an existing subdictionary to a dictionary copies values instead of
    replacing the subdictionary.
    """

    def __init__(self, dct, *, keys=None, types=None):
        assert isinstance(dct, collections.abc.Mapping)
        self._keys = self._build_keys(keys or dct)
        self._types = types or {}
        self._dct = {}
        for k, v in dct.items():
            self[k] = v

    def _build_keys(self, keys):
        built_keys = {}
        for k, v in keys.items():
            if isinstance(v, collections.abc.Mapping):
                built_keys[k] = self._build_keys(v)
            else:
                built_keys[k] = None
        return built_keys

    def __getitem__(self, key):
        return self._dct[key]

    def __delitem__(self, key):
        del self._dct[key]

    def __setitem__(self, key, value):
        self._dct[key] = self._convert(key, value)

    def _convert(self, key, value):
        if key not in self._keys:
            raise KeyError(key)

        if (
                key in self._types
                and not isinstance(self._types[key], collections.abc.Mapping)
        ):
            converter = self._types[key]
            try:
                value = converter(value)
            except (ValueError, TypeError) as e:
                raise errors.ConfigError(e) from e

        if isinstance(self._keys[key], collections.abc.Mapping):
            # Setting a subdictionary
            if not isinstance(value, collections.abc.Mapping):
                raise TypeError(
                    f'Expected dictionary for {key}, '
                    f'not {type(value).__name__}: {value!r}'
                )
            else:
                # Merge new dictionary into existing dictionary
                if key in self._dct:
                    value = utils.merge_dicts(self._dct[key], value)
                return _ConfigDict(
                    value,
                    keys=self._keys[key],
                    types=self._types.get(key, None),
                )
        elif isinstance(value, collections.abc.Mapping):
            # Key is not a dictionary, so value can't be one
            raise TypeError(f'{key} is not a dictionary: {value!r}')
        else:
            return value

    def __iter__(self):
        return iter(self._dct)

    def __len__(self):
        return len(self._dct)

    def __repr__(self):
        return repr(self._dct)

    def copy(self):
        """Return deep copy as :class:`dict`"""
        return copy.deepcopy(self)
