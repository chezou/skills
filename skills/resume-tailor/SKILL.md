---
name: resume-tailor
description: Tailor an existing resume to a specific job description, using an optional episode bank (past project inventory, brag doc, STAR notes) to source concrete evidence. Includes a dedicated branch for design roles (graphic, product, UX) covering portfolios, case studies, and client work. Use this whenever the user is applying to a job and mentions a JD, a job posting URL, a company they're targeting, "this role", or asks to revise, rewrite, review, adapt, or "optimize" a resume or CV. Also use it for cover letters and application questions tied to a specific posting, and when the user pastes a resume and asks "does this work for X". Do not use it for building a resume from scratch with no target role.
license: MIT
---

# Resume Tailor

Rewriting a resume for a specific role is not a formatting job. The same career can read as a strong fit or a weak one depending on which evidence is surfaced and how it is framed. This skill turns a generic resume plus a job description into a targeted revision, grounded in what the candidate has actually done.

## Inputs

Three things, of which only the first two are required:

1. **The current resume.** A Google Doc, an uploaded file, or pasted text.
2. **The job description.** A URL, pasted text, or just a company plus role title.
3. **An episode bank** (optional but high value). Any record of past work: a task inventory, brag doc, STAR notes, performance review self-assessments, old project write-ups. This is where the specific, credible material comes from. Ask for it if the user hasn't offered it and the resume is thin on specifics.

If the Google Drive connector is available, offer to read the resume directly from Drive rather than making the user paste it. Reading the real document preserves the section structure and heading hierarchy, which matters when producing the revision.

## Step 1: Understand the target

Get the actual job description before writing anything. Do not work from the role title alone; two "Senior Software Engineer" postings can want opposite things.

- If given a URL, fetch it. Many ATS pages (Ashby, Greenhouse, Lever, Workday) are JavaScript-rendered and return nothing useful. When a fetch comes back empty, search for the posting text instead — company name plus role title plus distinctive phrases usually surfaces a mirror on an aggregator.
- Read past the requirements list. The framing language matters: a company that describes engineers wearing "PM and designer hats" is telling you what to emphasize far more clearly than its bulleted skill list does.
- Look for what is explicitly *not* required. Postings often say things like "we don't require experience in our stack." That changes the strategy from hiding a gap to addressing it honestly.

Then state the target back to the user as a short list of 3-6 things this employer is actually selecting for, plus the tech stack if relevant. Do this before proposing changes — if the read on the role is wrong, everything downstream is wrong, and the user can correct it in one line.

## Step 2: Diagnose the current resume

Name the specific mismatches between the resume as written and the target. Be concrete about the problem, not just the fix:

- **Positioning mismatch.** The headline or summary frames the candidate as one kind of engineer when the role wants another. This is usually the single highest-leverage change.
- **Evidence buried or missing.** The candidate has done the relevant thing, but it's absent, or it's one clause inside a bullet about something else.
- **Implementation-heavy, outcome-light.** Lists of technologies used, with no user, customer, or business consequence attached.
- **Wrong altitude.** Senior and staff+ roles want scope, ambiguity, and cross-functional influence. Reciting individual tickets undersells; vague leadership claims with no artifact undersell differently.

Three to five real problems beat an exhaustive list. If a section is already working, say so and leave it alone.

## Step 3: Mine the episode bank

This is where the revision gets its credibility, and it's the step most likely to be skipped.

Go through the episode bank looking for evidence that maps to the target's priorities — especially material the current resume omits entirely. The best finds are usually the ones the candidate didn't think were resume-worthy: drawing wireframes to align with PMs, discovering a customer's real need in an interview, shipping a weekend project that solved a family problem. These read as evidence of a mindset, which is exactly what senior postings screen for.

When surfacing an episode, note which target priority it serves. If it doesn't serve one, leave it out no matter how good the story is.

If there is no episode bank, ask targeted questions instead of writing filler. Two or three good questions ("Was there a time you defined what to build, not just how?") recover most of the value.

## Step 4: Write the revision

Present changes section by section, in this shape:

```
### <Section name>
**Problem:** <what's wrong with the current version>
**Revised:**
<the actual replacement text, ready to use>
**Why:** <which target priority this now hits>
```

Give real replacement text, not instructions for writing it. "Emphasize product ownership more" is not a deliverable; the rewritten bullet is.

