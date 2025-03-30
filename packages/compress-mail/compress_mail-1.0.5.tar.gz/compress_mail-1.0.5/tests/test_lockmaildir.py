import pytest
import time

from compress_mail.lockmaildir import maildir_lock


def test_maildir_lock(tmp_path):
    lock_path = tmp_path / 'maildir'
    lock_path.mkdir()
    with maildir_lock(lock_path, 10) as lock_file:
        assert lock_file == tmp_path / 'maildir/dovecot-uidlist.lock'
        assert lock_file.exists()
    assert not lock_file.exists()


def test_lock_failure(tmp_path):
    p = tmp_path / 'dovecot-uidlist.lock'
    p.write_text('Test file')
    print(p)
    print(p.exists())
    with pytest.raises(TimeoutError) as excinfo:
        with maildir_lock(tmp_path, 1) as lock_file:
            time.sleep(1)
