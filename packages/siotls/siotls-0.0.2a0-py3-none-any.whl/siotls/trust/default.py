import importlib
from threading import RLock

_lock = RLock()

_store = None
def get_default_store():
    global _store  # noqa: PLW0603
    from . import castore

    if _store:
        return _store
    with _lock:
        if _store:
            return _store
        try:
            _store = castore.get_system_ca_certificates()
        except RuntimeError:
            try:
                _store = castore.get_certifi_store()
            except ImportError:
                pass
            else:
                return _store
            raise
        return _store


_net = None
def get_default_net():
    global _net  # noqa: PLW0603
    from .net.providers.basic import NSThread

    if not _net:
        with _lock:
            if not _net:
                _net = NSThread()
    return _net


_trust = None
def get_default_trust():
    global _trust  # noqa: PLW0603
    try:
        importlib.import_module('cryptography')
    except ImportError:
        from .providers.siotls import X509Verifier
    else:
        from .providers.openssl import X509Verifier

    if not _trust:
        with _lock:
            if not _trust:
                _trust = X509Verifier(get_default_store(), get_default_net())
    return _trust
