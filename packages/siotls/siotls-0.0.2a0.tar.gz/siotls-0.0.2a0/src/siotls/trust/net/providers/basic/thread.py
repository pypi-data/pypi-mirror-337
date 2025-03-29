from concurrent.futures import ThreadPoolExecutor

from .iterative import NSIterative


class NSThread(NSIterative):
    def __init__(
        self,
        max_workers=None,
        thread_name_prefix='',
        initializer=None,
        initargs=(),
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pool = ThreadPoolExecutor(max_workers, thread_name_prefix, initializer, initargs)

    def download_cert(self, url):
        return self.pool.submit(super().download_cert, url).result()

    def download_crl(self, url):
        return self.pool.submit(super().download_crl, url).result()

    def download_ocsp(self, url, ocsp_req_data):
        return self.pool.submit(super().download_ocsp, url, ocsp_req_data).result()
