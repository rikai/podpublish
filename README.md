# Introduction

A tool for encoding and publishing podcast content and assets. Inspired
by [bv-publish](https://github.com/stuartlangridge/bv-publish) and the
talk [Stuart Langridge gave at Oggcamp 2015](https://www.youtube.com/watch?v=IG6-YdBbwE8).

Project created by [Ubuntu Podcast](http://www.ubuntupodcast.org) and
released under the [GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
license.

## Installation

Eventually this will be added to PyPi (or something) for simplier
installation. But for now the following steps are required, which
requires you're running Ubuntu 16.04 or newer.

### Install ffmpeg and pip

    sudo apt-get install ffmpeg git libavcodec-extra python3-dev python3-pip

There is also a good quality statically compiled `ffmpeg` available from [John Van Sickle](http://johnvansickle.com/)

  * http://johnvansickle.com/ffmpeg/

### Install Pillow build dependencies

    sudo apt-get install liblcms2-dev libfreetype6-dev libjpeg8-dev \
    libopenjp2-7-dev libtiff5-dev libwebp-dev zlib1g-dev

### Install crypto build dependecies

    sudo apt install libffi-dev libssl-dev

### Install podpublish

#### System wide

    git clone git@bitbucket.org:flexiondotorg/podpublish.git
    sudo pip3 install -r podpublish/requirements.txt

#### In a virtualenv

These are the steps for installing on Ubuntu 16.04.

    sudo apt-get install python-setuptools python-virtualenv python-pip virtualenvwrapper
    sudo apt-get install libpython3.5 python3.5 python3.5-dev python3.5-minimal
    mkdir ~/Snakepit

Using `virtualenv`:

    virtualenv -p /usr/bin/python3.5 ~/Snakepit/podpublish
    source ~/Snakepit/podpublish/bin/activate

Or using `mkvirtualenv`:

    mkvirtualenv -p /usr/bin/python3.5 podpublish
    workon podpublish

Or using `virtualfish`:

    vf new -p /usr/bin/python3.5 podpublish
    workon podpublish

Install podpublish.

    pip3 install -r podpublish/requirements.txt

## Usage

This project is a work in progress and still somewhat hardcoded but
will soon be made into a generic tool useful to other podcasters.

### Encoding a single podcast

To encode an audio file to `.mp3`, `.ogg` and `.mkv` (for uploading to
YouTube, do the following.

The `skip` options, in the `.ini` file, will bypass encoding if set to
`True`.

  * Edit the example `podcast.ini`.
  * Execute `./encode_podcast podcast.ini`.

### Publishing a single podcast

The `skip` options, in the `.ini` file, will bypass publishing if set to
`True`.

  * Edit the example `podcast.ini`.
  * Execute `./publish_podcast podcast.ini`.

### Encoding a season of podcasts

To encode a season of audio files, from existing `.mp3` or `.ogg` files
, encode them to `.mkv` and upload them to YouTube, do the following.

  * Edit the example `season-to-youtube.ini`.
  * Execute `./season-to-youtube season-to-youtube.ini`.

The season encoder/uploader expects derive the each Episode number from
the source audio filename and each episode Title from tags embedded in
the source audio files.

### Publishing targets

#### YouTube API

The reference YouTube API provided by Google doesn't support playlists,
nor setting a publishing date, so [youtube-upload](https://github.com/tokland/youtube-upload)
is used instead.

To upload to YouTube you'll need a Google account with associated
YouTube channel, the YouTube Data API will need to be enabled and
OAuth 2.0 client-secret generated.

The Youtube API uses [OAuth 2.0](https://developers.google.com/accounts/docs/OAuth2)
to authenticate the upload. The first time you try to upload a video,
you will be asked to follow a URL in your browser to get an authentication
token. You can use multiple credentials, just use edit the option
`credentials-file=`. Also, check the [token expiration](https://developers.google.com/youtube/v3/)
policies.

If you plan to make a heavy use of the script, please
[create and use your own OAuth 2.0 file](https://developers.google.com/youtube/registering_an_application),
it's a free service. Steps:

  * Go to the Google [console](https://console.developers.google.com/).
  * _Create project_.
  * Side menu: _APIs & auth_ -> _APIs_
  * Top menu: _Enabled API(s)_: Enable all Youtube APIs.
  * Side menu: _APIs & auth_ -> _Credentials_.
  * _Create a Client ID_: Add credentials -> OAuth 2.0 Client ID -> Other -> Name: youtube-upload -> Create -> OK
  * _Download JSON_: Under the section "OAuth 2.0 client IDs". Save the file to your local system.
  * Use this JSON as your credentials file: `client-secrets=CLIENT_SECRETS`

The following video may also be helpful in enabling the YouTube Data API
and creating client secrets.

  * https://www.youtube.com/watch?v=IX8xlnk54Mg

#### sftp

This is how to create an account, on Ubuntu, that has sftp access via
key based authentication.

#### On your workstation

Generate a ssh key pair. This will create `~/PodPublish.key`
(the private key) and `~/PodPublish.pub` (the public key).

    ssh-keygen -b 4096 -t rsa -N yoursupersecretpassphrase -C "Podcast Publisher" -f ~/PodPublish

#### On the server

    sudo apt-get install ssh
    sudo adduser --gecos "Podcast Publisher" --disabled-password yourusername

As `root` do the following on the server to create the `authorized_keys`
file.

    mkdir /home/yourusername/.ssh

Add the content of `~/PodPublish.pub` to `/home/yourusername/.ssh/authorized_keys`

    nano /home/yourusername/.ssh/authorized_keys

Set the `~/.ssh` file/directory permissions.

    chmod 600 /home/yourusername/.ssh/authorized_keys
    chmod 700 /home/yourusername/.ssh/
    chown -R yourusername: /home/yourusername/.ssh

## Source Code

Source code is available from BitBucket.

  * https://bitbucket.org/flexiondotorg/podpublish

# Snap

## Ubuntu Podcast Setup

The Snap `home` interface munges `${HOME}` and my use cae for podpublish is to 
use configuration files that contain relative paths to podcast assets, such as 
audio files and artwork.

The Ubuntu Podcast team use Dropbox to sync all the show assets, therefore the 
Dropbox directory needs to be symlinked into the podpublish snap data 
directory.

Run the following, which will create the data directory.

    /snap/bin/podpublish.encode-podcast --version

Now symlink Dropbox.

    ln -s ~/Dropbox ~/snap/podpublish/x{*}/

## Use

To encode a podcast.

    /snap/bin/podpublish.encode_podcast ~/Dropbox/UbuntuPodcast/Configs/S09/s09exx.ini

To upload a podcast.
 
    /snap/bin/podpublish.publish_podcast ~/Dropbox/UbuntuPodcast/Configs/S09/s09exx.ini
