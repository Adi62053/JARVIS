# JARVIS PROJECT STATE

## Current Version

**V5 — WEB INTELLIGENCE**

## Current Status

**V5 COMPLETED**

JARVIS is now a voice-controlled Windows laptop assistant with:

* Voice conversation
* Wake-word activation
* Controlled Windows operations
* File and folder management
* Web search and web intelligence
* Current-information questions
* Webpage retrieval and text extraction
* Search-result fallback when webpages block direct access
* Modular command routing
* Security-aware command handling
* Local offline Kokoro TTS voice

V5 preserves all working V1, V2, V3 and V4 capabilities and adds controlled web-information capabilities.

---

# PROJECT ROADMAP

| Version | Name                 | Primary Outcome                                                                            |
| ------- | -------------------- | ------------------------------------------------------------------------------------------ |
| Phase 0 | Foundation           | Project setup, environment, architecture, configuration, logging and development workflow. |
| V1      | Basic JARVIS         | Voice → AI → Voice conversation.                                                           |
| V2      | Wake Word            | Hands-free activation and conversation sessions.                                           |
| V3      | Laptop Control       | Controlled application and Windows operations.                                             |
| V4      | Files & Folders      | Search, create, inspect, rename, copy, move and delete files/folders.                      |
| **V5**  | **Web Intelligence** | **Search, retrieve and use online information safely.**                                    |
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

# V5 — WEB INTELLIGENCE

## V5 Status

**✓ COMPLETE**

V5 adds controlled online information capabilities without replacing the existing V1–V4 architecture.

New modular files:

```text
tools/web_intelligence.py
tools/router_web.py
```

Existing V1–V4 modules remain in place.

---

## V5 Web Intelligence Module

### `tools/web_intelligence.py`

Responsible for:

✓ Web search

✓ Search-result collection

✓ Search-result formatting

✓ Webpage retrieval

✓ HTTP response handling

✓ Gzip response decompression

✓ Deflate response decompression

✓ Character encoding handling

✓ HTML cleanup

✓ Main-content extraction

✓ Trafilatura-based text extraction

✓ Fallback HTML text extraction

✓ Readable webpage text generation

✓ Webpage error handling

✓ Search-result text fallback support

The module remains below the project's 1000-line module limit.

---

## V5 Web Router

### `tools/router_web.py`

Responsible for:

✓ Web command detection

✓ Explicit web-search commands

✓ Current/latest information questions

✓ Search-result tracking

✓ Result-number recognition

✓ Direct webpage reading

✓ Search-result snippet fallback

✓ Local Ollama analysis

✓ Source-grounded current-information responses

✓ Web-related error handling

✓ Voice-friendly responses

✓ Modular connection to `main.py`

The module remains below the project's 1000-line module limit.

---

## V5 Explicit Web Search

Commands such as:

```text
search for latest cricket news
search for Python programming
search online for technology news
google latest cricket news
web search Python
```

are handled as explicit searches.

Behavior:

```text
Voice Command
      ↓
Web Router
      ↓
Web Search
      ↓
5 Search Results
      ↓
Results displayed in terminal
      ↓
Short Kokoro confirmation
```

✓ Search tested successfully

✓ Five-result output tested

✓ Search-result titles displayed

✓ Search-result URLs displayed

✓ Search confirmation spoken through Kokoro

---

## V5 Current Information Questions

Natural-language questions such as:

```text
What is the latest news about Python?
What is the latest news about cricket?
```

are handled as current-information requests.

Behavior:

```text
Voice Question
      ↓
Web Router
      ↓
Internal Web Search
      ↓
Retrieved Sources
      ↓
Local Ollama Analysis
      ↓
Source-grounded Answer
      ↓
Kokoro Voice
```

✓ Current Python information query tested

✓ Current cricket information query tested

✓ Internal web search tested

✓ Local Ollama analysis tested

✓ Direct answer mode tested

✓ JARVIS does not require the user to select a webpage

✓ Search results remain available internally for analysis

✓ Current-answer prompt requires source-grounded responses

✓ Prompt instructs Ollama not to invent current facts

✓ Prompt instructs Ollama not to rely on its own memory for current information

✓ Prompt instructs Ollama to acknowledge insufficient information

