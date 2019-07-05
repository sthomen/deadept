# DeAdept
Decrypt ADEPT DRM "protected" EPUB files

## Installation

To install, just run

```
python setup.py install
```

And it will take care of everything. As of this time of writing, the module is
not in pip.

## Usage

The module can be used directly by two automatically installed scripts; `deadept`
and `deadeptdump`.

The former performs the whole process, user key retrieval from the platform and
the second only does the key retrieval an dumps the user's private RSA key in
a DER-formatted file named `adept.der`.
