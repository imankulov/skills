---
name: writing
description: |
  Guidelines for clear, human-sounding prose. Use when writing any text humans will
  read: documentation, Slack messages, emails, commit messages, error messages,
  changelogs, support responses, marketing copy, landing pages, internal updates,
  reports, or UI text. Also use when reviewing drafts for AI tells or editing text
  to sound natural.
  Do NOT use for: agent instructions (AGENTS.md, SKILL.md, CLAUDE.md), or other files
  primarily read by AI agents.
metadata:
  imankulov.skills-sh-group: Writing
  imankulov.skills-sh-order: "10"
  imankulov.claude-display-name: Writing
  imankulov.claude-category: development
  imankulov.claude-keywords: "writing,agent-skills"
---

# Writing Guidelines

These guidelines ensure text sounds human and authentic. Based on Strunk's *Elements of
Style* and documented patterns of AI-generated text (see
[Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

## Grammar and Punctuation

- Form the possessive singular by adding 's: "Charles's friend", not "Charles' friend."
- In a series of three or more terms, use a comma after each except the last:
  "red, white, and blue."
- Don't join independent clauses with just a comma (comma splice). Use a semicolon, a
  conjunction, or split into two sentences.
- A participial phrase at the beginning of a sentence must refer to the grammatical
  subject: "Walking to the store, **I** noticed..." not "Walking to the store, **the
  rain** started."

## Words and Phrases to Avoid

These words are statistically overused in AI-generated text and signal inauthenticity.

**Never use:**

- "Additionally" at the start of a sentence
- "delve", "delving into"
- "tapestry" (as metaphor)
- "landscape" (as abstract noun, e.g., "the marketing landscape")
- "testament" (e.g., "a testament to")
- "game-changer", "game-changing"
- "unlock" (as metaphor for enabling features)
- "honestly" (as a sentence opener or intensifier, e.g., "Honestly, this was surprising")

**Use sparingly or find alternatives:**

| Avoid | Instead |
|-------|---------|
| crucial | important, matters, essential |
| enhance | improve, make better |
| leverage | use |
| utilize | use |
| pivotal | important, key |
| showcase | show, demonstrate |
| underscore | show, emphasize |
| foster | encourage, support, build |
| garner | get, earn, attract |
| intricate | detailed, complex |
| vibrant | active, lively |
| robust | strong, reliable |
| seamless | smooth, easy |
| empower | help, enable, let |
| bolstered | strengthened, supported |
| meticulous/meticulously | careful, thorough |
| enduring | lasting |
| interplay | interaction, relationship |
| align with | match, fit, follow |
| profound | deep, significant |
| renowned | well-known, respected |
| nestled | located, set |
| in the heart of | in, in central |
| diverse array | range, variety |
| commitment to | focus on, dedication to |
| valuable insights | (be specific: name the insight) |

## Composition

### Use Active Voice

Prefer "the team shipped the feature" over "the feature was shipped by the team." Use
passive only when the actor is unknown or genuinely irrelevant.

### Put Statements in Positive Form

Say what something is, not what it isn't. If you write "not X", check whether a direct
word exists.

| Avoid | Use instead |
|-------|-------------|
| "not honest" | "dishonest" |
| "not important" | "unimportant", "minor" |
| "did not remember" | "forgot" |
| "did not have much confidence in" | "distrusted" |
| "not unless" | "only if" |

### Omit Needless Words

| Cut | To |
|-----|----|
| "the reason why is that" | "because" |
| "the fact that" | drop it |
| "in order to" | "to" |
| "at this point in time" | "now" |
| "it is important to note that" | drop it |
| "there is/are ... that" | rephrase directly |

### One Paragraph, One Topic

Develop a single idea per paragraph, and start with the topic sentence so readers can
skim.

### Parallel Construction

Express co-ordinate ideas in the same grammatical form: "The system handles logging,
alerting, and monitoring," not "handles logging, is responsible for alerting, and
monitoring is also included."

### Keep Related Words Together

Place subject near verb, verb near object. Don't strand modifiers far from the words
they modify.

### Place the Emphasis at the End

Put the most important word where it lands with weight: "This technology opens
possibilities humanity has barely begun to explore," not "Humanity has barely begun to
explore the possibilities of this technology."

### Keep to One Tense in Summaries

When summarizing events or changes, pick one tense; don't drift between past and present.

## Sentence Structure

### Use Simple Verbs

| Avoid | Use instead |
|-------|-------------|
| "serves as" | "is" |
| "stands as" | "is" |
| "represents" | "is" |
| "marks" | "is" |
| "maintains" | "has", "keeps" |
| "boasts" | "has" |
| "features" | "has", "includes" |
| "offers" | "has", "gives you" |

### Avoid Negative Parallelisms

Make your point directly instead of setting up a contrast: "Not only X, but Y"; "It's
not just about X, it's about Y"; "X isn't just Y, it's Z".

### Avoid the Rule of Three

AI overuses triplets ("fast, reliable, and secure"; "track, analyze, and optimize").
Use one or two descriptors, and if you need three, make sure each adds distinct meaning.

### Avoid False Ranges

Don't use "from X to Y" when X and Y aren't endpoints of a scale ("from small startups
to enterprise companies, from marketing to engineering teams").

### Avoid Empty "-ing" Phrases

Present participles tacked on to fake depth add words without meaning: "highlighting its
importance," "emphasizing the need for," "ensuring reliability," "reflecting broader
trends," "symbolizing its ongoing commitment." Drop them and state the point.

### Avoid Elegant Variation

Don't cycle through synonyms for the same thing ("the platform," "the tool," "the
solution," "the system"). Repeating the right word beats forcing an unnatural synonym.

### Avoid Vague Attributions

Don't attribute claims to unnamed authorities ("Experts argue," "Industry reports
suggest," "Observers have noted," "Some critics argue"). Name the source or drop it.

### Avoid the "Despite" Formula

Skip formulaic conclusions like "Despite its [positive qualities], [subject] faces
challenges such as [list]." Discuss challenges concretely or leave them out.

## Formatting

### No Title Case in Headings

Use sentence case for headings: capitalize the first word and proper nouns only
("Getting started with your dashboard").

### No Overuse of Bold

Reserve bold for actual emphasis (sparingly) and UI element names in instructions.
Don't bold feature names, multiple phrases per paragraph, or lists of benefits.

### No Emoji in Professional Text

Never use emoji in email subject lines, marketing headers, documentation, or support
responses.

### Bullet Lists

Keep bullets short. Avoid the **Bold header:** followed by description pattern.

Bad:
- **Easy Setup:** Get started in minutes with our simple installation process.
- **Real-time Data:** See visitor activity as it happens on your site.

Good:
- Get started in minutes
- See visitor activity in real-time

### Em Dashes

Don't use em dashes. Replace with commas, colons, conjunctions, or rephrase. Em dashes
are overused in AI-generated text.

### Colons and Choppy Sentences

When replacing em dashes, don't mechanically swap them for colons or split into short
sentences; both produce the same staccato feel. Use conjunctions (because, where, while,
since, and) to merge related ideas into one flowing sentence: "A CLI script is the
simplest option, because the agent calls it via Bash," not "A CLI script is the simplest
option: the agent calls it via Bash." If a sentence is already long, a period is fine.

## Email Subject Lines

Bad:
- "Unlock Your Website's Full Potential"
- "Your Weekly Analytics Insights Are Here!"
- "Don't Miss Out: New Features Just Dropped"

Good:
- "Your weekly report"
- "New: filter by country"
- "Traffic spike on your site"

Keep subject lines lowercase (except proper nouns) and conversational.

## Tone

1. **Be direct.** Say what you mean in the fewest words.
2. **Be specific.** "See which pages get the most visits" beats "gain valuable
   insights into your content performance."
3. **Sound like a person wrote it.** Read it aloud. If it sounds like a press release,
   rewrite it.
4. **Contractions are fine.** "You'll see" is better than "You will see."
5. **Avoid marketing superlatives.** Don't call things "powerful", "cutting-edge", or
   "revolutionary."
6. **Don't hedge.** Avoid "helps you to", "allows you to", "enables you to". Just say
   what it does. Exception: in help text, "may", "usually", and "often" are fine
   when they set accurate expectations for behavior that depends on the user's data.

### Make Help Text Reader-Led

For help pages and docs, connect the explanation to the reader's situation.

- Start from what the reader may see: "If your engagement rate dropped..."
- Use "you" when it clarifies the next action or expected result.
- Say what to check, where to find it, and what may change after the action.
- Use "may", "usually", and "often" only when the outcome truly depends on the user's data.

Avoid fake warmth, rhetorical questions, and adding "you" to every sentence.

## Outbound Email Voice

For outbound emails (announcements, outreach, follow-ups) from a solo founder or small
team:

- Use "I", never "we" or "our team"
- Write plain text, no HTML templates or fancy formatting
- Admit what you don't know or what doesn't work yet
- Offer genuine value, not just ask for favors
- Don't pretend to be bigger than you are
- Don't use corporate language ("contact our support team", "we're excited to announce")
- Don't frame bug fixes or resolved issues as "good news." Saying "Good news: we fixed
  the issue" when the issue was on your end sounds fake. Just state what you did.

## Quick Self-Check

Before publishing, read it aloud: could a colleague have said this, does every sentence
add information, and did any words from the avoid lists slip through?
