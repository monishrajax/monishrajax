<!--
  FARM-THEMED PROFILE README
  ---------------------------------------------------------------------------
  Still to fill in (search this file for "TODO"; each spot shows a friendly "coming soon" note until then):
    - 01  NAME / EDUCATION / LOCATION rows in the dossier
    - 02  experience, leadership and education cards
    - 05  achievements        06  certifications
    - 08  LinkedIn / portfolio / email links
  Banners, tags, project cards, farm animals and the tech carousel are generated:
    python3 scripts/build_assets.py        (edit the CONFIG block at the top first)
  The crop-yield graph (assets/yield.svg) and the repo table below refresh by themselves:
    .github/workflows/farm-yield.yml  ->  scripts/update_yield.py
-->

<div align="center">

<img src="assets/hero.svg" alt="MONISHRAJAX - full-stack, applied AI and cloud. A green farm at sunrise with a windmill, a red barn and a tractor driving past, while cows, sheep, a pig, hens, a duck, a dog and a crowing rooster go about their day." width="100%">

<img src="assets/growth.svg" alt="Growth bar: seed, sprout, grow, bloom, harvest" width="100%">

</div>

<br>

<img src="assets/sec-01-dossier.svg" alt="01 - Farmer's Dossier" width="100%">

<!--
  TODO: add these rows to the table below (above SPECIALIZATION) once you have the details:
  | `NAME` | Your full name |
  | `EDUCATION` | University · degree · years |
  | `LOCATION` | City, country |
-->

