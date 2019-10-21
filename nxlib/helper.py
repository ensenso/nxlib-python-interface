# -*- coding: utf-8 -*-

import os
import platform
import re

from .exception import NxLibError


def find_and_return_lib(possible_directories, library_name):
    for possible_directory in possible_directories:
        for file in os.listdir(possible_directory):
            if file == library_name:
                return os.path.join(possible_directory, file)


def _get_os():
    operating_systems = {"win": "Windows",
                         "linux": "Linux",
                         "mac": "Darwin"}

    detected_os = platform.platform(terse=True)
    for possible_os in operating_systems:
        if operating_systems[possible_os] in detected_os:
            return possible_os


def _get_architecture_bits():
    [bits, linkage] = platform.architecture()
    return bits


def get_lib_name(is_remote_lib=False):
    if is_remote_lib:
        default_lib_names = {"win32bit": "NxLibRemote32.dll",
                             "win64bit": "NxLibRemote32.dll",
                             "linux32bit": "libNxLibRemote32.so",
                             "linux64bit": "libNxLibRemote64.so"}
    else:
        default_lib_names = {"win32bit": "NxLib32.dll",
                             "win64bit": "NxLib64.dll",
                             "linux32bit": "libNxLib32.so",
                             "linux64bit": "libNxLib64.so"}
    os = _get_os()
    bits = _get_architecture_bits()

    try:
        return default_lib_names[os + bits]
    except:
        raise NxLibError("Could not determine NxLib library for this "
                         "system os: {} and bits: {}".format(os, bits))


def fix_string_encoding(path):
    try:
        if path is None:
            return b''
        path = path.encode()
    except AttributeError:
        pass
    return path


def convert_camel_to_lower_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_camel_to_upper_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).upper()


def fix_nxlib_prefix(word):
    return word[:2] + word[3:]
