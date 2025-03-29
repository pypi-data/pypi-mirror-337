__project_name__ = 'upsies'
__description__ = 'Media metadata aggregator'
__homepage__ = 'https://upsies.readthedocs.io'
__changelog__ = 'https://codeberg.org/plotski/upsies/raw/branch/master/NEWS'
__version__ = '2025.03.29'


def application_setup(config):
    """
    This function should be called by the UI ASAP when `config` is available

    :param config: :class:`~.configfiles.ConfigFiles` instance
    """
    import os

    from . import utils

    utils.http.cache_directory = os.path.join(
        config['config']['main']['cache_directory'],
        'http',
    )


def application_shutdown(config):
    """
    This function should be called by the UI before the applicatin terminates

    :param config: :class:`~.configfiles.ConfigFiles` instance
    """
    import asyncio

    from . import utils

    # Maintain maximum cache size
    utils.fs.limit_directory_size(
        path=config['config']['main']['cache_directory'],
        max_total_size=config['config']['main']['max_cache_size'],
    )

    # Remove empty files and directories
    utils.fs.prune_empty(
        path=config['config']['main']['cache_directory'],
        files=True,
        directories=True,
    )
