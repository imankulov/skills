# Docstrings and Comments

## Plain text, written to be scanned

A docstring is plain English, not a rendered document. No RST, no Markdown: no headers,
no `**bold**`, no doubled backticks, no bold "label:" prefixes on list items. Wrapping one
identifier in single backticks or quotes is fine where the bare word would otherwise read
as ordinary English, as with an identifier named id, type, or all.

Prefer a plain bulleted list to prose wherever the content allows one:

- conditions under which something applies
- cases a value can take
- steps a caller performs in order
- things a function does

A reader scanning for one branch finds it on its own line. The same items stitched
together with "and"/"or" make them read the whole sentence to learn none of it applied.
Reserve prose for what doesn't decompose: a continuous explanation, a "why" that only
works as an argument.

## Start at one line

Default to a one-line docstring. Most functions, methods, and classes need nothing more.

When one line isn't enough, use the shape PEP 257 defines: a one-line summary, a blank
line, then the elaboration. Reach for Google-style sections only on top of that:

- `Raises:` whenever the function raises on purpose — entry points read that contract to
  decide what to catch.
- `Args:` / `Returns:` when a parameter's meaning or a non-obvious return value can't be
  read off the signature.

Most functions need none of the three; don't add them by reflex.

A docstring is either a true one-liner or a title plus a body. A single sentence wrapping
across two or three lines with no blank line after it is neither — shorten it until it
fits on one line, and let it grow into the title-plus-body shape only when there's a real
second sentence or list to add.

## Say only what the code can't

Start minimal and add a line only where something would otherwise be unclear: a hidden
invariant, a non-obvious "why", a workaround for a specific bug. Don't restate what a type
hint or a well-named variable already says.

Stay evergreen: state the rule, not the one-off observation that prompted it. Row IDs,
ticket numbers, and "verified on X" notes belong in a commit message or a pull request
description, not in a docstring that outlives them.

## Inline comments

The same rules apply, and the default is none. When one is needed, keep it to the
non-obvious "why", above the line it explains, not a play-by-play of what the code does.

## Tone

Apply the **writing** skill: plain, human sentences, no AI-writing tells.
