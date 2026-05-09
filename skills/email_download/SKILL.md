---
name: email-download
description: Detect new POF journal submission emails and download PDF attachments automatically.
license: Complete terms in LICENSE.txt
---

This skill automatically connects to a user's email, detects new POF submission emails, and downloads the attached PDFs to a local folder.

## Design Thinking
- **Purpose**: Automate manuscript PDF retrieval without user intervention.
- **Tone**: Professional, robust, and reliable.
- **Constraints**: IMAP email access, PDF attachments, automated execution.
- **Differentiation**: Minimizes time spent manually checking emails and downloading files.

## Input / Output
- Input: Email credentials, IMAP server address, download folder.
- Output: List of downloaded PDF file paths.