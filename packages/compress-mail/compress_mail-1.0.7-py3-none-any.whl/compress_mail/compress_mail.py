import os
import shutil
import subprocess
import re
import logging
from pathlib import Path

import click
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import track

from compress_mail._version import __version__
from compress_mail.lockmaildir import maildir_lock


console = Console(highlight=False)


def sizeof_fmt(
    num: float,
    suffix: str = 'B',
    units: list[str] = None,
    power: int = None,
    sep: str = '',
    precision: int = 2,
    sign: bool = False,
) -> str:
    sign = '+' if sign and num > 0 else ''
    fmt = '{0:{1}.{2}f}{3}{4}{5}'
    prec = 0
    for unit in units[:-1]:
        if abs(round(num, precision)) < power:
            break
        num /= float(power)
        prec = precision
    else:
        unit = units[-1]
    return fmt.format(num, sign, prec, sep, unit, suffix)


def sizeof_fmt_iec(num: float, suffix: str = 'B', sep: str = '', precision: int = 2, sign: bool = False) -> str:
    return sizeof_fmt(
        num,
        suffix=suffix,
        sep=sep,
        precision=precision,
        sign=sign,
        units=['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi'],
        power=1024,
    )


def sizeof_fmt_decimal(num: float, suffix: str = 'B', sep: str = '', precision: int = 2, sign: bool = False) -> str:
    return sizeof_fmt(
        num,
        suffix=suffix,
        sep=sep,
        precision=precision,
        sign=sign,
        units=['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'],
        power=1000,
    )


