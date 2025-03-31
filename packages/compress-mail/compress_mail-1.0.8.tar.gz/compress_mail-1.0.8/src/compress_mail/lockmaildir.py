import logging
import os
import signal
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DotlockSettings:
    timeout: int
    use_excl_lock: bool
    nfs_flush: bool


@contextmanager
def file_dotlock_create(dotlock_settings: DotlockSettings, path: Path) -> Path:
    lock_file = path.with_suffix('.lock')
    start_time = time.time()
    ours = False
    while True:
        try:
            with lock_file.open('x') as f:
                f.write('lock')
            logger.info(f'Created lock file {lock_file}')
            ours = True
            yield lock_file
            break
        except FileExistsError:
            logger.info(f'Lock file {lock_file} already exists')
            if time.time() - start_time >= dotlock_settings.timeout:
                raise TimeoutError(f"Failed to acquire lock within {dotlock_settings.timeout} seconds")
            time.sleep(1)
        finally:
            if lock_file.exists() and ours:
                logger.info(f'Removing lock file {lock_file}')
                lock_file.unlink()


def maildir_lock(path: Path, timeout: int) -> Path:
    dotlock_settings = DotlockSettings(
        timeout=timeout,
        use_excl_lock=os.getenv('DOTLOCK_USE_EXCL') is not None,
        nfs_flush=os.getenv('MAIL_NFS_STORAGE') is not None,
    )
    lock_path = path / 'dovecot-uidlist'
    return file_dotlock_create(dotlock_settings, lock_path)


def sig_die(signum, frame):
    print('Signal received, exiting...')
    sys.exit(0)


def main():
    if len(sys.argv) != 3:
        print('Usage: maildirlock <path> <timeout>\n - SIGTERM will release the lock.')
        sys.exit(1)

    path = Path(sys.argv[1])
    try:
        timeout = int(sys.argv[2])
    except ValueError:
        print(f'Invalid timeout value: {sys.argv[2]}')
        sys.exit(1)

    signal.signal(signal.SIGTERM, sig_die)
    signal.signal(signal.SIGINT, sig_die)

    lock_acquired = False
    try:
        with maildir_lock(path, timeout) as lock_file:
            lock_acquired = True
            pid = os.getpid()
            print(pid)
            while True:
                time.sleep(1)
    except Exception as e:
        if not lock_acquired:
            print(f'Failed to acquire lock: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
