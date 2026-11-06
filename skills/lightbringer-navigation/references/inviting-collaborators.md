# Inviting collaborators

Use this guidance when a saved innovation or Strategy has other people who should validate it, or when the user asks to invite someone to it. An invitation brings a colleague into the user's current Lightbringer organisation with access to that document. Inviting is optional; keep the main task moving.

## When to propose

Propose inviting only once the document has substance and is saved, typically after a confirmed save and readback rather than at the start of capture. Look for people who should validate it:

- co-inventors or contributors named in the disclosure or the conversation;
- people the user describes as owning the decision, such as a co-founder or CTO for a Strategy;
- inventors named on the organisation's own related patents saved in Lightbringer.

Make one short offer naming the people you noticed. Propose at most once per document in a conversation; if the user declines or does not take it up, do not raise it again for that document unless they bring it up. A direct request such as “invite the engineering team to this” can come at any point. Lightbringer invitations are for individual people, so resolve a group to named individuals with the user.

## Prepare the list

Take email addresses only from the user, or from a source the user has connected and pointed you to, such as a company directory or contact list. Never guess or construct an address, for example from a name and the company's domain, and do not fill gaps from memory or public search. Look people up by name only; do not put document content into those lookups. If an address is missing, ask for it or leave that person out.

Choose a role for each person:

- **Inventor** (default): sees only the documents shared with them. Suits co-inventors and contributors.
- **Inventor + Moderator:** sees all of the organisation's innovations and Strategies. Suggest it only for people who own company-level decisions, such as a co-founder or CTO, and say why.

Higher roles cannot be granted through the assistant; they are managed in the Team settings of the Lightbringer application.

Only a published Strategy can be shared. If the Strategy is a draft, explain this and suggest publishing it first. Publication makes the Strategy organisation-wide context and needs the user's explicit request; a request to invite someone does not authorise it.

## Approve, then send

Before sending, show the exact list: each person's name, email address and role, and the document they will get access to. Send only after the user approves that list. If they correct it, send only the corrected version they approve. Approval to save or publish a document is not approval to invite anyone.

Explain what the invitee receives: an email from Lightbringer showing the user as the inviter, naming the organisation and identifying the document by reference number only, with no title, content or personal note. Suggest the user message the person directly if they want to add context.

Use `invite_members` when the connection advertises it, following its schema, with one call for the approved people and document. Report each person's outcome plainly:

- **Invited:** the invitation was sent; accepting gives access to the document.
- **Already invited:** the pending invitation was re-sent with the document and keeps its earlier role.
- **Already a member:** no invitation was needed; the person was given access to the document. If some documents could not be shared, name them; the others were shared.
- **Refused:** not invited, with the reason the service returned.

If an invitation was saved but its email could not be sent, say so and point to the Team settings, where it can be re-sent; do not send it again through the tool.

If the service rejects the request, nothing was sent: explain the reason it gives and do not work around it. Emails cannot be recalled, so after an uncertain outcome do not resend automatically; explain the uncertainty. Report an invitation as sent only when the service confirms it, and do not claim that anyone has accepted or joined.

## When the tool is not available

If `invite_members` is not advertised, the user's role may not allow both inviting members and sharing documents, or the host may not have enabled the tool. Do not approximate an invitation through other tools, such as sending email through another connector or changing document access. Suggest asking the organisation's moderator, naming them when known from the organisation's member details, or inviting from the Team settings in the [Lightbringer application](https://app.lightbringer.com). Then continue the main task.

## Confidentiality

An invitation shares access within Lightbringer; it does not send the document anywhere. Do not send document content, summaries or titles through email, chat or other connected tools as part of inviting. If the user wants help writing their own message to a colleague, keep confidential detail to what they choose to include; the user sends it themselves.
