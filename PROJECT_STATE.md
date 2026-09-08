# JARVIS PROJECT STATE

## Current Version

**V4 — FILES & FOLDERS**

## Current Status

**V4 COMPLETED**

JARVIS is now a voice-controlled Windows laptop assistant with:

* Voice conversation
* Wake-word activation
* Controlled Windows operations
* File and folder management
* Modular command routing
* Security-aware command handling
* Local offline Kokoro TTS voice

V4 preserves all working V1, V2 and V3 capabilities and adds comprehensive file and folder operations.

---

# PROJECT ROADMAP

| Version | Name                 | Primary Outcome                                                                            |
| ------- | -------------------- | ------------------------------------------------------------------------------------------ |
| Phase 0 | Foundation           | Project setup, environment, architecture, configuration, logging and development workflow. |
| V1      | Basic JARVIS         | Voice → AI → Voice conversation.                                                           |
| V2      | Wake Word            | Hands-free activation and conversation sessions.                                           |
| V3      | Laptop Control       | Controlled application and Windows operations.                                             |
| **V4**  | **Files & Folders**  | **Search, create, inspect, rename, copy, move and delete files/folders.**                  |
| **V5**  | **Web Intelligence** | **Search and use online information/tools.**                                               |
| V6      | Computer Vision      | Optional screen/screenshot understanding and visual interaction.                           |
| V7      | Memory               | Persistent, user-controlled memory and context.                                            |
| V8      | Personal Automation  | Reusable multi-action workflows.                                                           |
| V9      | Security System      | Permissions, confirmations, authentication and sensitive-action controls.                  |
| V10     | Background Mode      | Start with Windows and wait for wake word.                                                 |
| V11     | JARVIS GUI           | Dedicated visual interface and system dashboard.                                           |
| V12     | Advanced Agent       | Goal-based planning, tool use, verification and multi-step execution.                      |

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

---

# V1 — Basic JARVIS

✓ Voice input
✓ Speech recognition
✓ AI conversation
✓ JARVIS response generation
✓ Voice output
✓ Ollama AI integration
✓ Core JARVIS architecture
✓ Conversational response handling

### Voice Update

The original development used cloud TTS during experimentation.

**Current permanent JARVIS voice:**

✓ Kokoro local TTS
✓ Offline operation
✓ `am_adam` voice
✓ No API credits required
✓ No cloud dependency for JARVIS voice

Sarvam AI is **not the active core JARVIS voice**.

---

# V2 — Wake Word

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
✓ Speech-recognition errors handled
✓ Multiple wake-word sessions tested
✓ Clean Ctrl+C shutdown

---

# V3 — Laptop Control

## Application Control

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

## Windows Utilities

✓ Windows Settings opening
✓ Windows Settings closing
✓ Task Manager opening
✓ Task Manager closing
✓ Control Panel support
✓ Command Prompt support
✓ PowerShell support
✓ Device Manager support
✓ Unapproved applications rejected

## System Control

✓ Volume increase
✓ Volume decrease
✓ Exact volume control
✓ Mute
✓ Unmute
✓ Lock computer

## Window Management

✓ Minimize active window
✓ Maximize active window
✓ Restore active window
✓ Show desktop
✓ Minimize all windows
✓ Switch between windows
✓ Basic Windows window management

## Command Routing

✓ Dedicated `CommandRouter`
✓ Application command routing
✓ System command routing
✓ Window command routing
✓ Exact volume command parsing
✓ Natural volume command parsing
✓ Tool command detection
✓ AI fallback for non-tool commands
✓ Modular tool architecture

## Security

✓ Dedicated `CommandSecurity`
✓ Safe command classification
✓ Risky command classification
✓ Blocked command classification
✓ Blocked dangerous commands
✓ Confirmation for risky operations
✓ Voice confirmation
✓ `yes` / `confirm` / `proceed` approval
✓ `no` / `cancel` rejection
✓ Unclear confirmation safely cancelled
✓ Risky application closing protection
✓ Risky computer-lock confirmation

## V3 Testing

✓ Application opening
✓ Application closing
✓ Settings
✓ Task Manager
✓ File Explorer safety
✓ Volume control
✓ Mute/unmute
✓ Exact volume
✓ Computer locking
✓ Window management
✓ Security confirmation
✓ Security cancellation
✓ AI fallback
✓ Wake-word integration
✓ Conversation loop
✓ Shutdown

---

# V4 — FILES & FOLDERS

## V4 Status

**✓ COMPLETE**

V4 was implemented without replacing or unnecessarily modifying the existing large filesystem module.

A dedicated module was added for the new filesystem modification operations:

```text
tools/filesystem2.py
```

The existing filesystem functionality remains in:

```text
tools/filesystem_control.py
```

