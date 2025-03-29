import socket
import subprocess as sp
import sys
import unittest
from os import fspath

from parameterized import parameterized

from . import TAG_EXTERNAL, TAG_INTEGRATION, TestCase, test_temp_dir


class TestExample(TestCase):
    @unittest.skipUnless(TAG_INTEGRATION, "enable with SIOTLS_INTEGRATION=1")
    def test_simple_client_server(self):
        # get an ephemeral free port
        with socket.create_server(('::1', 0), family=socket.AF_INET6, backlog=0) as sock:
            port = sock.getsockname()[1]

        server = self.popen(
            [
                sys.executable, '-m', 'siotls',
                'server',
                '--host', '::1',
                '--port', str(port),
                '--tlscert', fspath(test_temp_dir/'server-cert.pem'),
                '--tlskey', fspath(test_temp_dir/'server-privkey.pem'),
            ],
            stderr=sp.PIPE,
            text=True,
        )

        server_stderr_sel = self.selector(server.stderr)
        server_stderr_sel.select(timeout=.1)
        self.assertEqual(
            server.stderr.readline().removeprefix("INFO:siotls.examples.simple_server:"),
            f"serving http on ::1 port {port} (https://[::1]:{port})\n"
        )

        client = self.popen(
            [
                sys.executable, '-m', 'siotls',
                'client',
                '--host', '::1',
                '--port', str(port),
                '--insecure',
            ],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            text=True,
        )
        client.wait(timeout=1)
        server.terminate()
        server.wait(timeout=1)

        client_stdout, client_stderr = client.communicate(None, 1)
        _, server_stderr = server.communicate(None, 1)
        try:
            self.assertEqual(client_stdout, "Hello from siotls\n\n")
            for line, expected_line in zip(client_stderr.splitlines(), [
                "WARNING:siotls.configuration:missing x509verifier or list of trusted public "
                    "keys, will not verify the peer's certificate",
                f"INFO:siotls.examples.simple_client:connection with [::1]:{port} established",
                f"INFO:siotls.examples.simple_client:connection with [::1]:{port} secured",
                f"INFO:siotls.examples.simple_client:connection with [::1]:{port} closed",
            ], strict=True):
                self.assertEqual(line, expected_line)
            module = r"siotls\.examples\.simple_server"
            for line, regex in zip(server_stderr.splitlines(), [
                fr"^INFO:{module}:connection with \[::1\]:\d+ established$",
                fr"^INFO:{module}:connection with \[::1\]:\d+ secured$",
                fr'^INFO:{module}:::1 - - \[.*?\] "GET / HTTP/1\.1" 200 18$',
                fr"^INFO:{module}:connection with \[::1\]:\d+ closed$",
            ], strict=True):
                self.assertRegex(line, regex)
        except AssertionError as exc:
            complete_output = ("\n"
               f"client stdout:\n{client_stdout}\n"
               f"client stderr:\n{client_stderr}\n"
               f"server stderr:\n{server_stderr}\n"
            )
            raise AssertionError(complete_output) from exc

        self.assertFalse(client.returncode, "client exited by itself")
        self.assertTrue(server.returncode, "server was killed")

    @parameterized.expand(['example.com', 'drlazor.be'])
    @unittest.skipUnless(TAG_EXTERNAL, "enable with SIOTLS_EXTERNAL=1")
    def test_website(self, hostname):
        client = self.popen(
            [
                sys.executable, '-m', 'siotls',
                'client',
                '--host', hostname,
                '--port', '443',
                '-v', '--keylogfile', fspath(test_temp_dir/'keylogfile'),
            ],
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            text=True,
        )
        stdout, stderr = client.communicate(None, timeout=5)
        self.assertFalse(client.returncode, '\n' + stderr)
