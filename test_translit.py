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


DEFAULT_TEST_SET = [
    ("съёмка", "sjomka"),  # ъё
    ('бажась велявтомс ды муемс эстензэ ён тарка', 'bažaś velävtoms dy muems ěstenzě jon tarka'),
    ('УЖОСТО УЖОС ИДЕМЕВСТЬ ПАНСЯН!', 'UŽOSTO UŽOS IDEMEVSŤ PANSÄN!'),  # upper Ь
    ('ПЬЯНСТВО', 'ṔJANSTVO'),  # also upper Ь
    ('райононть', 'rajononť'),  # special case
    # TODO: FIXME ('XVIII пингень', 'XVIII pingeń'),  # consistency
]


def test_edge_cases():
    for cyr, lat in DEFAULT_TEST_SET:
        assert cyr2lat(cyr) == lat
        assert lat2cyr(lat) == cyr


def test_consistency():
    with open('examples/zontik_cyr.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    lines = [line for line in lines if line]
    assert len(lines) > 40
    for line_cyr in lines:
        line_lat = cyr2lat(line_cyr)
        line_cyr2 = lat2cyr(line_lat)
        assert line_cyr == line_cyr2

    for line_cyr in lines:
        line_lat = cyr2lat(line_cyr, joint_acute=False)
        line_cyr2 = lat2cyr(line_lat, joint_acute=False)
        assert line_cyr == line_cyr2

    for line_cyr in lines:
        line_lat = cyr2lat(line_cyr, soft_l_after_vowels=False)
        line_cyr2 = lat2cyr(line_lat, soft_l_after_vowels=False)
        assert line_cyr == line_cyr2

    for line_cyr in lines:
        if ' ежос' in line_cyr:  # normally, this does not happen in the Erzya language
            continue
        line_lat = cyr2lat(line_cyr, first_e_with_hacek=False)
        line_cyr2 = lat2cyr(line_lat, first_e_with_hacek=False)
        assert line_cyr == line_cyr2


def test_zontik():
    with open('examples/zontik_cyr.txt', 'r') as f:
        lines_cyr = [line.strip() for line in f.readlines()]
    lines_cyr = [line for line in lines_cyr if line]
    with open('examples/zontik_lat.txt', 'r') as f:
        lines_lat = [line.strip() for line in f.readlines()]
    lines_lat = [line for line in lines_lat if line]
    assert len(lines_cyr) == len(lines_lat)
    for line_cyr, line_lat in zip(lines_cyr, lines_lat):
        assert line_lat == cyr2lat(line_cyr)
        assert line_cyr == lat2cyr(line_lat)


def get_inconsistent_pairs():
    try:
        from datasets import load_dataset
    except ImportError:
        return
    dev = load_dataset('slone/myv_ru_2022', split='validation')
    with open('examples/mismatches.txt', 'w') as f:
        for line_cyr in dev['myv']:
            line_lat = cyr2lat(line_cyr)
            line_cyr2 = lat2cyr(line_lat)
            if line_cyr != line_cyr2:
                print(line_cyr, file=f)
                print(line_cyr2, file=f)
                print(line_lat, file=f)
                print(file=f)
