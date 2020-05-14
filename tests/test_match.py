import pathmagic  # noqa
from luxor.core.match import match

SET_X_T0 = 'test[0].x.int.set'
GET_X_T0 = 'test[0].x.int.get'
GET_X_T1 = 'test[1].x.int.get'
SET_Y_T0 = 'test[0].y.int.set'
GET_Y_T0 = 'test[0].y.int.get'
GET_Y_T1 = 'test[1].y.int.get'


def test_match_any():
    assert match(SET_X_T0, '*')
    assert match(GET_X_T0, '*')
    assert match(GET_X_T1, '*')
    assert match(GET_Y_T0, '*')


def test_match_x():
    assert match(SET_X_T0, 'x')
    assert match(GET_X_T0, 'x')
    assert not match(SET_Y_T0, 'x')
    assert not match(GET_Y_T0, 'x')


def test_match_get():
    assert match(GET_X_T0, '*.get')
    assert match(GET_Y_T0, '*.get')
    assert not match(SET_X_T0, '*.get')
    assert not match(SET_Y_T0, '*.get')
