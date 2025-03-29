import itertools
from collections import namedtuple
from collections.abc import Collection, Sequence
from datetime import UTC, datetime
from ipaddress import ip_address

from cryptography.x509 import DNSName, IPAddress, load_der_x509_certificate
from cryptography.x509.verification import (
    ClientVerifier,
    PolicyBuilder,
    ServerVerifier,
    Store,
    VerificationError,
)

import siotls.trust
from siotls.connection import TLSConnection
from siotls.contents import alerts
from siotls.contents.handshakes.certificate import X509Entry
from siotls.x509.load import DerCertificate

Entry = namedtuple('Entry', ('cryptocert', 'certificate', 'extensions'))


class X509Verifier(siotls.trust.X509Verifier):
   def __init__(
     self,
     der_ca_certificates: Collection[DerCertificate],
     network_service: siotls.trust.net.NetworkService | None,
   ):
      self._store = Store([
         load_der_x509_certificate(der_cert)
         for der_cert in der_ca_certificates
      ])
      self._policy_builder = PolicyBuilder().store(self._store)
      self.network_service = network_service

   def verify_chain(self, conn: TLSConnection, entry_chain: Sequence[X509Entry]):
      cert_chain = [
         load_der_x509_certificate(entry.certificate)
         for entry in entry_chain
      ]

      if conn.config.other_side == 'client':
         verifier = self._build_client_verifier()
      else:
         try:
            server_ip = ip_address(conn.server_hostname)
         except ValueError:
            subject = DNSName(conn.server_hostname)
         else:
            subject = IPAddress(server_ip)
         verifier = self._build_server_verifier(subject)

      try:
         result = verifier.verify(cert_chain[0], cert_chain[1:])
      except VerificationError as exc:
         raise alerts.BadCertificate from exc

      entry_chain = self._reorder(
         entry_chain,
         cert_chain,
         result.chain if conn.config.other_side == 'client' else result,
      )
      for subject, issuer in itertools.pairwise(entry_chain):
         # TODO: don't depend on siotls_X509Verifier
         from siotls.trust.providers.siotls import X509Verifier as siotls_X509Verifier
         siotls_X509Verifier.verify_online_status(
            self, subject, issuer
         )

   def _build_client_verifier(self) -> ClientVerifier:
      # override me if you want another policy
      return self._policy_builder.time(datetime.now(UTC)).build_client_verifier()

   def _build_server_verifier(self, subject) -> ServerVerifier:
      # override me if you want another policy
      return self._policy_builder.time(datetime.now(UTC)).build_server_verifier(subject)

   def _reorder(self, entry_chain, cert_chain, ordered_cert_chain):
      pairs = [
         (entry, cert)
         for (entry, cert)
         in zip(entry_chain, cert_chain, strict=True)
         if cert in ordered_cert_chain
      ]
      pairs.sort(key=lambda pair: ordered_cert_chain.index(pair[1]))
      return [entry for entry, _ in pairs]
