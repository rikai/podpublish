#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) Ubuntu Podcast
# http://www.ubuntupodcast.org
# See the file "LICENSE" for the full license governing this code.

import argparse
import podpublish
from podpublish import configuration
from podpublish import encoder

def main():
    parser = argparse.ArgumentParser(description='Encode a podcast to mp3, ogg and mkv.')
    parser.add_argument('--version', action='version', version=podpublish.__version__)
    parser.add_argument('filename', type=argparse.FileType('r'), help="Podcast configuration file.")
    args = parser.parse_args()

    config = configuration.Configuration(args.filename)
    if not config.skip_mp3:
        encoder.audio_encode(config, 'mp3')
        encoder.mp3_tag(config)
        encoder.mp3_coverart(config)

    if not config.skip_ogg:
        encoder.audio_encode(config, 'ogg')
        encoder.ogg_tag(config)
        encoder.ogg_coverart(config)

    encoder.png_header(config)
    encoder.png_poster(config)

    if not config.skip_youtube:
        encoder.mkv_encode(config)

if __name__ == '__main__':
    main()
