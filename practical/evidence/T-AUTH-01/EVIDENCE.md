# T-AUTH-01 — SPF, DKIM and DMARC Offline Authentication

**Result:** PASS — automated synthetic lab, 20 October 2026  
**Execution:** [GitHub Actions job, run 39389041933](https://github.com/Yuvrajbaisoya/secure-email-communication-system/actions/runs/39389041933)  
**Code revision:** `c641f4489b4b0f502304c8d5cf31cb6daed257eb`  
**Operating system:** GitHub-hosted Ubuntu, Python 3.12; cryptography dependency installed from requirements.txt.

## Observed tests

- **SPF — 6 positive/negative assertions PASS:** authorized IPv4, unauthorized IPv4, IPv6, softfail, invalid SPF syntax, unsupported mechanism rejected.
- **DKIM — 6 assertions PASS:** actual RSA-SHA256 signing/verification, body tampering failure, subject tampering failure, wrong key failure, wrong selector failure, and DNS TXT public-key formatting.
- **DMARC — 7 assertions PASS:** SPF or DKIM aligned pass, unaligned reject, strict vs relaxed alignment, suffix spoof rejection, `p=none` monitoring outcome and invalid policy rejection.
- **Integrated runner — PASS:** `spf_authorized_ip`, `spf_unauthorized_ip`, `dkim_rsa_signature`, `dkim_tampering_rejected` and `dmarc_alignment` were all `true` in the CI job.

## Genuine CI output excerpt

```text
test_real_rsa_dkim_signature ... ok
test_body_tampering_rejected ... ok
test_subject_tampering_rejected ... ok
test_unaligned_both_rejected ... ok
test_relaxed_is_not_suffix_confusion ... ok
test_unsupported_mechanism_fails_closed ... ok
Ran 37 tests in 1.275s
OK
"dkim_rsa_signature": true
"dkim_tampering_rejected": true
"dmarc_alignment": true
"spf_authorized_ip": true
"spf_unauthorized_ip": true
```

The 37-test count is **for the complete repository suite**; this authentication group contributes 19 tests. The whole job succeeded.

## Scope and limitations

This does **not** prove any domain published valid SPF, DKIM or DMARC records. SPF is a **subset simulator** with no real DNS resolution, lookup-limit handling or `include` support. DKIM uses actual RSA cryptography but supports only its fixed-format synthetic headers and explicit trusted public key, without full RFC parsing or DNS lookup. DMARC alignment uses an explicitly known organizational domain and does not parse aggregate reports. Production tests require an authorized real domain and mail provider.

**Reproduce:** `python -m unittest tests.test_authentication -v` and `python -m practical.run_labs`.
