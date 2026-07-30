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
The vocabulary and reply-voice tells also draw on the
[llm-smells](https://github.com/shitijkarsolia/llm-smells) skill.

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

Rewrite the sentence rather than swapping the word. A synonym dropped into the same
structure leaves the rhythm that gave the draft away.

**Never use:**

- "Additionally" at the start of a sentence
- "delve", "delving into"
- "tapestry" (as metaphor)
- "landscape" (as abstract noun, e.g., "the marketing landscape")
- "testament" (e.g., "a testament to")
- "game-changer", "game-changing"
- "unlock" (as metaphor for enabling features)
- "honestly" (as a sentence opener or intensifier, e.g., "Honestly, this was surprising")
- honesty claims: "to be candid", "the honest answer is", "my honest take is". Stating a
  claim is honest reads as a hedge against the rest not being.
- "at the end of the day"
- "boil the ocean", "swing for the fences"

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

### Borrowed Jargon Metaphors

Use a technical or business term only where it's literally accurate and a person in that
conversation would actually say it. Models reach for these as figures of speech, and
engineers now read them as a signature:

load-bearing, smoking gun, blast radius, seams, spine, backbone, substrate, ledger,
wedge, surface (as a verb), landed, spike, cutover, bake, paper-cuts,
belt-and-suspenders, earned its keep, critical path, the long pole, escape hatch, north
star, source of truth, first-class citizen, threading X through Y, the shape of.

The literal uses stay fine: a smoke test is a smoke test, and an endpoint really can be
idempotent. The tell is the metaphor, "this assumption is load-bearing," not the term.
Variants count for the same reason, so "anyone who has seen this shape before" is the tell
that "the shape of the problem" is; match on the figurative move, not the exact phrase.

Abstraction words carry the same smell when they're doing no work: directionally,
first-order, legible, parsimonious, category error, productive tension, holds multiple
truths, coordinate system, invariant. Name the actual thing instead.

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
| "it's worth noting that" | drop it |
| "when it comes to X" | "for X", "in X" |
| "at its core" | drop it |
| "the reality is", "the truth is" | drop it |
| "there is/are ... that" | rephrase directly |

Cut intensifier adverbs that add no information: just, simply, actually, truly,
genuinely, clearly, obviously, fundamentally, importantly, quietly. If the sentence is
true without them, they were decoration.

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

### Don't Narrate the Shape of Your Answer

Make the point instead of announcing that you're about to: "Stepping back, there are two
things happening here," "Put differently," "The distinction matters," "To be clear," "The
better framing is not X so much as Y." Cut the frame and keep the content.

The colon-led reveal is the same move in miniature: "Here's the thing:", "The uncomfortable
truth:", "The smoking gun:", "The takeaway:". Announcing a payoff doesn't create one.

The quietest version is the signpost sentence, which promises an explanation instead of
giving one: "Here's what happened," "this is what happened," "Below is a summary of the
issue," "Let me walk you through it." It passes every word check and still says nothing.
Replace it with what the reader actually needs to know: not "if you were affected during
that window, this is what happened," but "if your customers tried to pay during that
window, some of them couldn't."

### Don't Land Beats with Clipped Sentences

A very short sentence placed for timing rather than information is the tell that survives
every other edit. Told not to put the fragment on its own line, a draft will keep the
rhythm and move it inside the paragraph, so watch for it in all three positions:

- Alone on a line: "It wasn't." "That is the shift." "And that's not nothing."
- Closing a paragraph as a snap verdict: "It changed nothing." "Ours didn't." "That's
  where the view came from."
- Opening one as an announced diagnosis: "The cause was an N+1." "The problem was
  timing."

Each repairs the same way, by attaching the clause to the sentence it belongs with:
"prefetch_related was the first thing we tried, and nothing changed." Short sentences are
good writing when they carry the load. They are a tell when their job is percussion.

Standalone affirmations are the conversational version: "That tracks." "That holds." "The
risk is real." Say what tracks and why.

### Watch the Rhythm of Stacked Fragments

Repeating a structure and then capping it with an elevated word produces a cadence no one
uses in speech: "Fifty orders on a page, fifty extra round trips, each one fast on its own
and ruinous in aggregate." The parallel opening plus the literary payoff is a signature
even when every fact in it is correct. Say it plainly instead: "Fifty orders on a page
means fifty extra queries. Each one is only a few milliseconds, and together they are most
of a second."

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

Skip the paradox flourish too, the closing line that inverts itself for effect ("the
clarity revealed more complexity", "the fix was the problem"). Skip the recap ending that
restates what the reader just read. End on the last real point.

### Avoid Repeating a Metaphor

Once a metaphor is established, don't keep returning to it. Calling three separate things
load-bearing, or reaching for the same smoking gun in every section, turns the image into
a verbal tic. If the metaphor earns one use, it doesn't earn six.

## Formatting

### No Title Case in Headings

Use sentence case for headings: capitalize the first word and proper nouns only
("Getting started with your dashboard").

Drop the definite article too. "Architecture", "Caveats", and "What broke" beat "The
architecture", "The caveats", "The thing that broke."

### No Overuse of Bold

Reserve bold for actual emphasis (sparingly) and UI element names in instructions.
Don't bold feature names, multiple phrases per paragraph, or lists of benefits.

### Inline Code and Backticks

Use backticks only when the exact characters matter to the reader: commands, flags,
file paths, config keys and values, and short syntax fragments they will type or match.

Write names in plain prose when the sentence is about the thing rather than its spelling,
including class, function, variable, model, and field names, and library and product
names: "the Order model gets a status field," not "the `Order` model gets a `status`
field." Backtick such a name only when it would otherwise read as an ordinary English
word ("the `type` field", "pass `None`") or when it carries punctuation that looks like a
typo (`get_user()`, `--dry-run`, `settings.py`).

Restraint, not abstinence. A post that strips every backtick leaves `.filter()` and
`--dry-run` sitting bare in a sentence, where a reader sees a typo instead of a call.
Punctuation-bearing fragments keep their backticks no matter how sparse the rest is.

Traps:

- Several backticked spans in one paragraph render as scattered grey boxes and break the
  reading flow, even when each one is individually defensible.
- Backticks aren't emphasis. For a plain word that needs weight, use bold or rewrite.

Keep fenced code blocks for multi-line code and configuration; they nearly always render
well. Prefer a fenced block over a long inline span.

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

### Match the Document's Quote Style

Curly punctuation (’ “ ”) dropped into a file that uses straight ASCII (' ") marks the
text as pasted in from somewhere else. Follow whatever the surrounding document already
uses.

### Parenthetical Asides

Keep at most one aside per paragraph and never nest parentheses inside parentheses. A
draft that qualifies every clause in brackets reads as second-guessing; put the
qualification in the sentence or drop it.

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

Use sentence case in subject lines: capitalize the first word and proper nouns, but
do not capitalize every major word like a news headline. Keep them conversational.

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

## Replies and Chat Messages

When answering a person directly, in Slack, email, code review, or support, open with the
answer. That doesn't mean opening cold. A one-word acknowledgment is how people actually
reply, and dropping it makes a short message read as curt: "Yeah, I tried that first."
"No, that one's still open." What to cut is praise for the question or for the pushback,
which reads as buying time before the real reply.

- Skip the agreement preamble: "You're right to push back", "You're absolutely right",
  "Great question", "I appreciate you pressing on this", "Fair question".
- Skip self-flagellation: "That's on me", "I should have caught that sooner". Correct the
  thing and move on.
- Skip the unrequested retrospective: "What I'd do differently", "Going forward I'd be
  more deliberate about...". Add it only when asked.
- Skip performed thinking: "Let me verify one thing", "Let me read this rather than answer
  from memory", "Let me trace through this carefully". Do it, then report what you found.
- Skip the ceremony around a correction: "After further review", "Upon deeper reflection",
  "Now I have the full picture". State the corrected fact.
- Skip engagement bait and filler offers, which invite a response without putting anything
  on the table: "Would love to hear your thoughts", "Happy to help", "Let me know if you
  have any questions".
- Close by handing the decision back when there is one. Proposing an option and stopping
  leaves the other person guessing whether you want an answer, so end on the question:
  "Want me to add that before we merge?", "What do you think?" In chat especially, a reply
  that ends flat reads as closing the thread rather than continuing a conversation.
- Commit to an answer. Hedges that face both ways ("may still be defensible, but", "not
  exactly resolved, but") leave the reader with nothing to act on.

## Quick Self-Check

Before publishing, read it aloud: could a colleague have said this, does every sentence
add information, and did any words from the avoid lists slip through? The revision should
come out shorter than the draft; if it grew, the edit added padding instead of cutting it.
