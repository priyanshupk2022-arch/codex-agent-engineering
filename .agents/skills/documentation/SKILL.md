# Skill: documentation

## Overview
High-fidelity technical writing, API reference generation, and architecture documentation.

## When to Use
When shipping new features, writing architectural decision records (ADRs), or updating user guides.

## Inputs
Feature implementation, API contracts, target audience profile.

## Workflow
1. Audience & Scope Analysis: Determine user persona (Beginner, Intermediate, API Consumer, Maintainer).
2. Code & Interface Inspection: Read source code, docstrings, and type definitions to extract accurate schemas.
3. Structure & Drafting: Author documentation following Diablo/Divio principles (Tutorial, How-To, Reference, Explanation).
4. Code Sample Verification: Test all included code snippets and CLI commands in a real shell to guarantee accuracy.
5. Cross-Linking & Navigation: Update index files, table of contents, and internal navigation links.

## Outputs & Deliverables
Crisp, verified markdown documentation with executable code samples and architecture diagrams.

## Constraints & Guardrails
No untested code snippets. No placeholders ('TODO', 'exercise for reader'). Maintain uniform terminology.

## Verification Protocol
All markdown links verified via link checker; all code examples execute successfully without modification.

## Common Failure Modes & Recovery
Documentation drift after code changes -> link docs directly to test cases or generate from source docstrings.
