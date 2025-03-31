# coding:utf-8

from enum import Enum

from requests import Session


class ProxyProtocol(Enum):
    HTTP = "http"
    HTTPS = "https"
    SOCKS4 = "socks4"
    SOCKS5 = "socks5"


class ProxySession(Session):

    def __init__(self, protocol: ProxyProtocol, host: str, port: int):
        if not isinstance(protocol, ProxyProtocol):
            raise ValueError(f"Invalid proxy protocol: {protocol}")
        proxies = {
            "http": f"{protocol.value}://{host}:{port}",
            "https": f"{protocol.value}://{host}:{port}",
        }
        super(ProxySession, self).__init__()  # pylint: disable=R1725
        self.proxies.update(proxies)

    @classmethod
    def http_proxy(cls, host: str, port: int = 80) -> "ProxySession":
        return cls(ProxyProtocol.HTTP, host, port)

    @classmethod
    def https_proxy(cls, host: str, port: int = 443) -> "ProxySession":
        return cls(ProxyProtocol.HTTPS, host, port)

    @classmethod
    def socks4_proxy(cls, host: str, port: int = 1080) -> "ProxySession":
        return cls(ProxyProtocol.SOCKS4, host, port)

    @classmethod
    def socks5_proxy(cls, host: str, port: int = 1080) -> "ProxySession":
        return cls(ProxyProtocol.SOCKS5, host, port)
