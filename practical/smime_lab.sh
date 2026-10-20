#!/usr/bin/env bash
set -euo pipefail
# Offline S/MIME lab using disposable self-signed test certificates.
if command -v brew >/dev/null 2>&1 && brew --prefix openssl@3 >/dev/null 2>&1; then
  OPENSSL="$(brew --prefix openssl@3)/bin/openssl"
else
  OPENSSL="${OPENSSL:-openssl}"
fi
"$OPENSSL" version
LAB="$(mktemp -d /tmp/smimelab.XXXXXX)"
trap 'rm -rf "$LAB"' EXIT
cd "$LAB"
printf 'From: alice@example.test\nTo: bob@example.test\nSubject: Synthetic S/MIME test\n\nThis is a disposable test message.\n' > message.eml
echo "==> Creating disposable Alice and Bob certificates"
"$OPENSSL" req -x509 -newkey rsa:3072 -sha256 -nodes -days 1 -keyout alice.key -out alice.crt -subj "/CN=Alice Lab/emailAddress=alice@example.test" -addext "extendedKeyUsage=emailProtection" >/dev/null 2>&1
"$OPENSSL" req -x509 -newkey rsa:3072 -sha256 -nodes -days 1 -keyout bob.key -out bob.crt -subj "/CN=Bob Lab/emailAddress=bob@example.test" -addext "extendedKeyUsage=emailProtection" >/dev/null 2>&1
echo "==> Signing message with Alice's private key"
"$OPENSSL" smime -sign -in message.eml -signer alice.crt -inkey alice.key -out signed.pem -outform SMIME -nodetach
echo "==> Verifying Alice's signature with explicit lab trust anchor"
"$OPENSSL" smime -verify -in signed.pem -CAfile alice.crt -out verified.eml >/dev/null
cmp message.eml verified.eml || { echo "ERROR: Signed content mismatch"; exit 1; }
echo "==> Encrypting signed S/MIME for Bob"
"$OPENSSL" smime -encrypt -aes256 -in signed.pem -out encrypted.pem bob.crt
echo "==> Decrypting with Bob's private key"
"$OPENSSL" smime -decrypt -in encrypted.pem -recip bob.crt -inkey bob.key -out decrypted-signed.pem
cmp signed.pem decrypted-signed.pem || { echo "ERROR: Decrypted signed message mismatch"; exit 1; }
"$OPENSSL" smime -verify -in decrypted-signed.pem -CAfile alice.crt -out final-verified.eml >/dev/null
cmp message.eml final-verified.eml || { echo "ERROR: Final content mismatch"; exit 1; }
echo "PASS: Alice's S/MIME signature verified against the lab certificate."
echo "PASS: Bob decrypted the AES-256 S/MIME message; content matched."
echo "NOTE: Certificates are self-signed lab fixtures; no public CA or real email transport tested."
echo "NOTE: Disposable private keys were deleted on exit."
