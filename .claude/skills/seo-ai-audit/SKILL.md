---
name: seo-ai-audit
description: Audit a website (codebase or URL) the way an SEO specialist would, and check whether search engines and AI assistants (ChatGPT, Claude, Perplexity, Google AI Overviews) can find, read and cite it. Use when the user says "SEO audit", "чи знайде мене google/chatgpt", "перевір сайт на SEO", or after building a site with AI.
---

# SEO + AI-visibility audit

Run the checks below as parallel lanes (one subagent per lane when the site is large; inline when small). Each lane returns findings as `severity | page/file | problem | fix`.

## Lanes
1. **Crawlability** – robots.txt (does it block Googlebot, GPTBot, ClaudeBot, PerplexityBot, Google-Extended?), sitemap.xml present and referenced, canonical tags, no accidental `noindex`, sane status codes / redirects.
2. **Rendering** – is the main content in the initial HTML or only after client-side JS? SPA-only content is invisible to most AI crawlers. Recommend SSR/SSG/prerender if so.
3. **On-page** – one `<title>` (50–60 chars) and meta description (140–160) per page, unique; single `<h1>`; logical heading order; descriptive URLs; alt text on images.
4. **Structured data** – JSON-LD (Organization, WebSite, Article, Product, FAQ, BreadcrumbList as relevant); validate required fields.
5. **Social/preview** – Open Graph + Twitter card tags, og:image size.
6. **Performance / Core Web Vitals** – image sizes & formats, lazy loading, render-blocking scripts, font loading, bundle size.
7. **Mobile & a11y basics** – viewport meta, tap targets, contrast, `lang` attribute.
8. **Content quality** – thin pages, duplicate content, keyword the page is meant to rank for actually appears in title/h1/first paragraph.
9. **Internal linking** – orphan pages, broken links, anchor text.
10. **AI visibility (GEO)** – `llms.txt` present; clear "who/what/where/price" facts in plain text; FAQ-style Q&A blocks; author/about/contact pages (E-E-A-T); content quotable in self-contained paragraphs.
11. **Local/brand** (if a business) – NAP consistency, Google Business Profile hints, `sameAs` links.

## Output
- Score per lane (0–10) and an overall verdict: **"Google: found / partially / not found"** and **"AI assistants: likely / unlikely to cite"**.
- Top 10 fixes ordered by impact ÷ effort, each with the exact code/file change.
- Offer to apply the fixes.
