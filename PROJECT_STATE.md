# JARVIS PROJECT STATE

## Current Version

**V4 — FILES & FOLDERS**

## Current Status

**V3 COMPLETED**

JARVIS can now operate as a voice-controlled Windows laptop assistant.

V3 preserves all V1 and V2 capabilities and adds controlled laptop operations through a modular command-routing and security architecture.

---

# PROJECT ROADMAP

| Version | Name                | Primary Outcome                                                                            |
| ------- | ------------------- | ------------------------------------------------------------------------------------------ |
| Phase 0 | Foundation          | Project setup, environment, architecture, configuration, logging and development workflow. |
| V1      | Basic JARVIS        | Voice → AI → Voice conversation.                                                           |
| V2      | Wake Word           | Hands-free activation and conversation sessions.                                           |
| **V3**  | **Laptop Control**  | **Controlled application and Windows operations.**                                         |
| **V4**  | **Files & Folders** | **Search, create, move, inspect and safely modify files.**                                 |
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

✓ Sarvam AI integration

✓ Active JARVIS voice using Sarvam TTS

✓ JARVIS voice file/model resources

✓ Core JARVIS architecture

✓ Ollama AI integration

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

## V3 — Laptop Control

### Application Control

✓ Application launching

✓ Approved application list

✓ Notepad control

✓ Calculator control

✓ Chrome control

✓ File Explorer opening

✓ Safe File Explorer close refusal

✓ Application closing

✓ Application termination protection

✓ Last-opened application tracking

✓ Context commands such as `close it`

### Windows Utilities

✓ Windows Settings opening

✓ Windows Settings closing

✓ Task Manager opening

✓ Task Manager closing

✓ Control Panel support

✓ Command Prompt support

✓ PowerShell support

✓ Device Manager support

✓ Unapproved applications are rejected

### System Control

✓ Volume increase

✓ Volume decrease

✓ Exact volume control

✓ Mute

✓ Unmute

✓ Lock computer

✓ Windows system control through dedicated module

### Window Management

✓ Minimize active window

✓ Maximize active window

✓ Restore active window

✓ Show desktop

✓ Minimize all windows

✓ Switch between windows

✓ Basic Windows window management

### Command Routing

✓ Dedicated `CommandRouter`

✓ Application command routing

✓ System command routing

✓ Window command routing

✓ Exact volume command parsing

✓ Natural volume command parsing

✓ Tool command detection

✓ AI fallback for non-tool commands

✓ Modular tool architecture

### Security

✓ Dedicated `CommandSecurity`

✓ Safe command classification

✓ Risky command classification

✓ Blocked command classification

✓ Blocked dangerous commands

✓ Confirmation required for risky operations

✓ Confirmation using voice

✓ `yes` / `confirm` / `proceed` style approval

✓ `no` / `cancel` style rejection

✓ Unclear confirmation safely cancels the action

✓ Risky application closing protection

✓ Risky computer-lock confirmation

### Error Handling

✓ Application errors handled safely

✓ Speech recognition errors handled

✓ Unknown speech handled

✓ Invalid application commands rejected

✓ Unapproved applications rejected

✓ Unsafe File Explorer termination prevented

✓ Confirmation failures safely cancelled

✓ JARVIS conversation continues after recoverable errors

### V3 Testing

✓ Application opening tested

✓ Application closing tested

✓ Settings tested

✓ Task Manager tested

✓ File Explorer safety tested

✓ Volume control tested

✓ Mute/unmute tested

✓ Exact volume tested

✓ Computer locking tested

✓ Window management tested

✓ Security confirmation tested

✓ Security cancellation tested

✓ AI fallback tested

✓ Wake-word integration tested

✓ Conversation loop tested

✓ Shutdown tested

---

# CURRENT ARCHITECTURE

