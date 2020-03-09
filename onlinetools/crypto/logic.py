from datetime import datetime

from OpenSSL import crypto


def delimit_hex(hex_str: str, delimit_by: int = 2, delimit_char: str = ':') -> str:
    return delimit_char.join([hex_str[i:i+delimit_by] for i in range(0, len(hex_str), delimit_by)])


def format_components(components: list) -> str:
    return ', '.join(['='.join([part.decode('utf-8') for part in component]) for component in components])


def parse_certificate(cert) -> dict:
    result = {}
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    result['version'] = int(x509.get_version()) + 1
    result['version_hex'] = hex(x509.get_version())
    result['serial'] = delimit_hex(f'{x509.get_serial_number():x}')
    result['signature_algorithm'] = x509.get_signature_algorithm().decode('utf-8')
    result['issuer'] = format_components(x509.get_issuer().get_components())
    result['valid_not_before'] = datetime.strptime(x509.get_notBefore().decode('utf-8')[:-1], '%Y%m%d%H%M%S')
    result['valid_not_after'] = datetime.strptime(x509.get_notAfter().decode('utf-8')[:-1], '%Y%m%d%H%M%S')
    result['subject'] = format_components(x509.get_subject().get_components())
    result['ext'] = []
    if x509.get_extension_count() > 0:
        for i in range(x509.get_extension_count()):
            ext = x509.get_extension(i)
            result['ext'].append({'name': ext.get_short_name().decode('utf-8'),
                                  'critical': bool(ext.get_critical()),
                                  'data': str(ext)})
    return result
