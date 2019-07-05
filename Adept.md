# ADEPT Information

## Books

Books "protected" by ADEPT DRM contain a few extra things from a regular EPUB
file; two files;

 - **META-INF/encryption.xml** This file contains an index of encrypted files
   in the EPUB and what cipher is used for each file (as far as I know, there
   can only be one cipher, given that there is only one key for it)

 - **META-INF/rights.xml** Contains a bunch of information, but the important
   tag is encryptedKey. The text of this tag contains the encryption key for
   the book. It is first encrypted with the user's public RSA key (usually
   something they don't give you) and then BASE64-encoded.

For the book, this is it. Decode the key and decrypt everything, remove the
encryption.xml and rights.xml files and it's no longer "protected".

## User key

The user key mentioned above is one key of an RSA key pair, and to decrypt the
actual key for the book, you first must find the private key.

### ACSM

When ADEPT books are "downloaded" what you actually get is an ACSM file which
is a small xml document that contains some information that software like
_Adobe Digital Editions_ can use to download the actual book, encrypted with
the key it then makes for you. This is what enables the device locking, since
the EPUB you get has its actual encryption key encrypted using the RSA public
key that the software generates. Only the holder of the private key can unlock
the book for reading.

The software here could also be an e-reader device, and then the EPUB files on
that device can be locked to it since only it knows the RSA private key. 

## Adobe Digital Editions

_Adobe Digital Editions_ is a piece of software for Windows and Mac that can 
act as a device for ADEPT locked EPUB files. It knows how to use ACSM to
download books and and decode the DRM and display them.

I learned about how to do this from [I &#x2665; cabbage's blog][iheartcabbages]
entry on it and the [quite frankly disgustingly ugly ineptkey script][ineptkey]
he'd written, but it does show how ADE encodes the private RSA key on windows
and how to retrieve it from the windows registry.

### "activation" key

ADE on windows calls the RSA key that can reveal the book-encrypting key an
"activation" key, and it is stored in the registry under
HEKY\_CURRENT\_USER\\Software\\Adobe\\Adept\\Activation. There are lots of
registry keys here, but the one that holds the "activation" key is called
*privateLicenseKey*, look for it and you'll find a BASE64 encoded string
that is encrypted with AES.

### "device" key

So the activation key is also encrypted, but fortunately the key to this
encryption&mdash;called the "device" key&mdash;is also stored in the registry
under HKEY\_CURRENT\_USER\\Software\\Adobe\\Adept\\Device with the imaginative
name "key".

### key key key... key...

Unfortunately the "device" key is also encrypted, using the windows native
"CryptProtectData" function, and the key to THIS key is gathered from the
running system.

There are four components to this key:

 - the boot volume serial number
 - the processor manufacturer
 - the processor signature
 - the name of the current user

These are then combined (in that order) as:

 - a bigendian unsigned integer
 - a 12 byte string
 - a 3 byte string
 - a 13 byte string

There, that wasn't unnecessarily complicated, was it?

[ineptkey]: https://pastebin.com/fpwuPLCC
[iheartcabbages]: http://i-u2665-cabbages.blogspot.com/2009/02/circumventing-adobe-adept-drm-for-epub.html
