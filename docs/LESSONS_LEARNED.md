# RemixBuddy – Lessons Learned

## 1. Architecture before ML scale-up
Do not open stem separation until plugin ↔ service architecture is really proven locally.

## 2. Local validation matters
A “source-code complete” milestone is not enough.
The slice must be:
- built
- loaded in FL Studio
- tested with real files

## 3. Service restart matters
When backend code changes, restart the service.
Otherwise old logic continues to run and creates false debugging conclusions.

## 4. Background service visibility matters
If the service is already running on the expected port, a new instance will fail to bind.
This is not a new failure; it is proof that another instance already owns the port.

## 5. Dependency issues can masquerade as architecture failures
Missing Python dependencies (e.g. the `pkg_resources` problem) looked like analysis failure, but the architecture was fine.

## 6. BPM trust > BPM cosmetics
A wrong but “musically cleaned” BPM value is worse than an honest measured float.
Producer trust is lost immediately when the tool confidently reports the wrong tempo.

## 7. One good result does not validate the method
A BPM method that matches one track can still fail on another.
Real validation needs a small reference set with measured deltas.

## 8. FL Studio / Edison is a valid producer-side reference
Not an academic ground truth, but good enough to catch obvious product-level BPM misses.
