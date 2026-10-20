# T-PGP-01 — OpenPGP Encryption and Signature Verification

**Status:** PASS — user-executed local lab (reported terminal output)  
**Environment:** Apple Silicon macOS, GnuPG 2.5.24  
**Script:** [practical/openpgp_lab.sh](../../openpgp_lab.sh)  
**Code revision tested:** `8251477`  
**Test identities:** Alice Lab <alice@example.test> (sender/signing); Bob Lab <bob@example.test> (receiver/encryption)

## Procedure

The user ran `git pull origin main`, `bash practical/openpgp_lab.sh`, and `echo "Exit code: $?"` in their locally cloned repository. The test used a fresh isolated GnuPG home under `/tmp/pgplab.XXXXXX/g`, created disposable keys, signed and encrypted a synthetic message for Bob, decrypted it, compared the decrypted plaintext with the original, and inspected GnuPG `GOODSIG` and `VALIDSIG` machine-readable status records.

## Observed terminal transcript (provided by user)

```text
==> Generating Alice's disposable signing key
gpg: keybox '/tmp/pgplab.5HrVpc/g/pubring.kbx' created
gpg: /tmp/pgplab.5HrVpc/g/trustdb.gpg: trustdb created
gpg: directory '/tmp/pgplab.5HrVpc/g/openpgp-revocs.d' created
gpg: revocation certificate stored as '/tmp/pgplab.5HrVpc/g/openpgp-revocs.d/342CF200F552A208189C811E6D602D2590BAE506.rev'

==> Generating Bob's disposable encryption key
gpg: revocation certificate stored as '/tmp/pgplab.5HrVpc/g/openpgp-revocs.d/27909C780B7817628DDC36584EFECEC59DA83F47.rev'

==> Encrypting for Bob and signing as Alice

==> Decrypting and verifying
PASS: Bob decrypted the encrypted message; plaintext matched.
PASS: Alice's OpenPGP signature verified.
NOTE: Disposable test keys and ciphertext were deleted on exit.
Exit code: 0
```

## Interpretation

- **PASS:** The script finished with exit status 0.
- **PASS:** Decrypted plaintext matched the synthetic source message, per `cmp`.
- **PASS:** GnuPG reported valid Alice signing status, per `GOODSIG` and `VALIDSIG` checks in the script.
- **Privacy:** Script removed the temporary lab directory on exit. No secret keys, private credentials, or plaintext from a real account were added to the repository.

## Scope and limitations

This evidence is based on **terminal output shared by the user**, not an independently witnessed remote execution or a production email exchange. Both disposable lab secret keys were available inside the **same isolated GnuPG home** during the demonstration; this proves functional OpenPGP operations but **does not establish sender/receiver key isolation or prove that only Bob could decrypt in a separate-host scenario**. It does not verify actual email delivery, S/MIME, key revocation enforcement, SPF/DKIM/DMARC, MFA, gateway or DLP controls.

**Historical debugging:** The earlier test failed with `gpg-agent: IPC connect call failed` and exit code 1. Commit `8251477` shortened the temporary socket path and explicitly launched `gpg-agent`; the next user-reported execution passed.

## Reproduce

```bash
bash practical/openpgp_lab.sh
echo "Exit code: $?"
```
