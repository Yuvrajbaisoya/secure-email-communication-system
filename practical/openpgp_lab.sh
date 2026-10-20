#!/usr/bin/env bash
set -euo pipefail
# Disposable synthetic OpenPGP lab. No private key material should be committed.
command -v gpg >/dev/null || { echo "ERROR: GnuPG is not installed"; exit 1; }
LAB="$(mktemp -d /tmp/pgplab.XXXXXX)"
trap 'rm -rf "$LAB"' EXIT
export GNUPGHOME="$LAB/g"
mkdir -m 700 "$GNUPGHOME"
# Keep socket paths short on macOS, then launch the agent explicitly.
gpgconf --launch gpg-agent || fail "Could not start gpg-agent; check macOS permissions and socket path"
step() { printf '\n==> %s\n' "$1"; }
fail() { echo "ERROR: $1" >&2; exit 1; }
step "Generating Alice's disposable signing key"
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key "Alice Lab <alice@example.test>" ed25519 sign 1d || fail "Alice key generation failed"
step "Generating Bob's disposable encryption key"
gpg --batch --pinentry-mode loopback --passphrase '' --quick-generate-key "Bob Lab <bob@example.test>" rsa3072 encr 1d || fail "Bob key generation failed"
printf 'Synthetic confidential test message\n' > "$LAB/message.txt"
step "Encrypting for Bob and signing as Alice"
gpg --batch --yes --trust-model always --armor --recipient bob@example.test --local-user alice@example.test --sign --encrypt --output "$LAB/message.asc" "$LAB/message.txt" || fail "Encryption/signing failed"
step "Decrypting and verifying"
gpg --batch --yes --status-fd 2 --output "$LAB/decrypted.txt" --decrypt "$LAB/message.asc" >"$LAB/decrypt.log" 2>&1 || { cat "$LAB/decrypt.log" >&2; fail "Decryption/verification failed"; }
cmp "$LAB/message.txt" "$LAB/decrypted.txt" || fail "Plaintext mismatch"
grep -q '\[GNUPG:\] GOODSIG ' "$LAB/decrypt.log" || fail "GOODSIG missing"
grep -q '\[GNUPG:\] VALIDSIG ' "$LAB/decrypt.log" || fail "VALIDSIG missing"
echo "PASS: Bob decrypted the encrypted message; plaintext matched."
echo "PASS: Alice's OpenPGP signature verified."
echo "NOTE: Disposable test keys and ciphertext were deleted on exit."
