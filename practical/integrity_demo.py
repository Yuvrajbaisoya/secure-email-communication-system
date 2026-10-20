#!/usr/bin/env python3
"""Offline email-integrity demonstration using only Python's standard library.

Usage: python3 practical/integrity_demo.py
Uses synthetic content; creates no files or network connections.
"""
import hashlib
import hmac
from email.message import EmailMessage

def digest(message: bytes) -> str:
    return hashlib.sha256(message).hexdigest()

def run_demo() -> None:
    msg = EmailMessage()
    msg["From"] = "alice@example.test"
    msg["To"] = "bob@example.test"
    msg["Subject"] = "Synthetic security test"
    msg.set_content("CONFIDENTIAL-DEMO-12345: approved dummy message")
    original = msg.as_bytes()
    modified = original.replace(b"approved dummy message", b"altered dummy message")
    assert original != modified, "Tamper fixture was not modified"
    assert digest(original) != digest(modified), "Tampering not detected"
    print("SHA-256 original:", digest(original))
    print("SHA-256 modified:", digest(modified))
    print("PASS: modification changes the SHA-256 digest")
    print("NOTE: hashing alone does not authenticate a sender or replace OpenPGP/S/MIME signatures.")

if __name__ == "__main__":
    run_demo()
