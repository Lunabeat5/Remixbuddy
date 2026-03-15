# RemixBuddy – BPM Validation Protocol

## Purpose
Validate BPM on real material before approving the analysis method.

## Reference source
Primary practical reference:
- FL Studio / Edison BPM readout

## Validation classes
### Class A – loops
- short constant loops
- drum loops
- rhythmic consistency high

### Class B – full tracks
- intros
- breaks
- drops
- transitions
- real producer use case

## Current regression track
- `7 Thomas Schumacher - Ficken #3 (Original Mix).mp3`
- Reference: ~`127.002 BPM`
- Current bad result before method upgrade: `126.05 BPM`

## Suggested result table
| File | Type | Reference BPM | RemixBuddy BPM | Delta | Accepted? |
|---|---|---:|---:|---:|---|
| Track A | Full track | 127.002 | 126.05 | -0.952 | No |

## Acceptance guidance
### Loops
- very small deltas expected

### Full tracks
- method must remain close to reference
- obvious >0.5 to 1 BPM drifts on constant electronic tracks are not acceptable for product trust

## Current conclusion
The BPM method is not yet accepted for full tracks.