This preserves backward compatibility and keeps the architecture modular.

---

## File Search

✓ Search files
✓ Natural-language file search
✓ File path handling
✓ File reference handling
✓ File type detection/inspection
✓ Read files by search result
✓ Read files by filename/path

## Folder Search

✓ Search folders
✓ Natural-language folder search
✓ Folder path handling
✓ Folder inspection
✓ Open folder
✓ Close folder

## File Creation

✓ Create file
✓ Create file on Desktop
✓ Create file in supported locations
✓ File-name validation
✓ Invalid Windows filename protection
✓ Existing-file overwrite protection

## Folder Creation

✓ Create folder
✓ Create folder on Desktop
✓ Folder path handling

## File Inspection / Reading

✓ Read text files
✓ Read PDF files
✓ Read DOCX files
✓ Inspect files
✓ Open files
✓ Close files

## Folder Operations

✓ Rename folder
✓ Delete folder
✓ Copy folder
✓ Move folder

## File Operations

✓ Rename file
✓ Delete file
✓ Copy file
✓ Move file

## V4 Command Routing

✓ Dedicated `FileSystem2` module
✓ Router integration
✓ Rename command detection
✓ Delete command detection
✓ Copy command detection
✓ Move command detection
✓ File command routing
✓ Folder command routing
✓ Existing V4 filesystem commands preserved

## V4 Voice Integration

✓ Commands tested through `main.py`
✓ Wake word → speech → router → filesystem tool → response → Kokoro voice
✓ Rename folder through voice
✓ Delete folder through voice
✓ Copy folder through voice
✓ Move folder through voice
✓ Rename file through voice
✓ Delete file through voice
✓ Move file through voice
✓ Create file through voice
✓ Create folder through voice

## V4 Error Handling

✓ Non-existent file/folder handled
✓ Invalid move operation handled
✓ Attempt to move folder into itself safely rejected
✓ Unknown speech does not crash JARVIS
✓ Filesystem errors returned as JARVIS responses
✓ Conversation continues after recoverable filesystem errors

## V4 Testing

✓ File search tested
✓ Folder search tested
✓ Natural file search tested
✓ File reading tested
✓ PDF reading tested
✓ File opening tested
✓ Folder opening tested
✓ File closing tested
✓ Folder closing tested
✓ File creation tested
✓ Folder creation tested
✓ Folder rename tested
✓ Folder delete tested
✓ Folder copy tested
✓ Folder move tested
✓ File rename tested
✓ File delete tested
✓ File move tested
✓ Voice pipeline tested
✓ Multiple wake-word sessions tested
✓ Temporary V4 test items cleaned up

---

# V4 ARCHITECTURE

```text
                         JARVIS V4
                             │
                             ▼
                    ┌─────────────────┐
                    │    Wake Word    │
                    │   "Hey Jarvis"  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ WakeWordDetector│
                    └────────┬────────┘
                             │
                          DETECTED
                             │
                             ▼
                    ┌─────────────────┐
                    │     Listener    │
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
                    ┌────────┴─────────┐
                    │                  │
              Filesystem2       Existing Tools
                    │                  │
                    ▼                  ▼
             File/Folder Tool    App/System/Window
                    │                  │
                    └────────┬─────────┘
                             │
                             ▼
                         Result
                             │
                             ▼
                    ┌─────────────────┐
                    │     Speaker     │
                    │ Kokoro / am_adam│
                    └────────┬────────┘
                             │
                             ▼
                    Continue Conversation
```

---

# CURRENT PROJECT STRUCTURE

```text
JARVIS/
│
├── .venv/
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
├── kokoro_test/
│
├── .env
├── .gitignore
├── main.py
├── main_v2_backup.py
├── PROJECT_STATE.md
├── requirements.txt
│
├── kokoro-v1.0.onnx
├── voices-v1.0.bin
│
├── en_GB-alan-medium.onnx
├── en_GB-alan-medium.onnx.json
├── jarvis_voice.wav
│
├── wakeword_class_test.py
└── wakeword_test.py
```

---

# IMPORTANT CURRENT FILES

## `main.py`

Responsible for the overall JARVIS runtime:

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
       ├── Filesystem2
       ├── Existing V4 Filesystem
       ├── Application Control
       ├── System Control
       ├── Window Control
       └── AI Conversation
    ↓
Security / Tool Handling
    ↓
Windows / Filesystem Tool
    ↓
Result
    ↓
Kokoro Text-to-Speech
    ↓
Conversation continues
    ↓