| | |
|:--|:--|
| `FARMER ID` | **monishrajax** &nbsp;·&nbsp; [github.com/monishrajax](https://github.com/monishrajax) |
| `SPECIALIZATION` | Full-Stack Development & Applied AI |
| `STATUS` | **PLANTING // GROWING // HARVESTING** |

- Full-stack developer who ships products end to end: React and Next.js front ends, Express and Flask back ends, Postgres and Supabase underneath.
- Shipped and online: **NORMALIZE** (a single-product storefront built with Razorpay checkout), **VisaGuard** (an agentic-AI compliance platform demo) and **Don't Touch the Floor** (a multiplayer arcade game).
- Hands-on with applied AI: TF-IDF and cosine-similarity retrieval, in-browser OCR pipelines and agentic-AI product interfaces.
- Comfortable with the delivery side too: Docker, Kubernetes and GitHub Actions CI/CD.
- Philosophy: plant early, water daily (commit), harvest often (ship).

<br>

<img src="assets/sec-02-experience.svg" alt="02 - Experience and Leadership" width="100%">

> 🌱 *Fresh soil: roles, leadership and education are being planted here. Check back soon.*

<!--
  TODO: replace the note above with your real cards. Use one tag image per group:
    <img src="assets/tag-professional.svg" height="32" alt="Professional">   then your roles, newest first
    <img src="assets/tag-leadership.svg" height="32" alt="Leadership">       clubs, communities, events, teams
    <img src="assets/tag-education.svg" height="32" alt="Education">         school or university, degree, years

  EXAMPLE CARD - copy, paste and edit for each role:

  <table>
  <tr><td>

  <img src="assets/tag-professional.svg" height="30" alt="2026 - present">

  **Role title** · Company

  - What you built or shipped, and the result.
  - Another concrete achievement.

  </td></tr>
  </table>
-->

<br>

<img src="assets/sec-03-projects.svg" alt="03 - Projects" width="100%">

<img src="assets/tag-featured.svg" height="32" alt="Featured fields">

<br>

<a href="https://www.normalize.world"><img src="assets/project-01-normalize.svg" alt="Plot 01 - NORMALIZE: storefront for a single-product launch. Live. React, Vite, Tailwind, Express, Supabase." width="100%"></a>

- Single-product launch storefront: React 18 + Vite + Tailwind CSS v4 client, Express API, Supabase Postgres.
- Server-side pricing: the browser never sends a price. The API looks it up in Postgres and opens the Razorpay order, verifies the HMAC-SHA256 payment signature, and a webhook settles orders even if the customer's browser dies mid-checkout.
- Shiprocket logistics, plus a "launch mode" that opens the full catalogue with one database update and no redeploy.
- 33 automated checks run against a throwaway Postgres and the real server: catalogue, pricing, the payment-signature gate and the webhook.

**[▸ Live site](https://www.normalize.world)** &nbsp;·&nbsp; **[▸ Source](https://github.com/monishrajax/normalize-website)**

<br>

<a href="https://dont-touch-the-ground.vercel.app"><img src="assets/project-02-floor.svg" alt="Plot 02 - Don't Touch the Floor: prison-break arcade platformer with multiplayer. Live. Canvas, JavaScript, CSS, Vercel." width="100%"></a>

- Prison-break arcade platformer: hop between steel beams, dodge sawblades, shock orbs and barbed wire while a laser alarm floor keeps rising.
- Plain HTML5 Canvas, CSS and JavaScript: no dependencies and no build step. Touch controls for phones.
- Multiplayer: friends race up the same tower by sharing a 5-character game code, with a live scoreboard.

**[▸ Play it](https://dont-touch-the-ground.vercel.app)** &nbsp;·&nbsp; **[▸ Source](https://github.com/monishrajax/Dont-touch-the-ground)**

<br>

<a href="https://visa-smoky-rho.vercel.app"><img src="assets/project-03-visaguard.svg" alt="Plot 03 - VisaGuard: agentic-AI PCI and PII compliance platform. Live. Next.js, TypeScript, Tailwind, Framer Motion, Vercel." width="100%"></a>

- Marketing and demo site for an agentic-AI-enabled, continuous PCI / PII compliance platform.
- Next.js (App Router) + TypeScript + Tailwind CSS, with Framer Motion micro-interactions and Recharts dashboards.
- Built-in light / dark / system theme toggle.

**[▸ Live demo](https://visa-smoky-rho.vercel.app)** &nbsp;·&nbsp; **[▸ Source](https://github.com/monishrajax/visa)**

<br>

<a href="https://github.com/monishrajax/Smart-Resume-Job-Matching-Information-Retrieval-System"><img src="assets/project-04-resume.svg" alt="Plot 04 - Smart Resume Matcher: TF-IDF and cosine similarity retrieval system. Python, Flask, React, TypeScript, scikit-learn." width="100%"></a>

- Full-stack information-retrieval app that ranks uploaded resumes by relevance to a job description.
- Flask REST API: NLTK preprocessing (tokenisation, stop-word removal, lemmatisation), TF-IDF vectors and cosine-similarity ranking with scikit-learn.
- React + TypeScript + Tailwind UI that lists ranked results with similarity percentages.

**[▸ Source](https://github.com/monishrajax/Smart-Resume-Job-Matching-Information-Retrieval-System)**

<br>

<a href="https://github.com/monishrajax/ID-scanner"><img src="assets/project-05-idscanner.svg" alt="Plot 05 - ID Scanner: OCR attendance system for student IDs. React, Vite, Supabase, Tesseract.js." width="100%"></a>

- Attendance system: capture or upload a student ID, run OCR in the browser with Tesseract.js, auto-detect the roll number and mark attendance.
- Supabase stores members, events and attendance, with a unique (roll number, event) constraint to block duplicate check-ins.
- React 18 + Vite with real-time toast feedback.

**[▸ Source](https://github.com/monishrajax/ID-scanner)**

<br>

<a href="https://github.com/monishrajax/microservices-ci-cd"><img src="assets/project-06-cicd.svg" alt="Plot 06 - Microservices CI/CD: commit, build, container, cluster. GitHub Actions, Docker, Kubernetes, Node.js." width="100%"></a>

- Automates the whole delivery lifecycle: a push to GitHub triggers GitHub Actions, which builds the app, containerises it with Docker and deploys it to a Kubernetes cluster.

**[▸ Source](https://github.com/monishrajax/microservices-ci-cd)**

<br>

<img src="assets/tag-barn.svg" height="32" alt="The barn: all repositories">

<!-- REPOS:START -->
| Repo | What's growing | Stack | Live | Updated |
|:--|:--|:--|:--:|:--:|
| [**normalize-website**](https://github.com/monishrajax/normalize-website) | Storefront for a single-product launch with Razorpay checkout | React · Express · Supabase | [open](https://www.normalize.world) | 2026‑11‑20 |
| [**Dont-touch-the-ground**](https://github.com/monishrajax/Dont-touch-the-ground) | Prison-break arcade platformer with multiplayer races | JavaScript · Canvas | [open](https://dont-touch-the-ground.vercel.app) | 2026‑10‑17 |
| [**Smart-Resume-Job-Matching-Information-Retrieval-System**](https://github.com/monishrajax/Smart-Resume-Job-Matching-Information-Retrieval-System) | Ranks resumes against a job description (TF-IDF + cosine) | Flask · React · scikit-learn | — | 2026‑04‑06 |
| [**microservices-ci-cd**](https://github.com/monishrajax/microservices-ci-cd) | Commit → build → Docker → Kubernetes delivery pipeline | GitHub Actions · Docker · K8s | — | 2026‑04‑06 |
| [**CIGA-Business-Analytics-Framework**](https://github.com/monishrajax/CIGA-Business-Analytics-Framework) | Real-time intent analytics system that turns user behavior into actionable business insights *(fork)* | Python | — | 2026‑04‑01 |
| [**visa**](https://github.com/monishrajax/visa) | VisaGuard: agentic-AI PCI / PII compliance platform demo | Next.js · TypeScript | [open](https://visa-smoky-rho.vercel.app) | 2026‑01‑05 |
| [**ID-scanner**](https://github.com/monishrajax/ID-scanner) | OCR attendance scanner for student IDs | React · Tesseract.js · Supabase | — | 2025‑12‑20 |
| [**certifi-gen**](https://github.com/monishrajax/certifi-gen) | — | — | — | 2025‑12‑20 |
<!-- REPOS:END -->

<br>

<img src="assets/sec-04-arsenal.svg" alt="04 - Tech Arsenal" width="100%">

<img src="assets/arsenal.svg" alt="Scrolling carousel of tools: JavaScript, TypeScript, Python, HTML5, CSS3, React, Next.js, Tailwind, Vite, Framer, Node.js, Express, Flask, Supabase, PostgreSQL, scikit-learn, Docker, Kubernetes, GitHub Actions, Vercel, Git and GitHub." width="100%">

| | |
|:--|:--|
| `LANGUAGES` | JavaScript · TypeScript · Python · HTML · CSS |
| `FRONT END` | React · Next.js · Vite · Tailwind CSS · Framer Motion · Recharts |
| `BACK END` | Node.js · Express · Flask · REST APIs |
| `DATA & AI` | Supabase · PostgreSQL · scikit-learn · NLTK · Tesseract.js |
| `INTEGRATIONS` | Razorpay · Shiprocket |
| `CLOUD & DEVOPS` | Docker · Kubernetes · GitHub Actions · Vercel · Git |

<br>

<img src="assets/sec-05-achievements.svg" alt="05 - Achievements" width="100%">

<!-- TODO: add hackathons, awards, rankings or published work: one bullet each, newest first. Then delete the note below. -->
> 🏆 *The trophy shelf is being polished. Achievements land here soon.*

<br>

<img src="assets/sec-06-certifications.svg" alt="06 - Certifications" width="100%">

<!--
  TODO: add your certifications as a table and delete the note below, for example:
  | | |
  |:--|:--|
  | `Google` | Introduction to Generative AI |
-->
> 🌾 *Certificates are still drying in the barn. Check back soon.*

<br>

<img src="assets/sec-07-metrics.svg" alt="07 - System Metrics" width="100%">

<img src="assets/yield.svg" alt="Crop yield: contributions in the last 12 months, current streak, longest streak and public repos, drawn as a field where every active day grows a tuft of grass." width="100%">

<sub>Last 12 months · every active day grows grass · refreshed automatically by a GitHub Action · live graph: [github.com/monishrajax](https://github.com/monishrajax)</sub>

<br>

<img src="assets/sec-08-connect.svg" alt="08 - Establish Connection" width="100%">

<p align="center">
<a href="https://github.com/monishrajax"><img src="assets/badge-github.svg" height="42" alt="GitHub"></a>
<!--
  TODO: uncomment these and add your own links
  <a href="https://www.linkedin.com/in/YOUR-HANDLE"><img src="assets/badge-linkedin.svg" height="42" alt="LinkedIn"></a>
  <a href="https://YOUR-PORTFOLIO.example"><img src="assets/badge-portfolio.svg" height="42" alt="Portfolio"></a>
  <a href="mailto:you@example.com"><img src="assets/badge-email.svg" height="42" alt="Email"></a>
-->
</p>

<br>

<div align="center">

<img src="assets/footer.svg" alt="Thanks for visiting the farm. Built with soil, sun and a lot of commits. A cow, sheep, hens, a pig, a duck, a dog and a rooster stand together in the wheat." width="100%">

<sub>Hand-built SVG art, generated by <code>scripts/</code> · type set in Alfa Slab One &amp; Space Mono (SIL OFL 1.1) · logos from Simple Icons (CC0)</sub>

</div>
