# 0005 — Inbound handling stays two-stage: parse, then plan

Inbound MQTT messages are handled in two separate modules: `commands.parse_command`
turns a topic and payload into a typed command, and `dispatch.plan_action` turns a
command plus the device's current zones into a typed action. An architecture review
proposed collapsing these into a single inbound-handling module; we keep them separate.

The two stages have genuinely different inputs and meanings. Parsing is stateless — it
depends only on the topic and payload. Planning requires current zone state, to resolve
`toggle` against the present value and to reject unknown or disabled zones. That is a
real pre- and post-state-resolution split, not incidental layering.

The two type families are also distinct vocabularies rather than redundant plumbing.
The command types mirror the MQTT command grammar that the gateway exposes (documented
domain language); the action types mirror operations performed on the device. Keeping
them separate keeps "what the user asked over the wire" distinct from "what we will do
to the device."

## Consequences

- The split is deliberate; future reviews should not re-suggest merging the two modules.
- Each stage keeps its own focused unit tests.
- Revisit only if the command and action vocabularies become a true one-to-one mapping
  with no state-dependent step between them.
