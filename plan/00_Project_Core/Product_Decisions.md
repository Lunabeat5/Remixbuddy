# Product_Decisions.md

Decision: Dev environment baseline
Date: 2026-03-14
Scope: RemixBuddy v1

- Platform: Windows 10/11 x64
- Compiler: MSVC 2022
- Build: CMake
- Plugin framework: JUCE 8 via Git submodule
- Backend: Python 3.11 via project-local .venv
- Model storage (dev): <ProjectRoot>\runtime\models\
- GPU: optional
- CPU fallback: required
- Installer: out of scope for MVP