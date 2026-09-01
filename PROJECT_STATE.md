# JARVIS PROJECT STATE

## Current Version

**V2 — WAKE WORD**

## Current Status

**V2 COMPLETED**

JARVIS can now operate in two modes:

1. **Waiting Mode** — listens only for the wake word.
2. **Active Conversation Mode** — continuously listens and responds until the user ends the conversation.

---

# PROJECT ROADMAP

| Version | Name                | Primary Outcome                                                                            |
| ------- | ------------------- | ------------------------------------------------------------------------------------------ |
| Phase 0 | Foundation          | Project setup, environment, architecture, configuration, logging and development workflow. |
| V1      | Basic JARVIS        | Voice → AI → Voice conversation.                                                           |
| **V2**  | **Wake Word**       | Hands-free activation and conversation sessions.                                           |
| V3      | Laptop Control      | Controlled application and Windows operations.                                             |
| V4      | Files & Folders     | Search, create, move, inspect and safely modify files.                                     |
| V5      | Web Intelligence    | Search and use online information/tools.                                                   |
| V6      | Computer Vision     | Optional screen/screenshot understanding and visual interaction.                           |
| V7      | Memory              | Persistent, user-controlled memory and context.                                            |
| V8      | Personal Automation | Reusable multi-action workflows.                                                           |
| V9      | Security System     | Permissions, confirmations, authentication and sensitive-action controls.                  |
| V10     | Background Mode     | Start with Windows and wait for wake word.                                                 |
| V11     | JARVIS GUI          | Dedicated visual interface and system dashboard.                                           |
| V12     | Advanced Agent      | Goal-based planning, tool use, verification and multi-step execution.                      |

---

# COMPLETED

## Phase 0 — Foundation

✓ Python environment
✓ Virtual environment
✓ Project architecture
✓ Configuration structure
✓ Logging structure
✓ Security structure
✓ Testing structure

## V1 — Basic JARVIS

✓ Voice input
✓ Speech recognition
✓ AI conversation
✓ JARVIS response generation
✓ Voice output
✓ Sarvam integration
✓ Piper voice
✓ JARVIS voice file/model
✓ Core JARVIS architecture

## V2 — Wake Word

✓ openWakeWord installed
✓ Wake-word models downloaded
✓ `Hey Jarvis` wake-word model
✓ Dedicated `WakeWordDetector` class
✓ Microphone device configured
✓ Wake-word detection working
✓ Wake-word confidence threshold
✓ Wake-word cooldown
✓ Wake-word model reset
✓ Waiting mode
✓ Active conversation mode
✓ Conversation session handling
✓ `goodbye` ends current conversation
✓ `bye` ends current conversation
✓ `talk to you later` ends current conversation
✓ `exit` completely shuts down JARVIS
✓ Unknown speech does not end the conversation
✓ Speech-recognition errors do not end the conversation
✓ Multiple wake-word sessions tested
✓ Clean Ctrl+C shutdown

---

# CURRENT ARCHITECTURE

```text
                    JARVIS V2

                       │
                       ▼
              ┌─────────────────┐
              │   Wake Word      │
              │  "Hey Jarvis"    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   WakeWord       │
              │    Detector      │
              └────────┬────────┘
                       │
                  DETECTED
                       │
                       ▼
              ┌─────────────────┐
              │   JARVIS        │
              │   "Yes, sir."   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Listener     │
              │ Speech → Text    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Core JARVIS   │
              │  AI Processing  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Speaker      │
              │ Text → Speech   │
              └────────┬────────┘
                       │
                       ▼
                 Continue
                Conversation
                       │
          ┌────────────┴────────────┐
          │                         │
       goodbye                    exit
          │                         │
          ▼                         ▼
   Wake-word mode              Shutdown
```

---

# CURRENT PROJECT STRUCTURE

```text
JARVIS/
│
├── .venv/
│
├── automation/
├── config/
├── core/
├── data/
├── logs/
├── memory/
├── security/
├── tests/
├── tools/
├── ui/
├── voice/
│
├── .env
├── .gitignore
├── main.py
├── main_backup.py
├── requirements.txt
│
├── PROJECT_STATE.md
│
├── en_GB-alan-medium.onnx
├── en_GB-alan-medium.onnx.json
└── jarvis_voice.wav
```

---

# IMPORTANT CURRENT FILES

### `main.py`

Controls the overall JARVIS V2 loop:

```text
Wake Word
    ↓
Activation
    ↓
Conversation
    ↓
AI Response
    ↓
Conversation continues
    ↓
goodbye → Wake Word
exit → Shutdown
```

### `voice/wakeword.py`

Responsible for:

* Wake-word model
* Microphone stream
* `Hey Jarvis` detection
* Detection threshold
* Cooldown
* Model reset

### `voice/listener.py`

Responsible for:

* Microphone input
* Speech recognition
* Speech → text

### `voice/speaker.py`

Responsible for:

* Text → speech
* JARVIS voice output

### `core/jarvis.py`

Responsible for:

* Core JARVIS AI interaction
* AI response generation

---

# IMPORTANT DESIGN RULES

These rules should remain consistent throughout the project:

### 1. Free-first development

Use **free and/or open-source solutions whenever practical**.

Do not introduce paid services when a suitable free/local alternative exists.

### 2. Modular architecture

Do not put everything into `main.py`.

New capabilities should be implemented in the appropriate module/folder.

### 3. Version-by-version development

Do not jump ahead unnecessarily.

Complete and test the current version before moving to the next major version.

### 4. Safety

Laptop/system actions must eventually pass through a security/permission layer.

Never allow unrestricted system commands simply because an AI model generated them.

### 5. Backward compatibility

New versions should preserve working functionality from previous versions unless there is a clear architectural reason to change it.

### 6. Test before advancing

Every major feature must be tested manually and, where practical, with automated tests.

---

# NEXT VERSION

## V3 — LAPTOP CONTROL

### Goal

Allow JARVIS to safely control the Windows laptop through natural voice commands.

### Planned V3 capabilities

1. Application launching
2. Application closing
3. Opening common Windows utilities
4. System controls
5. Volume control
6. Mute/unmute
7. Lock computer
8. Basic window/application management
9. Safe command execution
10. Command routing
11. Security checks
12. Confirmation for risky operations
13. Error handling
14. Testing

### V3 architecture

```text
Voice
  ↓
Speech-to-Text
  ↓
Core JARVIS
  ↓
Intent Detection
  ↓
Command Router
  ↓
Security Check
  ↓
Tool / Windows Action
  ↓
Result
  ↓
JARVIS Response
  ↓
Text-to-Speech
```

---

# CURRENT POSITION

```text
Phase 0  ████████████████████ COMPLETE
V1       ████████████████████ COMPLETE
V2       ████████████████████ COMPLETE

V3       ░░░░░░░░░░░░░░░░░░░░ NEXT
V4       ░░░░░░░░░░░░░░░░░░░░
V5       ░░░░░░░░░░░░░░░░░░░░
V6       ░░░░░░░░░░░░░░░░░░░░
V7       ░░░░░░░░░░░░░░░░░░░░
V8       ░░░░░░░░░░░░░░░░░░░░
V9       ░░░░░░░░░░░░░░░░░░░░
V10      ░░░░░░░░░░░░░░░░░░░░
V11      ░░░░░░░░░░░░░░░░░░░░
V12      ░░░░░░░░░░░░░░░░░░░░
```

**Next session:** Continue from **V3 — Laptop Control**.

Do not restart V1/V2 unless debugging an existing feature.
