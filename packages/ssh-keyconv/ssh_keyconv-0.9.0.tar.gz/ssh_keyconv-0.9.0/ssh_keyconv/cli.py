import argparse
import logging
import enum
import sys

from . import __version__

from cryptography.hazmat.primitives.serialization import Encoding, \
    PrivateFormat, NoEncryption, load_pem_private_key, \
    load_ssh_private_key, load_der_private_key
from cryptography.hazmat.backends import default_backend

logging.basicConfig()
logger = logging.getLogger(__name__)

ENCODINGMAP = {
    'pem': Encoding.PEM,
    'openssh': Encoding.OpenSSH,
    'der': Encoding.DER
}

# I am excluding pkcs12 for now since I don't need to support that format.
FORMATMAP = {
    'openssh': PrivateFormat.OpenSSH,
    'pkcs8': PrivateFormat.PKCS8,
    'trad-openssl': PrivateFormat.TraditionalOpenSSL
}

LOADERS = {
    Encoding.PEM: load_pem_private_key,
    Encoding.OpenSSH: load_ssh_private_key,
    Encoding.DER: load_der_private_key
}

INPUT_ENCODING_CORRECTIONS = {
    (Encoding.PEM, PrivateFormat.OpenSSH):
        (Encoding.OpenSSH, PrivateFormat.OpenSSH)
}

OUTPUT_ENCODING_CORRECTIONS = {
    (Encoding.OpenSSH, PrivateFormat.OpenSSH):
        (Encoding.PEM, PrivateFormat.OpenSSH)
}

# encoding: [list of formats]
PERMITTED_OUTPUT_ENCODING_FORMATS = {
    Encoding.PEM: [PrivateFormat.OpenSSH,
                   PrivateFormat.PKCS8,
                   PrivateFormat.TraditionalOpenSSL],
    Encoding.OpenSSH: [],  # export to openssh format is not supported
    Encoding.DER: [PrivateFormat.PKCS8,
                   PrivateFormat.TraditionalOpenSSL]
}


class RetCode(enum.IntEnum):
    """Return codes"""
    OK = 0
    INFILE_NOT_LOADED = 1
    KEY_CANNOT_BE_CONVERTED = 2
    OUTPUT_FILE_NOT_WRITTEN = 3
    INVALID_OUTPUT_ENCODING_FORMAT = -1


class InvalidEncodingFormatError(Exception):
    """Exception raised when a format is not supported for an encoding"""
    def __init__(self, *args, encoding: Encoding, format: PrivateFormat,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self._encoding = encoding
        self._format = format

    def __str__(self):
        return f"Format {self._format} is unsupported for encoding " \
            "{self._encoding}"


def parse_args(argv: list):
    parser = argparse.ArgumentParser(
        description="Converts SSH private keys between formats")
    parser.add_argument("-i", "--infile", type=str, required=True,
                        help="Input file path")
    parser.add_argument("-f", "--informat", choices=FORMATMAP.keys(),
                        default="openssh", help="Input format")
    parser.add_argument("-e", "--inencoding", choices=ENCODINGMAP.keys(),
                        default="openssh",
                        help="Input encoding. Default: %(default)s")
    parser.add_argument("-o", "--outfile", type=str, required=True,
                        help="Output file path")
    parser.add_argument("-F", "--outformat", choices=FORMATMAP.keys(),
                        required=True, help="Output format")
    parser.add_argument("-E", "--outencoding", choices=ENCODINGMAP.keys(),
                        default="pem",
                        help="Output encoding. Default: %(default)s")
    parser.add_argument("-v", action="count", default=0,
                        help="Increase verbosity")
    parser.add_argument("--version", action="version",
                        version="%(prog)s "+__version__)
    return parser.parse_args(args=argv[1:])


def set_log_level(v: int):
    LOG_LEVELS = [logging.ERROR,
                  logging.WARNING,
                  logging.INFO,
                  logging.DEBUG]
    logging_level = LOG_LEVELS[min(v, 3)]
    logging.getLogger().setLevel(logging_level)  # Set level on global logger


def load_key(filepath: str, encoding: str, format: str,
             password: bytes = None):
    # Input configuration
    e = ENCODINGMAP[encoding]
    f = FORMATMAP[format]
    (e, f) = apply_encoding_format_corrections(
        INPUT_ENCODING_CORRECTIONS, e, f)
    loader = LOADERS[e]

    # Read input file
    with open(filepath, "rb") as infh:
        inkey = loader(data=infh.read(),
                       password=password,
                       backend=default_backend())

    logger.info(f"{filepath} loaded")
    return inkey


def convert_key(key: bytes, encoding: str, format: str, password=None):
    # Output configuration
    e = ENCODINGMAP[encoding]
    f = FORMATMAP[format]
    (e, f) = apply_encoding_format_corrections(
        OUTPUT_ENCODING_CORRECTIONS, e, f)

    validate_output_encoding_format(
        PERMITTED_OUTPUT_ENCODING_FORMATS, e, f)

    encryption_algorithm = NoEncryption()
    if password is not None:
        raise NotImplementedError("Password support not yet implemented")

    return key.private_bytes(
        encoding=e,
        format=f,
        encryption_algorithm=encryption_algorithm)


def write_key(filepath: str, outkey: bytes):
    with open(filepath, "wb") as outfh:
        outfh.write(outkey)
    logger.info(f"{filepath} written")


def main():
    args = parse_args(sys.argv)
    set_log_level(args.v)
    logger.debug(args)

    try:
        inkey = load_key(args.infile, args.inencoding, args.informat)
    except Exception:
        logger.fatal(f"Input file {args.infile} could not be loaded.",
                     exc_info=True)
        return RetCode.INFILE_NOT_LOADED

    # Convert key to new format
    try:
        outkey = convert_key(inkey, args.outencoding, args.outformat)
    except InvalidEncodingFormatError:
        logger.fatal(f"The requested output encoding {args.outencoding} "
                     f"and format {args.outformat} pair is not valid.",
                     exc_info=True)
        return RetCode.INVALID_OUTPUT_ENCODING_FORMAT
    except Exception:
        logger.fatal(
            f"Private key contents could not be converted to "
            f"{args.outencoding} encoding and {args.outformat} format",
            exc_info=True)
        return RetCode.KEY_CANNOT_BE_CONVERTED

    # Write to output file
    try:
        write_key(args.outfile, outkey)
    except Exception:
        logger.fatal(f"Output file {args.outfile} cannot be written",
                     exc_info=True)
        return RetCode.OUTPUT_FILE_NOT_WRITTEN

    return RetCode.OK


def apply_encoding_format_corrections(
        corrections_map: dict, encoding: Encoding, format: PrivateFormat) \
        -> tuple[Encoding, PrivateFormat]:
    """Apply a correction from `corrections_map` if one exists.

    :param corrections_map: Map of (encoding, format) to replacement
                            (encoding, format)
    :type corrections_map: map((Encoding, PrivateFormat):
                           (Encoding, PrivateFormat))
    :returns: Corrected (encoding, format) tuple if one exists, otherwise the
              original (encoding, format) tuple.
    """
    logger.debug(f"Requested (encoding, format): ({encoding},{format})")
    result = corrections_map.get((encoding, format), (encoding, format))
    logger.debug(f"Corrected (encoding, format): {result}")
    return result


def validate_output_encoding_format(
        valid_encoding_formats: dict, outencoding: Encoding,
        outformat: PrivateFormat) -> None:
    if outformat not in \
            valid_encoding_formats.get(outencoding, []):
        raise InvalidEncodingFormatError(
            encoding=outencoding, format=outformat)
