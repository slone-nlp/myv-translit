from myv_translit import cyr2lat, lat2cyr, detect_script


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


def test_detection():
    assert detect_script('123 456?? 8743 098543 ???...,.! @%%&&& хз') == 'unk'
    assert detect_script('ěrzä') == 'lat'
    assert detect_script('ěrzä ю') == 'lat'
    assert detect_script('ЭРЗЯ') == 'cyr'
    assert detect_script('ЭРЗЯ d') == 'cyr'
    assert detect_script('ěrzä эрзянь') == 'mix'


def test_lat2cyr_edge_cases():
    assert lat2cyr('bažaś velävtoms dy muems ěstenzě jon tarka') == 'бажась велявтомс ды муемс эстензэ ён тарка'


def test_consistency():
    with open('examples/zontik_cyr.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    lines = [line for line in lines if line]
    assert len(lines) > 40
    for line_cyr in lines:
        line_lat = cyr2lat(line_cyr)
        line_cyr2 = lat2cyr(line_lat)
        assert line_cyr == line_cyr2

