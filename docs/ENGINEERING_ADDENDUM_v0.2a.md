# RemixBuddy – Engineering Addendum after Implementation Start

This addendum corrects and supplements the earlier concept/spec documents.

## 1. What is now proven
The following is no longer speculative:
- local loopback HTTP/JSON communication works from plugin to service
- the plugin can live inside FL Studio while heavy analysis runs in the backend
- asynchronous polling and status updates work
- plugin host remains responsive during analysis

## 2. What is not yet proven
The following remains unproven or incomplete:
- producer-grade BPM accuracy on complete tracks
- stem separation runtime and quality
- persistent job storage
- release-grade installer / packaging

## 3. Important implementation corrections
### 3.1 Service lifecycle
The service can already be running in the background on the expected port.
This caused confusion during debugging because a second service instance could not bind to the same address.

### 3.2 Backend restart requirement
If backend logic changes, the service must be restarted.
Without restart, the plugin may appear to “ignore” fixes because it is talking to old code.

### 3.3 venv policy
Do not include `.venv` in shared ZIPs or handover artifacts.
The environment can become very large and is machine-specific.

### 3.4 Integration debugging
UI-only messages like `Service Offline` are not sufficient.
Minimal debug visibility in plugin and service logs is required for slice validation.

## 4. BPM-specific correction
The current BPM problem is not solved by:
- JSON schema tweaks
- UI formatting tweaks
- service restart alone
- switching which BPM field is displayed

The BPM problem is a **method problem**.

## 5. Approved next engineering pass
Segmented tempo estimation:
- windows
- candidate collection
- candidate weighting / filtering
- final value from stable candidate cluster
