"""
test_db
~~~~~~~

Unit tests for :mod:`charex.db`.
"""
from dataclasses import dataclass
from pathlib import Path

import pytest

from charex import db


@pytest.fixture
def denormal_path():
    """Path to the Denormal.zip file."""
    return 'v14_0/Denormal.zip'


@pytest.fixture
def path_map_default(mocker):
    path = Path('tests/data/test_path_map.json')
    mocker.patch('charex.db.get_path_map_file', return_value=path)
    """A path map with some default values and some overridden values."""
    data = {
        'spam': [
            'spam.txt',
            'old/EGGS.zip',
            'spam',
            ';',
        ],
        'bacon': [
            'bacon.txt',
            'old/EGGS.zip',
            'bacon',
            ';',
        ],
    }
    return {k: db.PathInfo(*data[k]) for k in data}


@pytest.fixture
def path_map_version(mocker):
    path = Path('tests/data/test_path_map.json')
    mocker.patch('charex.db.get_path_map_file', return_value=path)
    """A path map with some default values and some overridden values."""
    data = {
        'spam': [
            'spam.txt',
            'old/EGGS.zip',
            'spam',
            ';',
        ],
        'bacon': [
            'bacon.txt',
            'new/EGGS.zip',
            'bacon',
            ';',
        ],
        'bakedbeans': [
            'bakedbeans.txt',
            'new/EGGS.zip',
            'bakedbeans',
            ';',
        ],
    }
    return {k: db.PathInfo(*data[k]) for k in data}


@pytest.fixture
def ucd_path():
    """Path to the UCD.zip file."""
    return 'v14_0/UCD.zip'


@pytest.fixture
def uhn_path():
    """Path to the default Unihan.zip file."""
    return 'v14_0/Unihan.zip'


# Test alias_property.
def test_alias_property():
    """Given the long name for a property, return the alias of that
    property if it exists. If it doesn't exist, return the long name.
    """
    assert db.alias_property('General_Category') == 'gc'
    assert db.alias_property('spam') == 'spam'


def test_alias_value():
    """Given a property alias and the long name for a value of that
    property, return the alias of that value if it exists. If
    it doesn't exist, return the long name.
    """
    assert db.alias_value('gc', 'Letter') == 'L'
    assert db.alias_value('spam', 'eggs') == 'eggs'


# Test build_hangul_name.
def test_build_hangul_name():
    """When given a code point for a Hangul syllable,
    :func:`charex.db.build_jame_name` should return the Jamo
    name for that code point.
    """
    assert db.build_hangul_name('d4db') == 'PWILH'


# Test cache.
class TestCache:
    def test_cache(self):
        """When called, an attribute of :class:`FileCache` should return
        the data for the file tied to that attribute.
        """
        assert db.cache.blocks[0].start == 0x0000
        assert '0958' in db.cache.compositionexclusions
        assert '0340' in db.cache.derivednormalizationprops[1]['comp_ex']
        assert db.cache.jamo['1100'] == 'G'
        assert '0009' in db.cache.proplist['wspace']
        assert db.cache.unicodedata['0020'].na == 'SPACE'
        assert db.cache.rev_nfc['00c0'] == ('A\u0300',)

    def test_with_python_version(self):
        """When given a Python version, db.FileCache.from_python
        should return a FileCache with the correct version of
        Unicode for that version of Python.
        """
        @dataclass
        class Version_Info:
            major: int
            minor: int

        version = Version_Info(3, 12)
        cache = db.FileCache.from_python(version)
        assert cache.version == 'v15_0'

        version = Version_Info(3, 13)
        cache = db.FileCache.from_python(version)
        assert cache.version == 'v15_1'

    def test_with_higher_than_supported_version(self):
        """If given a version of python higher than the highest
        currently supported version, db.FileCache.from_python
        should return a FileCache object supporting the highest
        currently supported version of Unicode."""
        @dataclass
        class Version_Info:
            major: int
            minor: int

        version = Version_Info(3, 6_000_000)
        cache = db.FileCache.from_python(version)
        assert cache.version == 'v15_1'


# Test get_denormal_map_for_code.
def test_get_denormal_map_for_code():
    """Given a property and a code point,
    :func:`charex.db.get_denormal_map_for_code` should
    return the value for that property for the code point.
    """
    code = '0020'
    assert db.get_denormal_map_for_code('rev_nfc', code) == ()

    code = '00c5'
    assert db.get_denormal_map_for_code('rev_nfc', code) == (
        'A\u030a', '\u212b',
    )


