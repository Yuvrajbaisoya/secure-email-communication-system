# Contributing and Reproducing Results

Contributions must be scoped to **synthetic offline fixtures**. Do not submit live customer messages, malware samples, real passwords, MFA seeds, DKIM private keys, S/MIME private keys or confidential logs.

## Before a change

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m practical.run_labs
```

If `gpg` and OpenSSL 3 are installed, additionally run `bash practical/openpgp_lab.sh` and `bash practical/smime_lab.sh`.

## Security-focused review checklist

- Include both positive and negative tests: tampering, replay, wrong domain, wrong recipient, rejected markers and malformed data.
- Explicitly identify synthetic policy emulation versus actual cryptographic verification.
- Fail safely for inputs outside a deliberately bounded demonstration.
- Store no generated private material in the repository.
- Update evidence register only after a test run has actually passed; include execution source and limitations.
- Treat external domain tests and account access as out of scope without express authorization.

For rollout advice, see [deployment checklist](docs/deployment-checklist.md).