✓ Prompt instructs Ollama to handle conflicting sources carefully

✓ Prompt instructs Ollama to prefer official sources

---

## V5 Webpage Reader

Commands such as:

```text
read the first web page
read the second web page
read the third web page
```

are supported.

Behavior:

```text
Search
  ↓
Stored Results
  ↓
Result Number
  ↓
Webpage Fetch
  ↓
Content Extraction
  ↓
Kokoro Voice
```

✓ Result 1 selection tested

✓ Result 2 selection tested

✓ Direct webpage retrieval tested

✓ Successful webpage extraction tested

✓ Long webpage text capped for voice output

✓ Search-result persistence during session tested

---

## V5 Search-Result Fallback

Some websites block automated webpage access.

Example:

```text
HTTP 403 Forbidden
```

V5 handles this without crashing.

Behavior:

```text
Webpage Fetch
      ↓
Access Blocked
      ↓
Search Result Fallback
      ↓
Use Available Search Snippet
      ↓
Kokoro Voice
```

✓ Cricinfo 403 tested

✓ 403 handled safely

✓ Search-result snippet fallback tested

✓ JARVIS continued operating after webpage access failure

✓ Fallback information was successfully spoken

This ensures that a blocked webpage does not terminate the JARVIS conversation.

---

## V5 Error Handling

✓ HTTP 403 handling

✓ URL retrieval errors handled

✓ Webpage extraction failure handled

✓ Search-result fallback

✓ Empty search-result handling

✓ Web search failures handled

✓ Ollama failure fallback implemented

✓ Unknown speech does not crash JARVIS

✓ Conversation continues after recoverable web errors

---

## V5 Voice Integration

✓ Wake word → voice command → web router → web tool → response → Kokoro

✓ Explicit web search through voice

✓ Current-information question through voice

✓ Webpage reading through voice

✓ Search-result selection through voice

✓ Search-result fallback through voice

✓ Kokoro `am_adam` remains active

✓ No paid TTS service introduced

---

## V5 Testing

✓ Web search tested

✓ Latest/current information query tested

✓ Cricket current-information query tested

✓ Python current-information query tested

✓ Explicit cricket web search tested

✓ Webpage result selection tested

✓ Accessible webpage reading tested

✓ 403 webpage access tested

✓ Search-result fallback tested

✓ Voice integration tested

✓ Wake-word integration tested

✓ Kokoro integration tested

✓ Conversation continuation tested

✓ V5 Python syntax validation passed

✓ V5 module syntax validation passed

---

# V5 ARCHITECTURE

```text
                         JARVIS V5
                              │
                              ▼
                    ┌─────────────────┐
                    │    Wake Word    │
                    │   "Hey Jarvis"  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │WakeWordDetector │
                    └────────┬────────┘
                             │
                          DETECTED
                             │
                             ▼
                    ┌─────────────────┐
                    │    Listener     │
                    │  Speech → Text  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Main Runtime  │
                    └────────┬────────┘
                             │
                       Intent / Command
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌───────────────┐        ┌────────────────┐
        │  Web Router   │        │ Command Router │
        │ router_web.py │        │   router.py    │
        └───────┬───────┘        └───────┬────────┘
                │                        │
                ▼                        ▼
       ┌─────────────────┐       Existing V1–V4
       │ Web Intelligence│       Tools
       │web_intelligence │
       └────────┬────────┘
                │
        ┌───────┴─────────┐
        │                 │
        ▼                 ▼
   Web Search        Webpage Reader
        │                 │
        └────────┬────────┘
                 │
                 ▼
          Retrieved Sources
                 │
                 ▼
          Local Ollama AI
          Source Analysis
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
├── __pycache__/
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

Important V5 modules inside `tools/`:

```text
tools/
├── router.py
├── router_web.py
├── web_intelligence.py
├── filesystem_control.py
├── filesystem2.py
├── app_control.py
├── system_control.py
└── window_control.py
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

Web Router / Command Router

        │
        ├── Web Intelligence
        ├── Filesystem2
        ├── Existing V4 Filesystem
        ├── Application Control
        ├── System Control
        ├── Window Control
        └── AI Conversation

    ↓

Security / Tool Handling

    ↓

Windows / Filesystem / Web Tool

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

