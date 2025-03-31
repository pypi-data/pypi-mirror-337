import os
from pathlib import Path

import pytest
from unittest.mock import patch
from compress_mail.compress_mail import MailCompressor


@patch('os.walk')
def test_find_mails_to_compress(mock_walk):
    mock_walk.return_value = [
        (
            '/path/to/maildir',
            [],
            ['1742423129.M60927P26663.fully,S=30457,W=30918:2,S', '1742423130.M622371P26663.fully,S=12796,W=12984:2,S'],
        )
    ]
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    mails = compressor.find_mails_to_compress()
    assert len(mails) == 2


# @patch('shutil.copy2')
# @patch('subprocess.run')
# def test_compress_mails_gzip(mock_run, mock_copy):
#     compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
#     mails = ['/path/to/maildir/mail1:2,']
#     compressed_files = compressor.compress_mails(mails)
#     assert len(compressed_files) == 1
#     mock_run.assert_called_with(['gzip', '-6', '/tmp/mail1:2,'])


# @patch('os.utime')
# @patch('os.path.getmtime')
# def test_update_mtime(mock_getmtime, mock_utime):
#     mock_getmtime.return_value = 1234567890
#     compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
#     original_files = ['/path/to/maildir/mail1:2,']
#     compressed_files = ['/tmp/mail1:2,.gz']
#     compressor.update_mtime(original_files, compressed_files)
#     mock_utime.assert_called_with('/tmp/mail1:2,.gz', (1234567890, 1234567890))


def test_update_mtime(tmp_path):
    # Create original and compressed files
    original_file = tmp_path / 'original_mail'
    compressed_file = tmp_path / 'compressed_mail.gz'
    original_file.touch()
    compressed_file.touch()

    # Set a specific mtime for the original file
    original_mtime = 1234567890
    os.utime(original_file, (original_mtime, original_mtime))

    # Create a MailCompressor instance
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)

    # Call update_mtime
    compressor.update_mtime([original_file], [compressed_file])

    # Verify that the mtime of the compressed file matches the original file
    assert compressed_file.stat().st_mtime == original_mtime


# @patch('os.rename')
# @patch('os.remove')
# @patch('os.path.exists')
# def test_verify_and_replace_mails(mock_exists, mock_remove, mock_rename):
#     mock_exists.return_value = True
#     compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
#     original_files = ['/path/to/maildir/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa']
#     compressed_files = ['/tmp/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ']
#     compressor.verify_and_replace_mails(original_files, compressed_files)
#     mock_rename.assert_any_call('/tmp/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ', '/path/to/maildir/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa')
#     mock_rename.assert_any_call('/path/to/maildir/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa', '/path/to/maildir/1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ')


def test_verify_and_replace_mails(tmp_path):
    # Create original and compressed files
    original_file = tmp_path / '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa'
    compressed_file = tmp_path / '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa.gz'
    final_file = tmp_path / '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ'
    original_file.touch()
    compressed_file.touch()

    # Create a MailCompressor instance
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)

    # Call verify_and_replace_mails
    compressor.verify_and_replace_mails([original_file], [compressed_file])

    # Verify that the original file has been renamed and the compressed file has been removed
    assert not original_file.exists()
    assert not compressed_file.exists()
    assert final_file.exists()


@pytest.mark.parametrize(
    'path,original,expected',
    [
        (
            '',
            '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa',
            '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ',
        ),
        (
            '.folder.with spaces',
            '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSa',
            '1685154999.M900454P14950.fully,S=13592,W=13909:2,FSaZ',
        ),
    ],
)
def test_run_with_lock(path, original, expected, tmp_path):
    original_file = tmp_path / path / 'cur' / original
    compressed_file = tmp_path / path / 'cur' / expected
    original_file.parent.mkdir(parents=True)
    Path.mkdir(tmp_path / path / 'tmp', parents=True, exist_ok=True)
    original_file.write_text('Test file')
    compressor = MailCompressor(
        maildir=str(tmp_path / path / 'cur'),
        tmp_dir=str(tmp_path / path / 'tmp'),
        control_dir=str(tmp_path / path),
        timeout=10,
        compression_method='gzip',
        use_lock=True,
    )
    compressor.run()
    assert not original_file.exists()
    assert compressed_file.exists()


# @patch('compress_mail.compress_mail.MaildirLock')
# @patch('compress_mail.compress_mail.MailCompressor.check_binaries')
# @patch('compress_mail.compress_mail.MailCompressor.get_directory_size')
# def test_run_without_lock(mock_get_directory_size, mock_check_binaries, mock_lock):
#     mock_get_directory_size.return_value = 1
#     compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
#     compressor.find_mails_to_compress = MagicMock(return_value=['/path/to/maildir/mail1:2,'])
#     compressor.compress_mails = MagicMock(return_value=['/tmp/mail1:2,.gz'])
#     compressor.update_mtime = MagicMock()
#     compressor.verify_and_replace_mails = MagicMock()
#     compressor.run()
#     compressor.verify_and_replace_mails.assert_called_once()


@patch('os.walk')
def test_find_mails_to_compress_returns_empty_list_when_no_mails(mock_walk):
    mock_walk.return_value = [('/path/to/maildir', [], [])]
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    mails = compressor.find_mails_to_compress()
    assert len(mails) == 0


@patch('shutil.copy2')
@patch('subprocess.run')
def test_compress_mails_handles_empty_list(mock_run, mock_copy):
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    compressed_files = compressor.compress_mails([])
    assert len(compressed_files) == 0
    mock_run.assert_not_called()
    mock_copy.assert_not_called()


def test_update_mtime_handles_empty_lists():
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    compressor.update_mtime([], [])
    # No exception should be raised


def test_verify_and_replace_mails_handles_empty_lists():
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    compressor.verify_and_replace_mails([], [])
    # No exception should be raised


def test_with_ending_appends_correctly():
    compressor = MailCompressor('/path/to/maildir', '/tmp', '/control', 10, 'gzip', False)
    path = Path('example.txt')
    new_path = compressor.with_ending(path, 'Z')
    assert new_path.name == 'example.txtZ'
