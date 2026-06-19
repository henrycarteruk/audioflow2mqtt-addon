# 0006 — Device state is held as a plain dict, not a registry module

The orchestrator holds known devices as a `dict[str, Device]` keyed by serial number,
and reads and mutates it inline (membership, iteration, and per-device zone/health
updates). An architecture review proposed extracting a dedicated device-registry
module; we keep the dict.

The only non-trivial behaviour is de-duplication by serial number, which lives in one
place. A dict already provides a small, well-understood interface for the rest
(lookup, iteration, assignment). A registry wrapper around it would be shallow — its
interface would be about as wide as its implementation — and would introduce a seam
that nothing varies across, for no concentration of real complexity.

## Consequences

- Future reviews should not re-suggest extracting a registry while device handling
  remains this simple.
- Revisit when device identity or membership logic grows beyond trivial — for example
  re-keying when a device's IP address changes, eviction of stale devices, or handling
  identity collisions. At that point the logic becomes worth concentrating behind a
  small interface.
