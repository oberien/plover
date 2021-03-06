# Copyright (c) 2013 Hesky Fisher
# See LICENSE.txt for details.

import io
import json
from collections import defaultdict

import pytest

from plover_build_utils.testing import steno_to_stroke


DICT_NAMES = ['main.json',
              'commands.json',
              'user.json']
DICT_PATH = 'plover/assets/'


def test_no_duplicates_categorized_files():
    d = defaultdict(list)
    dictionary = None
    def read_key_pairs(pairs):
        for key, value in pairs:
            d[key].append((value, dictionary))
        return d
    for dictionary in map(lambda x: DICT_PATH + x, DICT_NAMES):
        with io.open(dictionary, encoding='utf-8') as fp:
            json.load(fp, object_pairs_hook=read_key_pairs)
    msg_list = []
    has_duplicate = False
    for key, value_list in d.items():
        if len(value_list) > 1:
            has_duplicate = True
            msg_list.append('key: %s\n' % key)
            for value in value_list:
                msg_list.append('%r in %s\n' % value)
    msg = '\n' + ''.join(msg_list)
    assert not has_duplicate, msg


@pytest.mark.parametrize('dictionary', DICT_NAMES)
def test_entries_are_valid(dictionary):
    with io.open(DICT_PATH + dictionary, encoding='utf-8') as fp:
        for k, v in json.load(fp).items():
            [steno_to_stroke(s) for s in k.split('/')]
