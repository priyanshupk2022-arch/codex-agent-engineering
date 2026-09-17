# Skill: security-review

## Overview
Threat modeling and vulnerability audit focusing on OWASP Top 10 and Agent-specific threats.

## When to Use
When handling user input, authentication/authorization logic, external API integrations, or sandbox configurations.

## Inputs
Target source files, infrastructure configs, data flow diagrams.

## Workflow
1. Attack Surface Mapping: Identify all entry points for untrusted external data (APIs, files, environment variables).
2. Vulnerability Scanning: Audit code for injection (SQLi, Command Injection, XSS), auth bypass, insecure deserialization, and SSRF.
3. Agent Threat Audit: Check for prompt injection surfaces, unauthorized tool execution paths, and secret leakage.
4. Exploit PoC Authoring: Draft safe, local Proof-of-Concept demonstrations for confirmed vulnerabilities.
5. Remediation & Hardening: Propose cryptographically sound, parameterized, and sandboxed remediations.

## Outputs & Deliverables
SECURITY_AUDIT.md detailing vulnerabilities, CVSS scores, remediation patches, and regression tests.

## Constraints & Guardrails
Do not execute live exploits against external systems. All PoCs must be contained within local mocks.

## Verification Protocol
Remediation verified by re-running exploit test to confirm vulnerability is completely closed.

## Common Failure Modes & Recovery
False sense of security from automated scanners -> combine automated SAST with manual control-flow analysis.
