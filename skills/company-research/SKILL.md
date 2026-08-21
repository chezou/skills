---
name: company-research
description: Research a company a candidate is applying to or interviewing with, and produce a one-page brief covering what the company does, how it makes money, the shape of the team, warning signs, and interview preparation. Use this when the user names a company they are applying to, asks "what should I know about X before my interview", asks whether a company is worth applying to, wants questions to ask an interviewer, or is preparing for a specific interview round. Pairs with resume-tailor, which handles the application documents themselves. Do not use this for competitive analysis, investment research, or vendor due diligence.
license: MIT
---

# Company Research

A candidate researching an employer needs different things than an analyst researching a business. The questions are: would I want to work here, will they want me, and what do I say in the room. This skill produces a brief that answers those, grounded in sources rather than impressions.

## Research budget

Decide the depth before starting, and say which mode is running so the user can redirect.

- **Quick pass (default).** Steps 1, 2, 4, and 7, plus the recent-news search from Step 6 — roughly 8-12 page fetches total. This is enough to decide whether a posting is worth a tailored application, which is the common case.
- **Full brief.** All eight steps, roughly 20-30 fetches. Run this only when the user has an interview scheduled or explicitly asks for the full version.

Within either mode: prefer one good source per question over three that agree. Search results pages often answer the question in the snippet — fetch the page only when the detail actually matters. Stop researching a question once it is answered, and stop the whole pass once the brief can be written; an unanswered item is a legitimate line in the output.

If a step is turning up nothing after two attempts, write "not public" and move on rather than trying more sources.

## Step 1: Establish the basics

Find these before anything else, because they set the shape of every later answer:

- **What the company sells, and to whom.** Say it in one sentence. If that sentence is hard to write from the company's own site, that is itself a finding.
- **How it makes money.** Subscription, ads, services, hardware margin, agency retainer. Revenue model determines which teams are cost centers and which are the core.
- **Size and stage.** Headcount, founding year, funding stage or private/public status, whether it's a subsidiary. A 40-person Series A and a 4,000-person public company behave nothing alike.
- **Where the role sits.** Which team, reporting to what function, and whether the office is in the candidate's region. For hybrid or on-site roles, get the actual office location, not the headquarters listed on the website.

Use the company's own site first, then a business database (Crunchbase, LinkedIn company page, corporate registry for private companies) to check what the site is quiet about.

## Step 2: Place them in their market

A company's competitive position determines what it needs from the person it hires. This is the difference between an interview answer that sounds informed and one that sounds like it came off the About page.

- **Name the two or three direct competitors** and what separates this company from them. The differentiator is usually one thing: an incumbent's scale, a challenger's specific technical bet, a niche nobody large bothers to serve. If the candidate can articulate that bet, they can talk about the role in terms of the company's actual problem.
- **Look at who their customers are.** A published customer list is a strategy statement — it shows which segment they've won and which they're reaching for. Whether the logos skew enterprise or startup, domestic or international, tells the candidate what the work will actually feel like.
- **Check whether the company is defending or attacking.** An incumbent losing share behaves differently from a challenger with momentum, and each wants different traits in a hire.

## Step 3: Read what they say about themselves

Most companies publish values. What matters is whether they are specific enough to be falsifiable.

- **Generic values** (integrity, innovation, teamwork) carry no information. Note their presence and move on.
- **Specific operating principles** are worth reading closely, because they predict daily working conditions. A company that publishes something like "we hold almost no meetings" or "engineers write the product spec" is describing a real workflow, and one the candidate can ask concrete questions about.
- **Check whether the stated principles match the postings and the reviews.** A company claiming deep autonomy while every JD lists rigid process requirements is telling on itself. Alignment is a good sign; contradiction is a flag worth raising in the brief.
- **Look for what they say about hiring specifically.** Companies that describe a deliberately slow or high-bar process are warning the candidate that the pipeline will be long. That's useful for planning, not a reason to skip applying.

**Growth health, where it's visible.** For companies that publish or leak these — funding announcements, press coverage, engineering blog posts — a few figures say more than the headline raise: revenue growth rate, customer count over time, burn relative to growth, retention or churn. A company that raised a large round and has barely spent it is in a very different position from one raising to cover a shortfall, even though both announce a round. Treat all of these as estimates unless the company is public, and say so.

## Step 4: Read the job market signal

The company's other postings say more than any single JD.

- **Look at everything they have open right now.** Twenty engineering roles and no design roles tells the candidate what this company thinks it is. A single designer position at a 200-person company means that person will be alone; ask whether that's what the candidate wants.
- **Check whether this specific role has been reposted.** A posting that has cycled repeatedly over months usually means an unrealistic bar, a compensation mismatch, or a difficult hiring manager. This is worth knowing before investing in a tailored application.
- **Read the seniority spread.** All senior and staff openings with no junior roles indicates a company that isn't set up to train. All junior roles indicates budget pressure or churn.
- **Note the tool and stack names that repeat** across postings. These are the real requirements, as opposed to the aspirational list in any one JD.