# Test get_named_sequences:
def test_get_named_sequences():
    """When called, :funct:`charex.db.get_named_sequences` returns the list
    of named sequences.
    """
    data = db.get_named_sequences()
    assert data[0] == db.NamedSequence(
        'KEYCAP NUMBER SIGN',
        '0023 FE0F 20E3'
    )


# Test get_standardized_variants:
def test_get_standardized_variants():
    """When called, :funct:`charex.db.get_standardized_variants` returns
    the mapping of standardized variants.
    """
    data = db.get_standardized_variant()
    assert data[0] == db.Variant(
        '0030 FE00', 'short diagonal stroke form', ''
    )


# Test get_value_for_code.
def test_get_value_for_code():
    """Given a property and a code point,
    :func:`charex.db.get_value_for_code` should
    return the value for that property for the
    code point.
    """
    code = '0020'
    assert db.get_value_for_code('na', code) == 'SPACE'
    assert db.get_value_for_code('scx', code) == 'Zyyy'
    assert db.get_value_for_code('age', code) == '1.1'
    assert db.get_value_for_code('blk', code) == 'Basic Latin'
    assert db.get_value_for_code('emoji', code) == 'N'
    assert db.get_value_for_code('ce', code) == 'N'
    assert db.get_value_for_code('comp_ex', code) == 'N'
    assert db.get_value_for_code('cjkirg_gsource', code) == ''
    assert db.get_value_for_code('cf', code) == '0020'
    assert db.get_value_for_code('lc', code) == ''
    assert db.get_value_for_code('bpb', code) == '<none>'
    assert db.get_value_for_code('cjkradical', code) == ''
    assert db.get_value_for_code('name_alias', code) == '<abbreviation>SP'
    assert db.get_value_for_code('ktgt_mergedsrc', code) == ''
    assert db.get_value_for_code('kddi', code) == ''

    code = '1f600'
    assert db.get_value_for_code('emoji', code) == 'Y'

    code = '0958'
    assert db.get_value_for_code('ce', code) == 'Y'

    code = '0340'
    assert db.get_value_for_code('comp_ex', code) == 'Y'

    code = '3400'
    assert db.get_value_for_code('cjkirg_gsource', code) == 'GKX-0078.01'

    code = 'fb00'
    assert db.get_value_for_code('tc', code) == '0046 0066'

    code = '0028'
    assert db.get_value_for_code('bpb', code) == '0029'

    code = '2f00'
    assert db.get_value_for_code('cjkradical', code) == '1'

    code = '0000'
    assert db.get_value_for_code('name_alias', code) == (
        '<control>NULL <abbreviation>NUL'
    )

    code = '17000'
    assert db.get_value_for_code('ktgt_mergedsrc', code) == 'L2008-0008'

    code = '1f6c0'
    assert db.get_value_for_code('kddi', code) == 'F34B'


# Test load_bidi_brackets.
def test_load_bidi_brackets(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_bidi_brackets` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'BidiBrackets.txt', ucd_path, 'bidi_brackets', ';'
    )
    data = db.load_bidi_brackets(pi)
    assert data['0028'] == db.BidiBracket('0028', '0029', 'o')
    assert data['ff63'] == db.BidiBracket('FF63', 'FF62', 'c')


# Test load_casefolding.
def test_load_casefolding(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_casefolding` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'CaseFolding.txt', ucd_path, 'casefolding', ';'
    )
    data = db.load_casefolding(pi)
    assert data['0041'] == db.Casefold('0061', '<code>', '<code>', '<code>')
    assert data['0049'] == db.Casefold('0069', '<code>', '<code>', '0131')
    assert data['1e921'] == db.Casefold('1E943', '<code>', '<code>', '<code>')


