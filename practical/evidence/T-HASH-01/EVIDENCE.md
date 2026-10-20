# Synthetic Email Integrity Test Evidence

**Test ID:** T-HASH-01

**Method:** Compare SHA-256 digests of synthetic email messages before and after a body modification.

**Original SHA-256:** `94b0bb3d53e11890807b7868ebf4aa7acdd71eaabb91aae19fc30e2a1227c947`

**Tampered SHA-256:** `8a5cda69b04780aaee38ac42293a905d5df6533fb77d5a46723515ff25909d50`

**Result:** PASS — digests differ.

**Reproduce:** `shasum -a 256 original-email.eml tampered-email.eml`

**Scope:** Synthetic, local test. No real email transmission or cryptographic signing occurred. Hashes alone do not authenticate senders.