## Step 5: Look at the people

**Start at the top for smaller and private companies.** At a startup or an owner-run business, the founders and the board are the company's strategy. This step matters less at a large public company, where the CEO's background rarely reaches an individual team.

- **Founders' prior companies and roles.** A founding team out of a specific industry builds the company that industry taught them to build. Repeat founders behave differently from first-timers. A technical founder and a sales founder produce very different internal cultures.
- **How long the founders have been at it.** Eight years in without an exit means something different from eighteen months post-launch.
- **Board members and investors.** Who funded them signals both the expected growth trajectory and the pressure the company is under. A board seat held by a fund known for aggressive timelines predicts a different work environment than one held by a family office or a strategic corporate investor.
- **What leadership says in public.** Interviews, conference talks, podcasts, and the company blog. Founders describe their actual priorities far more candidly in a podcast than in a careers page. This is also where the candidate finds the specific thing to reference in an interview.

Keep this to professional history — prior roles, companies, investments, public statements. Personal life is neither relevant nor appropriate here.

Then look at the level the candidate will actually work at:

- **Find who currently holds similar roles**, via LinkedIn or the company's team page. Their backgrounds show what the company actually hires, which is often looser than the JD implies. If everyone in the role came from a different industry, the candidate's non-obvious background is less of a problem than they think.
- **Check tenure.** A team where nobody has passed two years is a signal. So is a team where everyone has been there eight years and no one new has joined.
- **Identify the likely interviewer** where possible — the hiring manager or team lead. Knowing whether that person came up through the craft or from management changes how the candidate should pitch.
- **Look for recent departures** in the relevant team. A vacancy backfilling a long-tenured person is a different job than a newly created seat.

## Step 6: Find the unglamorous facts

These are the ones candidates skip and regret:

- **Recent news**: layoffs, funding rounds, acquisitions, leadership changes, product sunsets. Search the last twelve months specifically, and weight the last three months heavily.
- **Employee reviews**, read skeptically. Glassdoor and Indeed skew toward the angry and the coached. What's useful is repetition: the same specific complaint from many people over time is a real pattern; one detailed rant is not. Read the most recent reviews first, since old complaints may describe a management team that has since left.
- **Whether the company sponsors visas or requires local work authorization**, when relevant to the candidate.
- **Actual compensation data** for the role and region, from a salary database rather than the company's own claim. If the posting has no range and the jurisdiction requires one, note that.

## Step 7: Use the product

Spend a bounded amount of time looking at whatever the company makes: the product pages, the app store listing and its recent reviews, their social feeds and recent campaigns. Two or three pages is usually enough; this is not a full product audit.

This is the single highest-return step for interview preparation, and most candidates skip it. It produces specific observations, which are what interviewers remember. For design roles especially, an actual read on the company's visual language, brand consistency, and where the work is uneven is far more persuasive than any general enthusiasm.

Note two or three concrete things: something done well, something that seems unfinished, and something the candidate would want to ask about. The third one becomes an interview question.

## Step 8: Produce the brief

Keep it to roughly one page. Structure:

```
## <Company> — <role>
**What they do:** <one sentence>
**Business model:** <how money comes in>
**Size / stage:** <headcount, funding or public status, founded>
**Position:** <who they compete with, what their bet is>
**How they work:** <stated operating principles, where specific>
**The team:** <where the role sits, who's around it>

### Why the candidate fits
<2-4 points connecting real background to real needs>

### Gaps to address
<what they'll probe, and the honest answer>

### Flags
<what looks off, with the evidence — or "nothing notable">

### Questions to ask
<4-6 specific to this company, not generic>

### Likely questions from them
<3-5, drawn from the JD's emphasis>
```

The questions-to-ask section is where the research pays off visibly. "Where do you see the company in five years" signals nothing. A question about a specific product decision, a recent launch, or how the team handled a change the candidate noticed signals preparation that can't be faked.

## Sourcing discipline

Mark what is verified and what is inferred. A brief that reads confidently but mixes the company's press release with a Reddit comment is worse than no brief.

- Cite where each non-obvious claim came from, and give the date. Headcount and funding figures go stale fast.
- For private companies, revenue figures are usually estimates. Say so rather than presenting a number as fact.
- Do not fill gaps with plausible-sounding invention. "Their design team size isn't public" is a legitimate line in a brief.
- When sources conflict — a company claiming growth while reviews describe cuts — present both and let the candidate weigh it.

## Timing

Match the depth to the stage, per the research budget above. Before applying, the quick pass is enough to decide whether to invest in a tailored application. Run the full brief before a scheduled interview, and re-check the news search the day before, since a funding round or layoff announcement changes the conversation entirely.
