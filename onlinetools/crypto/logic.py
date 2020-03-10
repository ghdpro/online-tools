from datetime import datetime
import socket
import ssl

from OpenSSL import crypto


def delimit_hex(hex_str: str, delimit_by: int = 2, delimit_char: str = ':') -> str:
    return delimit_char.join([hex_str[i:i+delimit_by] for i in range(0, len(hex_str), delimit_by)])


def component_dict(components: list) -> dict:
    return {key.decode('utf-8'): value.decode('utf-8') for key, value in [component for component in components]}


def get_certificate_from_host(host: str, server: str = None, port: int = 443) -> str:
    raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.SSLContext()
    ssl_socket = ssl_context.wrap_socket(raw_socket, server_hostname=host)
    if server is None:
        server = host
    ssl_socket.connect((server, port))
    der = ssl_socket.getpeercert(True)
    return ssl.DER_cert_to_PEM_cert(der)


def parse_certificate(data) -> dict:
    result = {}
    raw = {}
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, data)
    raw['version'] = int(x509.get_version()) + 1
    raw['version_hex'] = hex(x509.get_version())
    result['serial'] = raw['serial'] = delimit_hex(f'{x509.get_serial_number():x}')
    raw['signature_algorithm'] = x509.get_signature_algorithm().decode('utf-8')
    raw['issuer'] = component_dict(x509.get_issuer().get_components())
    if 'O' in raw['issuer']:
        result['issuer'] = raw['issuer']['O']
    result['valid_not_before'] = raw['valid_not_before'] = \
        datetime.strptime(x509.get_notBefore().decode('utf-8')[:-1], '%Y%m%d%H%M%S')
    result['valid_not_after'] = raw['valid_not_after'] = \
        datetime.strptime(x509.get_notAfter().decode('utf-8')[:-1], '%Y%m%d%H%M%S')
    result['has_expired'] = raw['has_expired'] = x509.has_expired()
    raw['subject'] = component_dict(x509.get_subject().get_components())
    if 'O' in raw['subject']:
        result['subject'] = raw['subject']['O']
    if 'CN' in raw['subject']:
        result['common_name'] = raw['subject']['CN']
    raw['ext'] = []
    if x509.get_extension_count() > 0:
        for i in range(x509.get_extension_count()):
            ext = x509.get_extension(i)
            ext_data = {'name': ext.get_short_name().decode('utf-8'),
                        'critical': bool(ext.get_critical()),
                        'data': str(ext)}
            if ext_data['name'] == 'subjectAltName':
                result['subject_alt_name'] = ext_data['data'].strip().replace('DNS:', '')
            raw['ext'].append(ext_data)
    result['raw'] = raw
    return result
