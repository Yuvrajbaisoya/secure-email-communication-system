#!/usr/bin/env bash
set -euo pipefail
# Isolated synthetic OpenPGP lab. Never commit generated private keys.
command -v gpg >/dev/null || { echo "Install GnuPG first"; exit 1; }
LAB="$(mktemp -d "${TMPDIR:-/tmp}/secure-email-openpgp.XXXXXX")"
trap 'rm -rf "$LAB"' EXIT
export GNUPGHOME="$LAB/gnupg"
mkdir -m 700 "$GNUPGHOME"
printf '%s\n' 'Generating disposable test keys...'
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key "Alice Lab <alice@example.test>" ed25519 sign 1d >/dev/null 2>&1
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key "Bob Lab <bob@example.test>" default default 1d >/dev/null 2>&1
printf 'Synthetic confidential test message\n' > "$LAB/message.txt"
gpg --batch --yes --trust-model always --armor --recipient bob@example.test --local-user alice@example.test --sign --encrypt --output "$LAB/message.asc" "$LAB/message.txt"
gpg --batch --yes --status-fd 2 --output "$LAB/decrypted.txt" --decrypt "$LAB/message.asc" >"$LAB/decrypt.log" 2>&1
cmp "$LAB/message.txt" "$LAB/decrypted.txt"
grep -q '\[GNUPG:\] GOODSIG ' "$LAB/decrypt.log"
grep -q '\[GNUPG:\] VALIDSIG ' "$LAB/decrypt.log"
echo "PASS: Bob decrypted the encrypted message; plaintext matched."
echo "PASS: Alice's OpenPGP signature verified."
echo "NOTE: Disposable test keys and ciphertext were deleted on exit."
