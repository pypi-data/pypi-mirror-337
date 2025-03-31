from ssh_keyconv.cli import *

from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption

def test_apply_encoding_format_corrections():
    INPUT_ENCODING_CORRECTIONS = {
        (Encoding.PEM, PrivateFormat.OpenSSH):
            (Encoding.OpenSSH, PrivateFormat.OpenSSH)
    }

    # A mapped entry should be returned
    assert apply_encoding_format_corrections(
        INPUT_ENCODING_CORRECTIONS, Encoding.PEM, PrivateFormat.OpenSSH) \
            == (Encoding.OpenSSH, PrivateFormat.OpenSSH)
    
    # A missing entry should be returned unchanged
    assert apply_encoding_format_corrections(
        INPUT_ENCODING_CORRECTIONS, Encoding.PEM, PrivateFormat.PKCS8) \
            == (Encoding.PEM, PrivateFormat.PKCS8)


def test_validate_output_encoding_format():
    PERMITTED_OUTPUT_ENCODING_FORMATS = {
        Encoding.PEM: [PrivateFormat.OpenSSH,
                       PrivateFormat.PKCS8,
                       PrivateFormat.TraditionalOpenSSL],
        Encoding.OpenSSH: [],  # export to openssh format is not supported
        Encoding.DER: [PrivateFormat.PKCS8,
                       PrivateFormat.TraditionalOpenSSL]
    }

    # No exception should get thrown
    validate_output_encoding_format(
        PERMITTED_OUTPUT_ENCODING_FORMATS, Encoding.PEM, PrivateFormat.OpenSSH)

    # Exception should get thrown
    try:
        validate_output_encoding_format(
            PERMITTED_OUTPUT_ENCODING_FORMATS, Encoding.PEM, PrivateFormat.OpenSSH)
    except InvalidEncodingFormatError:
        pass


def test_main_rsa():
    '''Just test to make sure we don't throw any exceptions'''
    # PEM/PKCS8
    key = load_key("tests/_data/test_rsa", "openssh", "openssh")
    converted = convert_key(key, 'pem', 'pkcs8')

    # PEM/OpenSSH
    key2 = convert_key(key, 'openssh', 'openssh')
    key3 = convert_key(key, 'pem', 'openssh')

    # PEM/OpenSSL
    key4 = convert_key(key, 'pem', 'trad-openssl')

    # DER/PKCS8}
    key4 = convert_key(key, 'der', 'trad-openssl')

    # DER/OpenSSL
    key4 = convert_key(key, 'der', 'trad-openssl')