goodbye → Wake Word
exit → Shutdown
```

## `voice/wakeword.py`

Responsible for:

* Wake-word model
* Microphone stream
* `Hey Jarvis` detection
* Detection threshold
* Cooldown
* Model reset

## `voice/listener.py`

Responsible for:

* Microphone input
* Speech recognition
* Speech → text

## `voice/speaker.py`

Responsible for:

* Text → speech
* Kokoro local TTS
* `am_adam` JARVIS voice
* Offline voice generation

## `core/jarvis.py`

Responsible for:

* Core JARVIS AI interaction
* AI response generation
* Conversational responses

## `tools/router.py`

Responsible for:

* Command routing
* Application commands
* System commands
* Window commands
* Filesystem commands
* Filesystem2 commands
* Volume command parsing
* Tool command detection
* Connecting commands to the correct tool

## `tools/filesystem_control.py`

Responsible for existing V4 functionality:

* File search
* Folder search
* Natural search
* File inspection
* File reading
* PDF reading
* DOCX reading
* File opening/closing
* Folder opening/closing
* File creation
* Folder creation

This file remains unchanged as the established V4 filesystem foundation.

## `tools/filesystem2.py`

Responsible for the new V4 filesystem modification operations:

* Rename file
* Rename folder
* Delete file
* Delete folder
* Copy file
* Copy folder
* Move file
* Move folder

## `tools/app_control.py`

Responsible for:

* Approved application launching
* Approved application closing
* Windows utility launching
* Safe application termination
* Last-opened application support

## `tools/system_control.py`

Responsible for:

* Volume control
* Mute/unmute
* Computer locking

## `tools/window_control.py`

Responsible for:

* Minimize
* Maximize
* Restore
* Show desktop
* Window switching

## `security/command_security.py`

Responsible for:

* Command security classification
* Safe commands
* Risky commands
* Blocked commands
* Confirmation handling

---

# IMPORTANT DESIGN RULES

## 1. Free-first development

Use **free and/or open-source solutions whenever practical**.

Avoid paid services when a suitable free/local alternative exists.

The permanent JARVIS TTS should remain:

**Kokoro local offline TTS — `am_adam`**

---

## 2. Modular architecture

Do not put everything into `main.py`.

New capabilities should be implemented in the appropriate module/folder.

Do not unnecessarily rewrite large existing files.

---

## 3. Version-by-version development

Complete and test the current version before moving to the next major version.

Do not restart completed versions without a debugging reason.

---

## 4. Safety

Laptop/system/file actions must use controlled tool routing.

Never allow unrestricted system commands simply because an AI model generated them.

Destructive filesystem functionality must remain controlled and should receive additional confirmation/security treatment when the security architecture is expanded.

---

## 5. Backward compatibility

New versions must preserve working functionality from previous versions unless there is a clear architectural reason to change it.

---

## 6. Test before advancing

Every major feature must be manually tested and, where practical, automated tests should be added.

---

## 7. One feature at a time

Development should proceed incrementally.

For each new feature:

1. Create the appropriate new module when practical.
2. Connect it to the existing router/runtime.
3. Test it.
4. Fix problems.
5. Verify backward compatibility.
6. Only then continue to the next feature.

---

# V4 FINAL POSITION

```text
Phase 0  ████████████████████ COMPLETE

V1       ████████████████████ COMPLETE

V2       ████████████████████ COMPLETE

V3       ████████████████████ COMPLETE

V4       ████████████████████ COMPLETE

V5       ░░░░░░░░░░░░░░░░░░░░ NEXT

V6       ░░░░░░░░░░░░░░░░░░░░

V7       ░░░░░░░░░░░░░░░░░░░░

V8       ░░░░░░░░░░░░░░░░░░░░

V9       ░░░░░░░░░░░░░░░░░░░░

V10      ░░░░░░░░░░░░░░░░░░░░

V11      ░░░░░░░░░░░░░░░░░░░░

V12      ░░░░░░░░░░░░░░░░░░░░
```

---

# NEXT VERSION

## V5 — WEB INTELLIGENCE

### Goal

Allow JARVIS to safely obtain and use online information and web-based tools while preserving all existing V1–V4 functionality.

### Planned V5 capabilities

1. Web search
2. Search result processing
3. Website retrieval
4. Web-page information extraction
5. Current information queries
6. News/search intelligence
7. Online information summarization
8. Controlled web interaction
9. Search result source handling
10. Error handling
11. Security restrictions
12. Voice command integration
13. Testing

### V5 design requirement

V5 must be added **modularly**.

Do not rewrite the existing V4 filesystem architecture.

Do not replace Kokoro.

Do not break the wake-word system.

Do not remove V1/V2/V3/V4 capabilities.

---

# CURRENT POSITION

```text
Phase 0  COMPLETE
V1       COMPLETE
V2       COMPLETE
V3       COMPLETE
V4       COMPLETE
V5       NEXT
```

**Next development session: Begin V5 — Web Intelligence.**

Do not restart V1/V2/V3/V4 unless debugging an existing feature.
