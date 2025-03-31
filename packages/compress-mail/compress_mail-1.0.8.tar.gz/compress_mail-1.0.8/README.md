# Compress mail

[![PyPI - Version](https://img.shields.io/pypi/v/compress-mail.svg)](https://pypi.org/project/compress-mail)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/compress-mail.svg)](https://pypi.org/project/compress-mail)

[![blog](https://img.shields.io/badge/blog-Nerd%20stuff-blue)](https://blog.lucid.net.au/category/nerd-stuff/)
![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/lingfish)

compress-mail is a simple command line tool that is used with [Dovecot](https://www.dovecot.org/) to compress Maildir
format files.

-----

## Table of Contents
<!-- TOC -->
* [Compress mail](#compress-mail)
  * [Table of Contents](#table-of-contents)
  * [Introduction](#introduction)
  * [Installation](#installation)
<!-- TOC -->

## Introduction

`compress-mail` is a simple command line tool that is used with [Dovecot](https://www.dovecot.org/) to compress Maildir
format files.

It follows Dovecot best practices, including its own implementation of the `maildirlock` program, originally written in
C and that is buggy. The Dovecot authors suggest using dsync (`doveadm sync`), but this only does whole mailboxes, not
individual folders, and is more time consuming to configure.

`compress-mail` uses Maildir flags to mark which files have already been compressed, and thus skips them on subsequent
runs, so it is safe to run multiple times.

## Installation

The recommended way to install `compress-mail` is to use [pipx](https://pipx.pypa.io/stable/).

After getting `pipx` installed, simply run:

```console
pipx install compress-mail
```

Please [don't use pip system-wide](https://docs.python.org/3.11/installing/index.html#installing-into-the-system-python-on-linux).

You can of course also install it using classic virtualenvs.

## Usage

Usage help can be obtained by running:

```console
compress-mail --help

Usage: compress-mail [OPTIONS]

Options:
  -b, --basedir TEXT             Base directory containing dovecot-uidlist,
                                 cur, and tmp directories  [required]
  -m, --maildir TEXT             Path to the Maildir (default: basedir/cur/)
  -t, --tmp-dir TEXT             Path to the temporary directory for
                                 compression (default: basedir/tmp/)
  -c, --control-dir TEXT         Path to the control directory containing
                                 dovecot-uidlist (default: basedir)
  --timeout INTEGER              Timeout for maildirlock
  -z, --compression [gzip|zstd]  Compression method to use (gzip or zstd)
  -l, --lock / --no-lock         Use maildir locking mechanism
  --version                      Show the version and exit.
  --help                         Show this message and exit.
```

So, if you have a normal Maildir structure like the following:

```console
drwx------ 2 user group  2363392 Mar 31 08:42 cur
-rw------- 1 user group   242824 Mar 30 15:41 dovecot.index
-rw------- 1 user group 15596760 Mar 31 08:18 dovecot.index.cache
-rw------- 1 user group    26224 Mar 31 08:42 dovecot.index.log
-rw------- 1 user group       97 Feb 15  2019 dovecot-keywords
-rw------- 1 user group   953295 Mar 31 08:18 dovecot-uidlist
-rw------- 1 user group        0 Mar  2  2011 maildirfolder
drwx------ 2 user group    36864 Mar 31 08:17 new
drwx------ 2 user group   270336 Mar 31 08:18 tmp

.Trash
├── cur
├── new
└── tmp
```

All you need to do is run:

```console
user@host:~$ compress-mail --basedir .Trash --compression zstd
```