# Test load_cjk_radicals.
def test_load_cjk_radicals(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_cjk_radicals` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'CJKRadicals.txt', ucd_path, 'cjk_radicals', ';'
    )
    data = db.load_cjk_radicals(pi)
    assert data['2f00'] == db.Radical('1', '2F00', '4E00')
    assert data['2ee2'] == db.Radical('187\'', '2EE2', '9A6C')
    assert data['9fa0'] == db.Radical('214', '2FD5', '9FA0')


# Test load_derived_normal.
def test_load_derived_normal(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_derived_normal` should return the data
    contained within the path as a :class:`tuple`.
    """
    pi = db.PathInfo(
        'DerivedNormalizationProps.txt', ucd_path, 'derived_normal', ';'
    )
    single, simple = db.load_derived_normal(pi)
    assert single['fc_nfkc']['037a'] == '0020 03B9'
    assert single['nfkc_cf']['e0fff'] == ''
    assert '0340' in simple['comp_ex']
    assert 'e0fff' in simple['cwkcf']


# Test load_denormal_map.
def test_load_denormal_map(denormal_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_denormal_map` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'rev_nfc.json', denormal_path, 'denormal_map', ''
    )
    data = db.load_denormal_map(pi)
    assert data['00c0'] == ('A\u0300',)
    assert data['00c5'] == ('A\u030a', '\u212b')
    assert data['2a600'] == ('\U0002fa1d',)


# Test load_emoji_source.
def test_load_emoji_source(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_emoji_source` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'EmojiSources.txt', ucd_path, 'emoji_source', ';'
    )
    data = db.load_emoji_source(pi)
    assert data['0023 20e3'] == db.EmojiSource(
        '0023 20E3', 'F985', 'F489', 'F7B0'
    )
    assert data['1f6c0'] == db.EmojiSource('1F6C0', '', 'F34B', 'F780')


# Test load_entity_map.
def test_load_entity_map():
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_entity_map` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'entities.json', '', 'entity_map', ''
    )
    data = db.load_entity_map(pi)
    assert data['00c6'] == (
        db.Entity('&AElig', ('00c6',), '\u00c6'),
        db.Entity('&AElig;', ('00c6',), '\u00c6'),
    )
    assert data['200c'] == (
        db.Entity('&zwnj;', ('200c',), '\u200c'),
    )


# Test load_from_archive.
def test_load_from_archive(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, return the lines contained in the file as a :class:`tuple`.
    """
    pi = db.PathInfo('Jamo.txt', ucd_path, 'single_value', ';')
    lines = db.load_from_archive(pi)
    assert lines[0] == '# Jamo-14.0.0.txt'
    assert lines[-1] == '# EOF'


# Test load_name_alias.
def test_load_name_alias(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_name_alias` should return the data
    contained within the path as a :class:`set`.
    """
    pi = db.PathInfo(
        'NameAliases.txt', ucd_path, 'simple_list', ';'
    )
    data = db.load_name_alias(pi)
    assert data['0000'] == (
        db.NameAlias('0000', 'NULL', 'control'),
        db.NameAlias('0000', 'NUL', 'abbreviation'),
    )
    assert data['e01ef'] == (
        db.NameAlias('E01EF', 'VS256', 'abbreviation'),
    )


# Test load_named_sequence.
def test_load_named_sequence(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_named_sequence` should return the data
    contained within the path as a :class:`set`.
    """
    pi = db.PathInfo(
        'NamedSequences.txt', ucd_path, 'named_sequence', ';'
    )
    data = db.load_named_sequence(pi)
    assert data['keycap number sign'] == db.NamedSequence(
        'KEYCAP NUMBER SIGN',
        '0023 FE0F 20E3'
    )
    assert data[
        'modifier letter extra-low extra-high contour tone bar'
    ] == db.NamedSequence(
        'MODIFIER LETTER EXTRA-LOW EXTRA-HIGH CONTOUR TONE BAR',
        '02E9 02E5'
    )


# Test load_path_map.
class TestLoadPathMap:
    def test_load_path_map(self, ucd_path):
        """When called, :func:`charex.db.load_path_map` should return a
        :class:`dict` that allows mapping of a Unicode file name to the
        archive that contains it.
        """
        exp = ucd_path
        path = 'unicodedata'
        pm = db.load_path_map(version='v14_0')
        pi = pm[path]
        assert pi.archive == exp

    def test_load_default(self, path_map_default):
        """When called without a version, charex.db.load_path_map
        should return the default path information.
        """
        assert db.load_path_map() == path_map_default

    def test_load_version(self, path_map_version):
        """When called without a version, charex.db.load_path_map
        should return the default path information.
        """
        assert db.load_path_map('tomato') == path_map_version


# Test load_prop_list.
def test_load_prop_list(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_prop_list` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'PropList.txt', ucd_path, 'prop_list', ';'
    )
    data = db.load_prop_list(pi)
    assert '0000' not in data['wspace']
    assert '0009' in data['wspace']
    assert '1f1ff' in data['ri']
    assert '10ffff' not in data['ri']


# Test load_property_alias.
def test_load_property_alias(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_property_alias` should return the data
    contained within the path as a :class:`set`.
    """
    pi = db.PathInfo(
        'PropertyAliases.txt', ucd_path, 'property_alias', ';'
    )
    data = db.load_property_alias(pi)
    assert data['kaccountingnumeric'].alias == 'cjkAccountingNumeric'
    assert data['expands_on_nfkd'].alias == 'XO_NFKD'


# Test load_simple_list.
def test_load_simple_list(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_simple_list` should return the data
    contained within the path as a :class:`set`.
    """
    pi = db.PathInfo(
        'CompositionExclusions.txt', ucd_path, 'simple_list', ';'
    )
    data = db.load_simple_list(pi)
    assert '0000' not in data
    assert '0958' in data
    assert '1d1c0' in data
    assert '10FFFF' not in data


# Test load_single_value.
def test_load_single_value(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_single_value` should return the data
    contained within the path as a :class:`collections.defaultdict`.
    """
    pi = db.PathInfo('Jamo.txt', ucd_path, 'single_value', ';')
    data = db.load_single_value(pi)
    assert data['1100'] == 'G'
    assert data['11c2'] == 'H'
    assert data['0041'] == ''


# Test load_special_casing:.
def test_load_special_casing(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_special_casing` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo('SpecialCasing.txt', ucd_path, 'special_casing', ';')
    data = db.load_special_casing(pi)
    assert data['fb00'].code == 'FB00'
    assert data['0069'].condition_list == 'az'


# Test load_standardized_variant:.
def test_load_standardized_variant(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_standardized_variant` should return the
    data contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo(
        'StandardizedVariants.txt', ucd_path, 'standard_variant', ';'
    )
    data = db.load_standardized_variant(pi)
    assert data['0030 fe00'] == db.Variant(
        '0030 FE00', 'short diagonal stroke form', ''
    )
    assert data['2a600 fe00'] == db.Variant(
        '2A600 FE00', 'CJK COMPATIBILITY IDEOGRAPH-2FA1D', ''
    )


# Test load_unihan.
def test_load_unihan(uhn_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_unihan` should return the data
    contained within the path as a :class:`collections.defaultdict`.
    """
    pi = db.PathInfo(
        'Unihan_IRGSources.txt', uhn_path, 'single_value', '\t'
    )
    data = db.load_unihan(pi)
    assert data['cjkirg_gsource']['3400'] == 'GKX-0078.01'
    assert data['ktotalstrokes']['3134a'] == '22'


# Test load_unicode_data.
def test_load_unicode_data(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_unicode_data` should return the data
    contained within the path as a :class:`dict`.
    """
    pi = db.PathInfo('UnicodeData.txt', ucd_path, 'unicode_data', ';')
    data = db.load_unicode_data(pi)
    assert data['0000'].code == '0000'
    assert data['10fffd'].code == '10FFFD'
    assert data['2a701'].na == 'CJK UNIFIED IDEOGRAPH-2A701'
    assert data['d4db'].na == 'HANGUL SYLLABLE PWILH'


# Test load_value_aliases.
def test_load_value_aliases(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_value_aliases` should return the data
    contained within the path as a :class:`collections.dict`.
    """
    pi = db.PathInfo('PropertyValueAliases.txt', ucd_path, '', ';')
    data = db.load_value_aliases(pi)
    assert data['ahex']['no'].alias == 'N'
    assert data['xids']['no'].alias == 'N'


# Test load_value_range.
def test_load_value_range(ucd_path):
    """When given the information for a path as a :class:`charex.db.PathInfo`
    object, :func:`charex.db.load_value_range` should return the data
    contained within the path as a :class:`tuple`.
    """
    pi = db.PathInfo('Blocks.txt', ucd_path, 'value_range', ';')
    data = db.load_value_range(pi)
    assert data[0] == db.ValueRange(0x0000, 0x0080, 'Basic Latin')
    assert data[-1] == db.ValueRange(
        0x100000, 0x110000, 'Supplementary Private Use Area-B'
    )
    assert data[106] == db.ValueRange(0x2fe0, 0x2ff0, 'No_Block')
