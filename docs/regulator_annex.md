# Regulator Annex: DBC × SUITCASE
## A Plain-Language Summary for Auditors

**To:** Regulatory Bodies (ICO, PIPEDA, FTC)
**From:** Helix AI Innovations Inc.
**Subject:** Liability Tracing & Custody Architecture

### 1. What problem does this solve?
Current AI systems often operate as "Orphaned Agents"—software acting without a clear chain of human liability. When an AI causes harm, the developer, the user, and the platform blame each other. **DBC × SUITCASE** eliminates this ambiguity.

### 2. The Mental Model
*   **The DBC (Digital Birth Certificate):** Think of this as the **VIN (Vehicle Identification Number)** on a car chassis. It is stamped at the factory (Genesis) and cannot be changed. It proves the agent exists and who owns the keys.
*   **The SUITCASE:** Think of this as the **Service Log & Glovebox**. It travels with the car. It contains the registration, insurance (attestations), and maintenance history (telemetry). It is append-only; you cannot tear pages out, only add new ones.

### 3. What can Regulators Verify?
By demanding the SUITCASE file, a regulator can mathematically verify:
1.  **Identity:** Is this the original agent, or a clone? (Merkle Root check).
2.  **Custody:** Which human held the signing key at the exact moment of an action?
3.  **Integrity:** Has the history been tampered with? (Hash chain check).

### 4. Conclusion
This architecture ensures there is **No Action Without Validation** and **No Agent Without a Human**. It turns AI governance from a philosophical debate into a forensic science.
