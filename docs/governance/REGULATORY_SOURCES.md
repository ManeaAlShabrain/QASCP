# QASCP regulatory and engineering source register

[English handbook](ENGINEERING_GOVERNANCE.md) · [الدليل العربي](ENGINEERING_GOVERNANCE.ar.md)

External references supply criteria and evidence terminology for independent design. This register records official discovery links. It does not designate QASCP as certified, approve applicability, or establish that the linked edition is current for every client.

| ID | Issuer and official source | Use and current applicability |
|---|---|---|
| REF-NIST-CSF | NIST, [Cybersecurity Framework 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) | Cyber risk and governance design guidance. |
| REF-NIST-AI | NIST, [AI RMF 1.0](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10) | Model risk and evaluation design guidance. Track further published revisions during review. |
| REF-NIST-SSDF | NIST, [SP 800-218 v1.1](https://csrc.nist.gov/pubs/sp/800/218/final) | Secure software lifecycle and supplier review guidance. |
| REF-MITRE-ATTACK | MITRE, [ATT&CK](https://attack.mitre.org/) | Defensive detection coverage and threat language. Record version when mapping. |
| REF-MITRE-ATLAS | MITRE, [ATLAS](https://atlas.mitre.org/) | AI threat modeling and defensive control coverage. Record version when mapping. |
| REF-OWASP-ASVS | OWASP, [ASVS](https://asvs.owasp.org/) | Application and API verification. Pin edition and control IDs when adopting. |
| REF-OWASP-AI | OWASP, [GenAI Security Project](https://genai.owasp.org/) | AI security design and defensive verification. Pin applicable publication and version when adopting. |
| QA-QCB-AI | QCB, [Artificial Intelligence Guideline 2024](https://www.qcb.gov.qa/Services/Financial%20Technology/QCB_Artificial_Intelligence_Guideline.pdf) | Candidate for QCB-regulated entities using relevant AI systems. Entity and deployment scope pending. |
| QA-QCB-DHP | QCB, [Data Handling and Protection Regulation](https://www.qcb.gov.qa/Documents/InformationSecurity/Data%20Handling%20and%20Protection%20Regulation.pdf) | Candidate for data classification, processing, and third-party controls. Entity scope and effective edition pending. |
| QA-QCB-CLOUD | QCB, [Cloud Computing Regulation](https://www.qcb.gov.qa/Documents/InformationSecurity/Cloud%20Computing%20Regulation.pdf) | Candidate when a relevant cloud or outsourcing arrangement is in scope. Review arrangement, access and location. |
| QA-QCB-BANK | QCB, [Instructions to Banks index](https://www.qcb.gov.qa/ar/Pages/InstructionsToBanks2024.aspx) | Discovery source. Confirm latest applicable instruction, amendments, and circulars for the bank's license. |
| QA-NCSA-PDP | NCSA, [PDPPL and regulated-entity guidance](https://ncsa.gov.qa/en/pages/guidance-hub-for-regulated-entities) | Separately identify the law, official provisions, and explanatory guidance. Confirm relevant roles and jurisdiction. |
| QA-NCSA-NIA | NCSA, [National Information Assurance Standard v2.1](https://assurance.ncsa.gov.qa/sites/default/files/publications/policy/2023/NCSA_CSGA_%20National_Information_Assurance_Standard_En_V2.1_1.pdf) | Candidate assurance controls. Confirm applicable edition, scope and any contractual basis. |
| QA-QFMA-RULES | QFMA, [Legislation and decisions](https://www.qfma.org.qa/English/Legislation/Legal_decisions) | Discovery source for an institution whose regulated activities fall under QFMA. Confirm exact rules and amendments per license. |
| QA-QFC-DP | QFC, [Data Protection Regulations and Rules index](https://www.qfc.qa/en/resource-centre/) | Candidate for processing in scope of the QFC data-protection regime. Confirm jurisdiction, roles and current texts. |

## Applicability decision procedure

1. Identify entity, licensing authority, regulated activity, data classes, model use, deployment, storage and processing locations, vendors, and access paths. Select the relevant set from activation conditions such as QCB supervision, tenant license, use of personal data, and cloud or outsourcing materiality.
2. Obtain authoritative documents and track amendments and effective dates. Record publisher, title, edition, clause, link, retrieval date, and hash if an authorized snapshot is retained. Preserve rights metadata and use permitted quotes only.
3. Record the exact clause, deployment scope, interpretation, mandatory or advisory basis, mapped QASCP control, evidence owner, reviewer, and expiry or next review date.
4. Track applicability as pending, applicable, or inapplicable with reason. Assess evidence separately as unassessed, insufficient, failed, or verified for scope. Keep gaps open for review. Record any authorization or certification against its exact scope and date.
