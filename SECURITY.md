# Security Policy

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| < 0.3   | :x:                |

## Reporting a Vulnerability
This repository defines **Cryptographic Custody Infrastructure**. 

If you discover a vulnerability that allows for:
1.  **DBC Forgery** (Minting without a key)
2.  **Suitcase Tampering** (Breaking the hash chain)
3.  **Identity Spoofing** (HGL collision)

Please do **NOT** open a public issue. 
Email the Custodian directly at: **helix.project.ai@helixprojectai.com** (or via LinkedIn DM).

## Custody Model
Helix-TTD operates on a **Custody-Before-Trust** model.
*   We do not hold your keys.
*   We do not store your logs.
*   Security is structural, not managed.