class MailCompressor:
    def __init__(
        self, maildir: str, tmp_dir: str, control_dir: str, timeout: int, compression_method: str, use_lock: bool
    ) -> object:
        self.maildir: Path = Path(maildir)
        self.tmp_dir: Path = Path(tmp_dir)
        self.control_dir: Path = Path(control_dir)
        self.timeout = timeout
        self.compression_method = compression_method
        self.use_lock = use_lock
        self.pid = None
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(message)s',
            datefmt='[%X]',
            handlers=[RichHandler(show_path=False, omit_repeated_times=False, show_level=False)],
        )

    def check_binaries(self) -> None:
        required_binaries = [self.compression_method]
        for binary in required_binaries:
            if not shutil.which(binary):
                raise FileNotFoundError(f'Required binary not found: {binary}')
        logging.info('All required binaries are present')

    def find_mails_to_compress(self) -> list[Path]:
        mails_to_compress: list[Path] = []
        for root, dirs, files in os.walk(self.maildir):
            for filename in track(files, description=f'{"Searching for mails":<25}'):
                if re.search(r'S=\d+', filename) and 'Z' not in filename.split(':')[1]:
                    mails_to_compress.append(Path(root) / filename)
        if mails_to_compress:
            logging.info(f'Found {len(mails_to_compress)} mails to compress')
        else:
            logging.info('No mails found to compress')
        return mails_to_compress

    def compress_mails(self, mails: list[Path]) -> list[Path]:
        compressed_files: list[Path] = []
        for mail in track(mails, description=f'{"Compressing mails":<25}'):
            compressed_file = self.tmp_dir / mail.name
            shutil.copy2(mail, compressed_file)
            if self.compression_method == 'gzip':
                subprocess.run(['gzip', '-6', compressed_file])
                compressed_files.append(self.with_ending(compressed_file, '.gz'))
            elif self.compression_method == 'zstd':
                subprocess.run(['zstd', '-3', '--rm', '-q', '-T0', compressed_file])
                compressed_files.append(self.with_ending(compressed_file, '.zst'))
        logging.info(f'Compressed {len(compressed_files)} mails using {self.compression_method}')
        return compressed_files

    def update_mtime(self, original_files: list[Path], compressed_files: list[Path]) -> None:
        zipped = list(zip(original_files, compressed_files))
        for original, compressed in track(zipped, description=f'{"Updating mtime":<25}'):
            logging.debug(f'Original file: {original}')
            logging.debug(f'Compressed file: {compressed}')
            original_mtime = original.stat().st_mtime
            os.utime(compressed, (original_mtime, original_mtime))
        logging.info('Updated mtimes for compressed files')

    def verify_and_replace_mails(self, original_files: list[Path], compressed_files: list[Path]) -> None:
        zipped = list(zip(original_files, compressed_files))
        for original, compressed in track(zipped, description=f'{"Verifying/replacing mails":<25}'):
            logging.debug(f'Original file: {original}')
            logging.debug(f'Compressed file: {compressed}')
            if original.exists():
                final = compressed.replace(self.with_ending(original, 'Z'))
                logging.debug(f'Final file: {final}')
                original.unlink()
            else:
                compressed.unlink()
        logging.info('Verified and replaced original mails with compressed ones')

    def get_directory_size(self, directory: Path) -> int:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                total_size += file_path.stat().st_size
        return total_size

    def with_ending(self, path: Path, ending: str) -> Path:
        return path.with_name(path.name + ending)

    def run(self):
        try:
            logging.info('Starting maildir compression process')
            logging.info(f'maildir: {self.maildir}')
            logging.info(f'tmp_dir: {self.tmp_dir}')
            logging.info(f'control_dir: {self.control_dir}')

            self.check_binaries()
            initial_size = self.get_directory_size(self.maildir)
            logging.info(f'Initial maildir size: {sizeof_fmt_decimal(initial_size)}')

            mails_to_compress = self.find_mails_to_compress()
            if not mails_to_compress:
                return
            logging.debug(f'Found {mails_to_compress} mails to compress')

            compressed_files = self.compress_mails(mails_to_compress)
            self.update_mtime(mails_to_compress, compressed_files)

            if self.use_lock:
                with maildir_lock(self.control_dir, self.timeout):
                    self.verify_and_replace_mails(mails_to_compress, compressed_files)
            else:
                self.verify_and_replace_mails(mails_to_compress, compressed_files)

            final_size = self.get_directory_size(self.maildir)
            logging.info(f'Final maildir size: {sizeof_fmt_decimal(final_size)}')

            savings = ((initial_size - final_size) / initial_size) * 100
            logging.info(f'Disk savings: {savings:.2f}%')

            logging.info('Completed maildir compression process')

        except FileNotFoundError as e:
            logging.error(f'Error occurred: {e}')
            console.print_exception(show_locals=True, width=250, word_wrap=True)


@click.command()
@click.option('--basedir', '-b', required=True, help='Base directory containing dovecot-uidlist, cur, and tmp directories')
@click.option('--maildir', '-m', default=None, help='Path to the Maildir (default: basedir/cur/)')
@click.option('--tmp-dir', '-t', default=None, help='Path to the temporary directory for compression (default: basedir/tmp/)')
@click.option('--control-dir', '-c', default=None, help='Path to the control directory containing dovecot-uidlist (default: basedir)')
@click.option('--timeout', type=int, default=10, help='Timeout for maildirlock')
@click.option(
    '--compression',
    '-z',
    type=click.Choice(['gzip', 'zstd']),
    default='gzip',
    help='Compression method to use (gzip or zstd)',
)
@click.option('--lock/--no-lock', '-l', is_flag=True, default=True, help='Use maildir locking mechanism')
@click.version_option(version=__version__)
def main(basedir, maildir, tmp_dir, control_dir, timeout, compression, lock):
    if maildir is None:
        maildir = basedir + '/cur'
    if tmp_dir is None:
        tmp_dir = basedir + '/tmp'
    if control_dir is None:
        control_dir = basedir

    compressor = MailCompressor(
        maildir=maildir,
        tmp_dir=tmp_dir,
        control_dir=control_dir,
        timeout=timeout,
        compression_method=compression,
        use_lock=lock,
    )
    compressor.run()


if __name__ == '__main__':
    main()
