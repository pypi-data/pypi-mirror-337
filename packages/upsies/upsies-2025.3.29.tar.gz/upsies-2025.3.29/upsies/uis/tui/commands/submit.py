"""
Generate all required metadata and upload to tracker
"""

import functools
import os

from .... import __project_name__, constants, jobs, trackers, utils
from . import base


class submit(base.CommandBase):
    """Generate all required metadata and upload to TRACKER"""

    names = ('submit',)

    argument_definitions = {}

    subcommand_name = 'TRACKER'
    subcommands = {
        tracker.name: {
            'description': (
                f'Generate all required metadata and upload it to {tracker.label}.\n'
                '\n'
                f'For step-by-step instructions run this command:\n'
                '\n'
                f'    $ {__project_name__} submit {tracker.name} --howto-setup\n'
            ),
            'cli': {
                # Default arguments for all tackers
                ('--howto-setup',): {
                    'action': base.PrintText(text_getter=tracker.generate_setup_howto),
                    'nargs': 0,
                    'help': 'Show detailed instructions on how to do your first upload',
                },
                'CONTENT': {
                    'type': utils.argtypes.content,
                    'help': 'Path to release content',
                },
                ('--is-scene',): {
                    'type': utils.argtypes.bool_or_none,
                    'default': None,
                    'help': ('Whether this is a scene release (usually autodetected)\n'
                             'Valid values: '
                             + ', '.join(
                                 f'{true}/{false}'
                                 for true, false in zip(utils.types.Bool.truthy, utils.types.Bool.falsy)
                             )),
                },
                ('--exclude-files', '--ef'): {
                    'nargs': '+',
                    'action': 'extend',
                    'metavar': 'PATTERN',
                    'help': ('Glob pattern to exclude from torrent '
                             '(matched case-insensitively against path in torrent)'),
                    'default': [],
                },
                ('--exclude-files-regex', '--efr'): {
                    'nargs': '+',
                    'action': 'extend',
                    'metavar': 'PATTERN',
                    'help': ('Regular expression to exclude from torrent '
                             '(matched case-sensitively against path in torrent)'),
                    'type': utils.argtypes.regex,
                    'default': [],
                },
                ('--reuse-torrent', '-t'): {
                    'nargs': '+',
                    'metavar': 'TORRENT',
                    'help': ('Use hashed pieces from TORRENT instead of generating '
                             'them again or getting them from '
                             f'{utils.fs.tildify_path(constants.GENERIC_TORRENTS_DIRPATH)}\n'
                             'TORRENT may also be a directory, which is searched recursively '
                             'for a matching *.torrent file.\n'
                             "NOTE: This option is ignored if TORRENT doesn't match properly."),
                    'type': utils.argtypes.existing_path,
                    'default': (),
                },
                ('--add-to', '-a'): {
                    'type': utils.argtypes.client,
                    'metavar': 'CLIENT',
                    'help': ('Case-insensitive BitTorrent client name\n'
                             'Supported clients: ' + ', '.join(utils.btclient.client_names())),
                },
                ('--copy-to', '-c'): {
                    'metavar': 'PATH',
                    'help': 'Copy the created torrent to PATH (file or directory)',
                },
                ('--ignore-rules', '--ir'): {
                    'action': 'store_true',
                    'help': 'Allow submission if it is against tracker rules',
                },
                # Custom arguments defined by tracker for this command
                **tracker.TrackerConfig.argument_definitions.get('submit', {}),
            },
        }
        for tracker in trackers.trackers()
    }

    @functools.cached_property
    def jobs(self):
        return (
            *self.tracker_jobs.jobs_before_upload,
            self.main_job,
            *self.tracker_jobs.jobs_after_upload,
        )

    @functools.cached_property
    def main_job(self):
        return jobs.submit.SubmitJob(
            home_directory=self.home_directory,
            cache_directory=self.cache_directory,
            ignore_cache=self.args.ignore_cache,
            tracker_jobs=self.tracker_jobs,
        )

    @functools.cached_property
    def tracker_name(self):
        """Lower-case abbreviation of tracker name"""
        return self.args.subcommand.lower()

    @functools.cached_property
    def tracker_options(self):
        """
        :attr:`tracker_name` section in trackers configuration file combined with
        CLI arguments where CLI arguments take precedence unless their value is
        `None`
        """
        return self.get_options('trackers', self.tracker_name)

    @functools.cached_property
    def tracker(self):
        """
        :class:`~.trackers.base.TrackerBase` instance from one of the submodules of
        :mod:`.trackers`
        """
        return trackers.tracker(
            name=self.tracker_name,
            options=self.tracker_options,
        )

    @functools.cached_property
    def tracker_jobs(self):
        """
        :class:`~.trackers.base.TrackerJobsBase` instance from one of the submodules
        of :mod:`.trackers`
        """
        return self.tracker.TrackerJobs(
            tracker=self.tracker,
            options=self.tracker_options,
            content_path=self.args.CONTENT,
            reuse_torrent_path=(
                tuple(self.args.reuse_torrent)
                + tuple(self.config['config']['torrent-create']['reuse_torrent_paths'])
            ),
            screenshots_optimization=self.config['config']['screenshots']['optimize'],
            show_poster=self.config['config']['id']['show_poster'],
            image_hosts=self._get_image_hosts(),
            btclient=self._get_btclient(),
            torrent_destination=self._get_torrent_destination(),
            exclude_files=(
                tuple(self.config['trackers'][self.tracker.name]['exclude'])
                + tuple(self.args.exclude_files)
                + tuple(self.args.exclude_files_regex)
            ),
            common_job_args={
                'home_directory': self.home_directory,
                'cache_directory': self.cache_directory,
                'ignore_cache': self.args.ignore_cache,
            },
        )

    def _get_image_hosts(self):
        return tuple(
            self._get_image_host(name)
            for name in self.tracker_options.get('image_host', ())
        )

    def _get_image_host(self, name):
        # Get global image host options from imghosts.ini
        name = str(name).lower()
        options = self.config['imghosts'][name].copy()

        # Apply tracker-specific options that are common for all image hosts
        # (e.g. thumbnail size)
        options.update(self.tracker.TrackerJobs.image_host_config.get('common', {}))

        # Apply tracker-specific options for the used image host
        options.update(self.tracker.TrackerJobs.image_host_config.get(name, {}))

        return utils.imghosts.imghost(
            name=name,
            options=options,
            cache_directory=self.home_directory,
        )

    def _get_btclient_name(self):
        return (
            getattr(self.args, 'add_to', None)
            or self.tracker_options.get('add_to', None)
            or None
        )

    def _get_btclient(self):
        client_name = self._get_btclient_name()
        if client_name:
            options = self.get_options('clients', client_name)
            return utils.btclient.BtClient(
                name=client_name,
                url=options['url'],
                username=options['username'],
                password=options['password'],
                # See torrent_create.download_path for some reasoning.
                download_path=options['translate_path'].translate(
                    os.path.abspath(utils.fs.dirname(self.args.CONTENT))
                ),
                check_after_add=options['check_after_add'],
                category=options.get('category', ''),
            )

    def _get_torrent_destination(self):
        return (
            getattr(self.args, 'copy_to', None)
            or self.tracker_options.get('copy_to', None)
            or None
        )
