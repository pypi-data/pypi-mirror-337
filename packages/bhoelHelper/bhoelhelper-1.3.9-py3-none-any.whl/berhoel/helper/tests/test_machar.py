"""Testing `berhoel.helper.machar`."""

from berhoel.helper import machar


def test_ibeta():
    assert isinstance(machar.ibeta, int)


def test_it():
    assert isinstance(machar.it, int)


def test_irnd():
    assert isinstance(machar.irnd, int)


def test_ngrd():
    assert isinstance(machar.ngrd, int)


def test_machdep():
    assert isinstance(machar.machdep, int)


def test_negep():
    assert isinstance(machar.negep, int)


def test_iexp():
    assert isinstance(machar.iexp, int)


def test_minexp():
    assert isinstance(machar.minexp, int)


def test_maxexp():
    assert isinstance(machar.maxexp, int)


def test_eps():
    assert isinstance(machar.eps, float)


def test_epsneg():
    assert isinstance(machar.epsneg, float)


def test_xmin():
    assert isinstance(machar.xmin, float)


def test_xmax():
    assert isinstance(machar.xmax, float)
