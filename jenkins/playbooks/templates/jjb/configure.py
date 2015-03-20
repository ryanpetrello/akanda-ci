#!/usr/bin/env python

import os
import base64
import hashlib
from M2Crypto.EVP import Cipher

MAGIC = "::::MAGIC::::"


def main():
    master_key = open('{{jenkins_home}}/secrets/master.key').read()
    hudson_secret_key = open(
        '{{jenkins_home}}/secrets/hudson.util.Secret'
    ).read()

    hashed_master_key = hashlib.sha256(master_key).digest()[:16]
    cipher = Cipher('aes_128_ecb', hashed_master_key, '', 0)
    v = cipher.update(hudson_secret_key)
    x = v + cipher.final()
    assert MAGIC in x

    k = x[:-16]
    k = k[:16]

    token = os.urandom(16).encode('hex')

    plaintext = token + MAGIC
    cipher = Cipher('aes_128_ecb', k, '', 1)
    v = cipher.update(plaintext)
    password = base64.b64encode(v + cipher.final())
    print password

    with open('/etc/jenkins_jobs/jenkins_jobs.ini', 'wb+') as f:
        f.write('\n'.join([
            '[jenkins]',
            'user=jenkins',
            'password=%s' % hashlib.md5(token).hexdigest(),
            'url=http://localhost:8080'
        ]))

if __name__ == '__main__':
    main()
