---
name: prelaunch-legal
description: Pre-release legal and compliance checklist for an app or website built with Claude — privacy policy, terms, personal data, licenses, cookies, payments, app-store rules. Use when the user says "готуюсь до релізу", "що треба юридично перед запуском", "privacy policy", "terms of service", or before publishing an app.
---

# Pre-launch legal checklist (20 tasks)

Not legal advice — produce drafts and flags, and tell the user which items need a lawyer for their jurisdiction. First ask (once): target countries/regions, whether users pay, whether minors may use it, what data is collected.

Scan the codebase to answer each item from evidence (what data fields, which third-party SDKs, analytics, payment providers), then produce the deliverables.

1. **Data inventory** – list every personal data field collected, where stored, who it's shared with (from code + SDKs).
2. **Privacy policy** – draft matching the inventory (purposes, legal basis, retention, rights, contacts).
3. **Terms of service / user agreement** – acceptable use, account termination, liability limits, governing law.
4. **Cookie / tracking consent** – banner required? (EU/UK: yes for non-essential cookies). Block analytics until consent.
5. **GDPR / UK GDPR** – lawful basis, DPA with processors, data-subject request flow (export, delete).
6. **Other regimes** – CCPA/CPRA (US-CA), Ukraine's personal data law, LGPD, etc. per target regions.
7. **Account deletion** – in-app delete account + data (mandatory for App Store / Google Play).
8. **Children** – COPPA / age gate if under-13/16 users possible.
9. **Open-source licenses** – audit dependencies (GPL/AGPL obligations), produce THIRD_PARTY_NOTICES.
10. **Your own license** – choose license for your code/content.
11. **AI-generated content** – disclose AI use where required (EU AI Act transparency), check model provider ToS for your use case.
12. **User-generated content** – moderation, report/takedown flow, DMCA/notice-and-action contact.
13. **Assets** – fonts, images, icons, music are licensed for commercial use.
14. **Trademarks / name** – quick conflict check of app name and domain.
15. **Payments & refunds** – refund policy, subscription auto-renewal disclosures, VAT/sales tax, store billing rules.
16. **Consumer law** – withdrawal rights (EU 14 days), clear pricing.
17. **Accessibility** – WCAG basics (EU Accessibility Act for some services).
18. **Security & breach** – incident response plan, breach notification duty (72h GDPR).
19. **Marketing** – email opt-in, unsubscribe link (CAN-SPAM / GDPR), no fake reviews.
20. **Imprint / contacts** – legal entity, address, support email (Impressum in DE/AT).

## Extra items called out in the source video
Public offer / refund terms, cookie banner with consent in several formats, data minimisation (collect nothing extra), audit third-party SDKs, **remove dark patterns, hidden payments, fake reviews and empty promises**, image alt text, colour contrast, keyboard navigation, company details, parental consent for children's data, unsubscribe in mailings, font/image licences, data deletion on request.

## Output
A checklist table `# | item | status (ok / missing / risk) | evidence | action`, plus generated draft files (`PRIVACY.md`, `TERMS.md`, `THIRD_PARTY_NOTICES.md`) when the user agrees.
