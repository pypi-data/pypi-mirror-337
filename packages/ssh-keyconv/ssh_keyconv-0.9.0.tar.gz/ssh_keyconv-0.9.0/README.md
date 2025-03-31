# ssh-keyconv

ssh-keyconv is a SSH key conversion utility that can convert SSH private keys between OpenSSH, PEM and DER encoding, and OpenSSH, PKCS8 and Traditional OpenSSL format.

**Supported Formats:**

* OpenSSH
* PKCS8
* Traditional OpenSSL (trad-openssl)

**Supported Encodings:**

* PEM
* OpenSSH (PEM)
* DER

## Installation

```bash
pip install ssh_keyconv
```

This will install the ssh_keyconv module and the ssh-keyconv executable.

## Example usage

1. Generate a SSH keypair

```bash
ssh-keygen -t rsa -b 4096 -f newkey_rsa
```

2. Convert the private key to PKCS8 format

```bash
ssh-keyconv -i newkey_rsa -f openssh -e openssh -o newkey_rsa.pem -F pkcs8 -E pem
```

## Development

1. Clone the repo

```bash
git clone https://codeberg.org/lkm35t/ssh-keyconf
```

2. Set up a virtualenv

```bash
cd ssh-keyconv
make setup
```

3. Run tests

```bash
make test
```

4. Bump the version number in `ssh_keyconv/__init__.py:__version__`

5. Build a release

```bash
make clean build
```

6. Do a test publish

```bash
make publish-test
```

7. Verify the test publish

```bash
make verify-publish-test
```

8. Publish to PyPI

```bash
make publish
```

9. Verify the publish to PyPI

```bash
make test-publish
```