* Existing V3/V4 command routing
* Application commands
* System commands
* Window commands
* Filesystem commands
* Filesystem2 commands
* Volume command parsing
* Tool command detection
* Connecting commands to existing tools

This is an established large working file and should not be unnecessarily expanded or rewritten.

## `tools/router_web.py`

Responsible for:

* Web command detection
* Current-information queries
* Explicit web searches
* Search-result selection
* Webpage reading
* Webpage fallback
* Local Ollama source analysis
* Web-specific error handling

## `tools/web_intelligence.py`

Responsible for:

* Web searching
* Webpage fetching
* Compression handling
* HTML cleanup
* Main-content extraction
* Search-result formatting
* Webpage reading

## `tools/filesystem_control.py`

Responsible for established V4 functionality:

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

Responsible for V4 filesystem modification operations:

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

## 3. 1000-line module rule

If any single code file approaches or exceeds approximately **1000 lines**, do not continue adding substantial functionality to that file.

Instead:

1. Create a second appropriately named module.
2. Put the new functionality in the new module.
3. Import/connect it to the existing system.
4. Preserve the existing working file.
5. Avoid unnecessary refactoring.

This rule applies to V5 and all future versions.

---

## 4. Version-by-version development

Complete and test the current version before moving to the next major version.

Do not restart completed versions without a debugging reason.

---

## 5. Safety

Laptop/system/file actions must use controlled tool routing.

Never allow unrestricted system commands simply because an AI model generated them.

Destructive filesystem functionality must remain controlled and should receive additional confirmation/security treatment when the security architecture is expanded.

Web intelligence should remain primarily read-oriented and should not automatically execute arbitrary online actions.

---

## 6. Backward compatibility

New versions must preserve working functionality from previous versions unless there is a clear architectural reason to change it.

---

## 7. Test before advancing

Every major feature must be manually tested and, where practical, automated tests should be added.

---

## 8. One feature at a time

Development should proceed incrementally.

For each new feature:

1. Create the appropriate new module when practical.
2. Connect it to the existing router/runtime.
3. Test it.
4. Fix problems.
5. Verify backward compatibility.
6. Only then continue to the next feature.

---

## 9. Preserve working code

Do not reconstruct large working files unnecessarily.

When modifying an established file:

* Preserve existing functionality.
* Make targeted changes.
* Do not remove unrelated code.
* Do not replace a large file with a shortened reconstruction.
* Prefer adding new modules when appropriate.

---

# V5 FINAL POSITION

```text
Phase 0  ████████████████████ COMPLETE

V1       ████████████████████ COMPLETE

V2       ████████████████████ COMPLETE

V3       ████████████████████ COMPLETE

V4       ████████████████████ COMPLETE

V5       ████████████████████ COMPLETE

V6       ░░░░░░░░░░░░░░░░░░░░ NEXT

V7       ░░░░░░░░░░░░░░░░░░░░

V8       ░░░░░░░░░░░░░░░░░░░░

V9       ░░░░░░░░░░░░░░░░░░░░

V10      ░░░░░░░░░░░░░░░░░░░░

V11      ░░░░░░░░░░░░░░░░░░░░

V12      ░░░░░░░░░░░░░░░░░░░░
```

---

# V5 FINAL SUMMARY

V5 — Web Intelligence is complete and functionally tested.

Completed:

✓ Web search

✓ Search result processing

✓ Website retrieval

✓ Web-page information extraction

✓ Current information queries

✓ News/search intelligence

✓ Online information summarization

✓ Controlled web interaction foundation

✓ Search result source handling

✓ Webpage access error handling

✓ 403 fallback handling

✓ Local Ollama source analysis

✓ Source-grounded current answers

✓ Voice command integration

✓ Kokoro offline voice integration

✓ Wake-word integration

✓ V1–V4 backward compatibility

✓ Syntax validation

V5 is now ready for final Git versioning.

---

# CURRENT POSITION

```text
Phase 0  COMPLETE

V1       COMPLETE

V2       COMPLETE

V3       COMPLETE

V4       COMPLETE

V5       COMPLETE

V6       NEXT
```

**Next development session: Begin V6 — Computer Vision.**

Do not restart V1/V2/V3/V4/V5 unless debugging an existing feature.
