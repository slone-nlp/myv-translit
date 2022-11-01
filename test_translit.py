from myv_translit import cyr2lat


def test_join_acute():
    assert cyr2lat('кель') == 'keĺ'
    assert cyr2lat('кель', joint_acute=False) == 'keĺ'
    assert len(cyr2lat('кель')) == 3
    assert len(cyr2lat('кель', joint_acute=False)) == 4


def test_first_e():
    assert cyr2lat('эрзя') == 'ěrzä'
    assert cyr2lat('эрзя', first_e_with_hacek=False) == 'erzä'


def test_soft_l():
    assert cyr2lat('пелькс') == 'peĺks'
    assert cyr2lat('пелькс', soft_l_after_vowels=False) == 'pelks'


# todo: test on a larger corpus
# todo: test cyclical consistency