Grouping bullets under short thematic sub-headings (Product & Technical Leadership, Scalable System Design, Cross-functional Collaboration) works well for long tenures, because it lets a skimming reader see the shape of the role rather than a flat list of twelve bullets.

Close with a short before/after comparison table covering the two or three dimensions that changed most. It gives the user a fast way to sanity-check the direction.

## Step 5: Cover letter and application questions

Only if the user wants them. The cover letter carries what the resume cannot: cultural fit, the honest framing of a gap, and the one story that explains why this role specifically.

Application questions ("tell us about a challenging project") should be answered with episodes already surfaced in Step 3, so the whole application stays consistent.

## Design roles

When the target is a graphic designer, product designer, UX designer, or similar, several things change. Apply this section in addition to the steps above, not instead of them.

**The portfolio outranks the resume.** For most design roles the resume exists to get someone to open the portfolio. Check early whether the portfolio has case studies for the pieces the resume claims. A resume bullet pointing at a project with no corresponding case study is a dead end; flag it, and if the user has to choose where to spend their time, writing one case study usually beats another resume revision.

**Read which kind of design role it is.** Postings that look similar select for opposite things:

- *Production / marketing design* wants Adobe Creative Suite fluency, multi-page layout, print specs, brand consistency, and volume. Evidence is finished deliverables.
- *Product / UX design* wants process — research, problem definition, wireframes, iteration, Figma, design systems, working with engineers. Evidence is the reasoning behind the artifact.
- *Hybrid roles* (common at small companies and in marketing teams) want both, and usually name a specific tool stack. Take the tool list literally here.

A candidate strong in one and applying to the other needs the framing shifted, not just the bullets reordered. Figma-and-research experience reads as thin for a production role unless the layout and print work is pulled forward, and vice versa.

**Count the work the candidate discounts.** Designers routinely leave out real evidence because it doesn't feel like a job:

- Paid client work, however small. Sole proprietors and small businesses are clients. Money changing hands makes it professional work.
- Coursework done to a real brief, especially solo end-to-end projects. A full redesign of a real organization's site is a case study, whether or not it shipped.
- Competition entries, including ones that didn't win. They show working to a brief and a deadline.
- Self-initiated IP: sticker sets, print-on-demand merchandise, illustration shops. These demonstrate producing to platform specs, taking work to market, and owning a visual identity — which is exactly what character, apparel, and consumer-goods employers screen for. Do not hide these as "side hustles."
- Volunteer and nonprofit work for organizations with actual stakeholders.

**Be honest about level.** Junior design postings are scarce and heavily contested, and many listings labeled junior in fact ask for several years. Do not inflate a candidate into a mid-level profile to match; it fails at the portfolio review. Position instead on the strongest true signal — a completed credential, a solo project of real scope, paid client work — and let the volume of applications do the rest.

**Bilingual and cross-cultural work is a differentiator**, not a footnote. Designing in two writing systems, or for an audience in another market, is a real skill that most applicants in the pile don't have. Give it a line rather than burying it under "languages."

**Format matters here in a way it doesn't elsewhere.** A design resume is itself a work sample. Do not hand back a rewritten resume that undoes the candidate's typography and layout. Deliver the revision as content the candidate places into their own designed document, and say so explicitly.

## The honesty rule

Never add a skill, technology, or accomplishment the candidate does not have. If the resume lists React and the user says they've never written React, remove it — do not soften it to "familiar with."

Gaps get handled by finding the true adjacent strength and naming it plainly: no professional React, but deep comfort with typed languages, Kotlin in production, type hints pushed through a Python codebase. This survives an interview. Inflation does not, and it fails at the worst possible moment.

The same applies to numbers. Use the figures the candidate actually reported. Do not invent percentages to make a bullet sound quantified, and do not round a real number upward.

## Output

Default to a markdown file with the full revision, so the user can copy sections into their own document.

Produce a `.docx` when the user asks for a document, or when a resume needs to go out as an attachment. If a Google Docs version is wanted and the Drive connector is available, create the doc directly and match the original's heading structure and styling as closely as the source document allows.

When the resume came from Drive, offer the revised version back to Drive as a new document rather than overwriting the original — candidates usually keep one resume per application.

## Language

Match the language of the resume, not the conversation. A Japanese-speaking candidate applying to a North American company needs an English resume, even when the whole discussion is in Japanese; the commentary and reasoning can stay in the conversation's language.