```text
                    JARVIS V3
                       │
                       ▼
              ┌─────────────────┐
              │   Wake Word     │
              │  "Hey Jarvis"   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  WakeWord       │
              │   Detector      │
              └────────┬────────┘
                       │
                   DETECTED
                       │
                       ▼
              ┌─────────────────┐
              │     JARVIS      │
              │   "Yes, sir."   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Listener     │
              │  Speech → Text  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │   Core JARVIS   │
              │   AI Processing │
              └────────┬────────┘
                       │
                 Intent / Command
                       │
                       ▼
              ┌─────────────────┐
              │ Command Router  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Security     │
              │     Check       │
              └────────┬────────┘
                       │
             ┌─────────┼─────────┐
             │         │         │
           SAFE      RISKY    BLOCKED
             │         │         │
             │    Confirmation   │
             │         │         │
             │      Approved     │
             │         │         │
             └─────────┼─────────┘
                       │
                       ▼
              ┌─────────────────┐
              │      Tools      │
              │                 │
              │ App Control     │
              │ System Control  │
              │ Window Control  │
              └────────┬────────┘
                       │
                       ▼
                    Result
                       │
                       ▼
              ┌─────────────────┐
              │     Speaker     │
              │   Text → Speech │
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

Controls the overall JARVIS V3 loop:

```text
Wake Word

    ↓

Activation

    ↓

Conversation

    ↓

Command / AI Detection

    ↓

Command Router
       │
       ├── Tool Command
       │
       └── AI Conversation

    ↓

Security Check

    ↓

Confirmation if Required

    ↓

Windows Tool

    ↓

Result

    ↓

Text-to-Speech

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
* Sarvam AI TTS
* JARVIS voice output

### `core/jarvis.py`

Responsible for:

* Core JARVIS AI interaction
* AI response generation
* Conversational responses

### `tools/router.py`

Responsible for:

* Command routing
* Application commands
* System commands
* Window commands
* Volume command parsing
* Connecting commands to the correct tool

### `tools/app_control.py`

Responsible for:

* Approved application launching
* Approved application closing
* Windows utility launching
* Safe application termination
* Last-opened application support through the router

### `tools/system_control.py`

Responsible for:

* Volume control
* Mute/unmute
* Computer locking

### `tools/window_control.py`

Responsible for:

* Minimize
* Maximize
* Restore
* Show desktop
* Window switching

### `security/command_security.py`

Responsible for:

* Command security classification
* Safe commands
* Risky commands
* Blocked commands

### `tests/`

Responsible for:

* Feature testing
* Future automated tests
* Regression testing

---

# IMPORTANT DESIGN RULES

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

Laptop/system actions must pass through a security/permission layer.

Never allow unrestricted system commands simply because an AI model generated them.

### 5. Backward compatibility

New versions should preserve working functionality from previous versions unless there is a clear architectural reason to change it.

### 6. Test before advancing

Every major feature must be tested manually and, where practical, with automated tests.

---

# NEXT VERSION

## V4 — FILES & FOLDERS

### Goal

Allow JARVIS to safely interact with files and folders on the Windows laptop through natural voice commands.

### Planned V4 capabilities

1. File search

2. Folder search

3. File creation

4. Folder creation

5. File inspection

6. Folder inspection

7. File moving

8. Folder moving

9. File copying

10. Safe file deletion

11. Safe folder deletion

12. File renaming

13. Folder renaming

14. File type detection

15. File path handling

16. Command routing

17. Security checks

18. Confirmation for destructive file operations

19. Error handling

20. Testing

### V4 architecture

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

File / Folder Tool

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

V3       ████████████████████ COMPLETE

V4       ░░░░░░░░░░░░░░░░░░░░ NEXT

V5       ░░░░░░░░░░░░░░░░░░░░

V6       ░░░░░░░░░░░░░░░░░░░░

V7       ░░░░░░░░░░░░░░░░░░░░

V8       ░░░░░░░░░░░░░░░░░░░░

V9       ░░░░░░░░░░░░░░░░░░░░

V10      ░░░░░░░░░░░░░░░░░░░░

V11      ░░░░░░░░░░░░░░░░░░░░

V12      ░░░░░░░░░░░░░░░░░░░░
```

---

**Next session:** Continue from **V4 — Files & Folders**.

Do not restart V1/V2/V3 unless debugging an existing feature.
