"""Testes da funcao parse_target. Rodar com: pytest"""

from shadowaudit.utils.net import parse_target


def test_url_https():
    host, usa_https = parse_target("https://exemplo.com")
    assert host == "exemplo.com"
    assert usa_https is True


def test_url_http():
    host, usa_https = parse_target("http://exemplo.com")
    assert host == "exemplo.com"
    assert usa_https is False


def test_hostname_puro_assume_https():
    host, usa_https = parse_target("exemplo.com")
    assert host == "exemplo.com"
    assert usa_https is True
