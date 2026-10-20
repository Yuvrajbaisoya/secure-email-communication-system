"""Deliberately bounded offline SPF and DMARC policy evaluation.

This is NOT a complete SPF DNS resolver or a production DMARC implementation.
Only v=spf1 ip4/ip6/all mechanisms and explicit mock domains are supported.
"""
from dataclasses import dataclass
import ipaddress


@dataclass(frozen=True)
class DMARCDecision:
    result: str
    action: str
    aligned_spf: bool
    aligned_dkim: bool


def evaluate_spf(ip_address: str, txt_record: str) -> str:
    """Evaluate SPF ip4, ip6 and all in order against a synthetic IP.

    Unsupported mechanisms raise ValueError rather than silently allowing mail.
    A production SPF evaluator also needs DNS lookup limits, includes, redirects,
    MX/A resolution, error handling, and envelope HELO/mail-from logic.
    """
    address = ipaddress.ip_address(ip_address)
    tokens = txt_record.split()
    if not tokens or tokens[0].lower() != "v=spf1":
        raise ValueError("Invalid SPF record")
    for token in tokens[1:]:
        qualifier = token[0] if token[:1] in "+-~?" else "+"
        mechanism = token[1:] if token[:1] in "+-~?" else token
        match = False
        if mechanism == "all":
            match = True
        elif mechanism.startswith("ip4:") or mechanism.startswith("ip6:"):
            family, network = mechanism.split(":", 1)
            parsed = ipaddress.ip_network(network, strict=False)
            if (family == "ip4") != (parsed.version == 4):
                raise ValueError("SPF mechanism/address-family mismatch")
            match = address in parsed
        else:
            raise ValueError("Unsupported SPF mechanism in bounded offline lab: " + mechanism)
        if match:
            return {"+": "pass", "-": "fail", "~": "softfail", "?": "neutral"}[qualifier]
    return "neutral"


def _domain(value: str) -> str:
    cleaned = value.strip().lower().rstrip(".")
    if not cleaned or ".." in cleaned or any(
        not (part.replace("-", "").isalnum() and not part.startswith("-") and not part.endswith("-"))
        for part in cleaned.split(".")
    ):
        raise ValueError("Invalid DNS domain")
    return cleaned


def _aligned(candidate: str, from_domain: str, mode: str, organizational_domain: str | None) -> bool:
    if not candidate:
        return False
    candidate = _domain(candidate)
    from_domain = _domain(from_domain)
    if candidate == from_domain:
        return True
    if mode == "s":
        return False
    # Do not guess public suffixes: require an explicitly known organizational
    # domain for relaxed-alignment comparisons in this offline model.
    if not organizational_domain:
        return False
    root = _domain(organizational_domain)
    return all(domain == root or domain.endswith("." + root)
               for domain in (candidate, from_domain))


def evaluate_dmarc(
    *, from_domain: str, envelope_domain: str, spf_result: str,
    dkim_domain: str | None, dkim_result: str, dmarc_record: str,
    organizational_domain: str | None = None
) -> DMARCDecision:
    """DMARC pass requires SPF *or* DKIM to pass with From-domain alignment.

    No DNS organizational-domain discovery, ARC, subdomain policy or pct
    semantics are implemented here; do not use as a mail receiver.
    """
    tags = {}
    for item in dmarc_record.split(";"):
        if not item.strip():
            continue
        if "=" not in item:
            raise ValueError("Malformed DMARC tag")
        k, v = (segment.strip().lower() for segment in item.split("=", 1))
        if k in tags:
            raise ValueError("Duplicate DMARC tag")
        tags[k] = v
    if tags.get("v") != "dmarc1" or tags.get("p") not in {"none", "quarantine", "reject"}:
        raise ValueError("Invalid DMARC version or policy")
    if tags.get("aspf", "r") not in {"s", "r"} or tags.get("adkim", "r") not in {"s", "r"}:
        raise ValueError("Invalid alignment mode")
    spf_aligned = spf_result == "pass" and _aligned(
        envelope_domain, from_domain, tags.get("aspf", "r"), organizational_domain
    )
    dkim_aligned = dkim_result == "pass" and _aligned(
        dkim_domain or "", from_domain, tags.get("adkim", "r"), organizational_domain
    )
    passed = spf_aligned or dkim_aligned
    policy = tags["p"]
    return DMARCDecision(
        result="pass" if passed else "fail",
        action="accept" if passed or policy == "none" else policy,
        aligned_spf=spf_aligned,
        aligned_dkim=dkim_aligned,
    )
