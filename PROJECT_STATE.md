# JARVIS PROJECT STATE

## Current Version

**V7 — MEMORY**

## Current Status

**V7 COMPLETE AND FROZEN**

JARVIS is now a voice-controlled Windows laptop assistant with:

* Voice conversation

* Wake-word activation

* Controlled Windows operations

* File and folder management

* Web search and web intelligence

* Current-information questions

* Webpage retrieval and text extraction

* Search-result fallback when webpages block direct access

* Screen capture

* OCR

* Structured screen analysis

* Active-window detection

* Browser control

* Vision command routing

* Persistent local memory

* Memory search and retrieval

* Memory update and deletion

* Session and persistent memory context

* Local Ollama memory-context integration

* Voice-controlled memory operations

* Local offline Kokoro TTS voice

V7 preserves all working V1, V2, V3, V4, V5 and V6 capabilities and adds controlled persistent Memory capabilities.

**V7 final full test suite: 96 PASSED / 0 FAILED / 0 ERRORS.**

**V7.6 real Ollama End-to-End validation: 3 PASSED.**

**V7.12 memory lifecycle End-to-End validation: 1 PASSED.**

**V7 is officially frozen.**

---

# PROJECT ROADMAP

| Version | Name                | Primary Outcome                                                                            |
| ------- | ------------------- | ------------------------------------------------------------------------------------------ |
| Phase 0 | Foundation          | Project setup, environment, architecture, configuration, logging and development workflow. |
| V1      | Basic JARVIS        | Voice → AI → Voice conversation.                                                           |
| V2      | Wake Word           | Hands-free activation and conversation sessions.                                           |
| V3      | Laptop Control      | Controlled application and Windows operations.                                             |
| V4      | Files & Folders     | Search, create, inspect, rename, copy, move and delete files/folders.                      |
| V5      | Web Intelligence    | Search, retrieve and use online information safely.                                        |
| V6      | Computer Vision     | Screen understanding and visual interaction.                                               |
| **V7**  | **Memory**          | **Persistent, user-controlled memory and context.**                                        |
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

# V6 — COMPUTER VISION

## V6 Status

**✓ COMPLETE — FROZEN**

V6 adds the Computer Vision foundation to JARVIS without replacing the existing V1–V5 architecture.

V6 provides:

✓ Screen capture

✓ OCR

✓ Structured screen analysis

✓ Active-window detection

✓ Browser control

✓ Vision command routing

✓ Screen text reading

✓ Visual screen understanding

✓ Browser navigation commands

✓ Voice integration

✓ V6 safety handling

✓ End-to-end validation

---

## V6.1 — Screen Capture

Module:

```text
tools/vision_capture.py
```

Responsible for:

✓ Capturing the current screen

✓ Saving screenshots

✓ Creating timestamped screenshot files

✓ Providing captured image paths to the vision pipeline

Screenshot storage:

```text
data/screenshots/
```

V6.1 testing passed successfully.

---

## V6.2 — OCR

Module:

```text
tools/vision_ocr.py
```

Responsible for:

✓ Loading screenshots

✓ OCR processing

✓ Extracting visible text

✓ Returning OCR text to JARVIS

✓ Handling OCR errors safely

Technology:

✓ pytesseract

✓ PIL/Pillow

✓ Local processing

V6.2 testing passed successfully.

---

## V6.3 — Screen Analyzer

Module:

```text
tools/vision_analyzer.py
```

Responsible for:

✓ Structured OCR

✓ Screen element detection

✓ Element coordinates

✓ Element dimensions

✓ OCR confidence

✓ Raw element collection

✓ Clean element filtering

✓ Full-screen text extraction

✓ Screen resolution detection

Element structure includes:

✓ text

✓ x

✓ y

✓ width

✓ height

✓ confidence

V6.3 testing passed successfully.

---

## V6.4 — Active Window Detection

Module:

```text
tools/window_control_v6.py
```

Responsible for:

✓ Active-window detection

✓ Window title detection

✓ Process identification

✓ Process ID detection

✓ Process path detection

✓ Window class detection

✓ Visibility detection

✓ Maximized/minimized state

✓ Window geometry

Windows native APIs are used for active-window information.

V6.4 testing passed successfully.

---

## V6.5 — Vision Router

Module:

```text
tools/vision_router.py
```

Responsible for:

✓ Connecting screen capture and analysis

✓ Connecting active-window detection

✓ Unified vision results

✓ Current-screen analysis

✓ Storing the latest vision result

Unified result contains:

✓ success

✓ image

✓ screen

✓ active_window

V6.5 testing passed successfully.

---

## V6.6 — Browser Control

Module:

```text
tools/browser_control_v6.py
```

Responsible for:

✓ Browser detection

✓ Default-browser fallback

✓ URL validation

✓ URL normalization

✓ Search URL generation

✓ Opening URLs

✓ Browser navigation

✓ New tab

✓ Close current tab

✓ Refresh

✓ Back

✓ Forward

✓ New browser window

✓ Keyboard control

✓ Browser status

Supported browser targets include:

✓ Chrome

✓ Microsoft Edge

✓ Firefox

✓ System default browser fallback

V6.6 testing passed successfully.

---

## V6.7 — Vision Command Layer

Module:

```text
tools/vision_command_layer.py
```

Responsible for:

✓ Vision command detection

✓ Pure command classification

✓ Screen analysis commands

✓ Active-window commands

✓ OCR commands

✓ Browser commands

✓ Google opening

✓ Web search

✓ New tab

✓ Refresh

✓ Back

✓ Forward

✓ Safe unknown-command rejection

Command classification is separated from command execution.

Example:

```text
"what is on my screen"

        ↓

"analyze_screen"

        ↓

Vision Router

        ↓

Screen analysis
```

This prevents accidental duplicate execution.

The command layer also provides:

✓ `classify()`

✓ `is_vision_command()`

✓ `execute()`

✓ Last-result tracking

V6.7 testing passed successfully.

---

## V6.8 — Main Integration

V6 was integrated into `main.py` while preserving V1–V5 behavior.

Main runtime now supports:

```text
Wake Word

    ↓

Speech Recognition

    ↓

V6 Vision Detection

    ↓

Vision Command Layer

    ↓

Vision Tool

    ↓

Result

    ↓

Kokoro TTS
```

V6 commands are handled before AI fallback when they match a supported vision command.

Existing V1–V5 routing remains preserved.

V6.8 live voice integration was tested successfully.

Tested commands included:

```text
what application is open

what is on my screen

what text is visible

open Google

search Google for python

open a new tab

go back

refresh the page
```

✓ Active application detection

✓ Screen analysis

✓ OCR text reading

✓ Google opening

✓ Browser search

✓ New tab

✓ Back navigation

✓ Refresh

✓ Wake-word integration

✓ Kokoro voice response

✓ Clean shutdown

V6.8 integration passed successfully.

---

## V6.9 — End-to-End Testing

Dedicated test:

```text
tests/test_v6_e2e.py
```

The final V6.9 End-to-End test validates:

✓ V6 module imports

✓ V6.1 screen capture

✓ V6.2 OCR

✓ V6.3 structured screen analyzer

✓ V6.4 active-window detection

✓ V6.5 Vision Router

✓ V6.6 Browser Control

✓ V6.7 command classification

✓ V6.7 command execution

✓ Unknown-command safety

✓ V6.8 main.py integration

Final validation result:

```text
[PASSED] 11

[FAILED] 0

[TEST PASS] JARVIS V6.9 End-to-End testing passed.

[STATUS] V6 is ready for final freeze.
```

**V6.9 is officially passed.**

---

## V6.10 — Final Freeze

**✓ COMPLETE**

V6 Computer Vision is officially frozen.

The following modules are considered stable V6 modules:

```text
tools/vision_capture.py

tools/vision_ocr.py

tools/vision_analyzer.py

tools/window_control_v6.py

tools/vision_router.py

tools/browser_control_v6.py

tools/vision_command_layer.py
```

These modules should not be unnecessarily rewritten during V7 development.

Future versions should integrate with the existing V6 interfaces rather than reconstructing the V6 system.

---

# V6 ARCHITECTURE

```text
                         JARVIS V6

                              │

                              ▼

                    ┌─────────────────┐
                    │    Wake Word    │
                    │  "Hey Jarvis"   │
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
       ┌─────────────────┐       ┌────────────────┐
       │ Vision Command  │       │ Existing V1–V5 │
       │     Layer       │       │    Routing     │
       └────────┬────────┘       └────────────────┘
                │
                ▼
       ┌─────────────────┐
       │  Vision Router  │
       └────────┬────────┘
                │
      ┌─────────┼──────────┐
      │         │          │
      ▼         ▼          ▼
   Screen     Active     Browser
   Capture    Window     Control
      │         │          │
      ▼         ▼          ▼
     OCR   Window Info  Navigation
      │
      ▼
Screen Analyzer
      │
      ▼
Structured Vision Result
      │
      ▼
  JARVIS Result
      │
      ▼
┌─────────────────────┐
│ Kokoro / am_adam   │
└──────────┬──────────┘
           │
           ▼
Continue Conversation
```

---

# V6 FINAL TEST STATUS

```text
V6.1  Screen Capture             ✓ PASS

V6.2  OCR                        ✓ PASS

V6.3  Screen Analyzer            ✓ PASS

V6.4  Active Window              ✓ PASS

V6.5  Vision Router              ✓ PASS

V6.6  Browser Control            ✓ PASS

V6.7  Vision Command Layer       ✓ PASS

V6.8  Main Integration           ✓ PASS

V6.9  End-to-End Testing         ✓ PASS

V6.10 Final Freeze               ✓ COMPLETE
```

**Final V6 End-to-End result:**

```text
11 TESTS PASSED

0 TESTS FAILED
```

---

# V6 IMPORTANT LIMITATIONS

V6 is a Computer Vision foundation and does not yet provide advanced AI vision reasoning.

Current limitations:

✓ OCR accuracy depends on screen resolution, font, contrast and visible UI.

✓ OCR may occasionally produce recognition artifacts.

✓ Browser executable detection may fall back to the system default browser.

✓ Browser keyboard control depends on `pyautogui`.

✓ Vision analysis currently focuses on screen text/elements and active-window information.

✓ V6 does not yet provide advanced object recognition.

✓ V6 does not yet provide face recognition.

✓ V6 does not yet provide continuous visual monitoring.

✓ V6 does not automatically click arbitrary screen coordinates based solely on AI output.

These are future capabilities and should not be considered V6 failures.

---

# V6 SAFETY

V6 preserves the project's safety architecture.

✓ Unknown V6 commands are rejected safely.

✓ Vision classification is separate from execution.

✓ Browser commands are explicitly recognized.

✓ V6 does not expose unrestricted system-command execution.

✓ Existing V3 security architecture remains active.

✓ Existing V4 filesystem safety remains active.

✓ V5 web intelligence remains primarily read-oriented.

✓ Future sensitive visual actions should remain confirmation/security controlled.

---

# V7 — MEMORY

## V7 Status

**✓ COMPLETE — FROZEN**

V7 adds persistent local memory to JARVIS without replacing the existing V1–V6 architecture.

V7 provides:

✓ Local persistent memory

✓ SQLite memory storage

✓ Memory categories

✓ Save memory

✓ Retrieve memory

✓ Search memory

✓ List memory

✓ Count memory

✓ Update memory

✓ Forget/delete memory

✓ Deterministic memory retrieval

✓ Relevance scoring

✓ Meaningful phrase matching

✓ Session memory context

✓ Persistent memory context

✓ Ollama memory-context integration

✓ Natural-language memory commands

✓ Voice-controlled memory operations

✓ Confirmation for destructive memory deletion

✓ Memory lifecycle testing

✓ V6 backward compatibility

✓ Full End-to-End validation

✓ Final V7 freeze

---

## V7.1 — Memory Architecture

V7 memory is implemented as a modular subsystem rather than placing memory logic directly inside `main_v7.py`.

The memory subsystem contains:

```text
memory/

├── memory_commands.py

├── memory_context.py

├── memory_controller.py

├── memory_manager.py

├── memory_ollama.py

├── memory_retrieval.py

├── memory_search.py

├── memory_store.py

└── __init__.py
```

The persistent memory database is stored locally:

```text
memory/data/jarvis_memory.db
```

The memory database is user-specific persistent data and is not committed to Git.

---

## V7.2 — Local Memory Storage

Module:

```text
memory/memory_store.py
```

Responsible for:

✓ SQLite database initialization

✓ Memory table creation

✓ Memory existence checking

✓ Local persistent storage

✓ Memory insertion

✓ Memory retrieval

✓ Memory updating

✓ Memory deletion

✓ Memory counting

✓ Injectable database path for testing

Database schema:

```text
memories

id

category

content

created_at

updated_at
```

Memory remains fully local.

No external memory service is required.

---

## V7.3 — Memory Manager

Module:

```text
memory/memory_manager.py
```

Responsible for:

✓ Memory CRUD operations

✓ Save memory

✓ Get memory

✓ List memories

✓ Update memory

✓ Delete memory

✓ Count memories

✓ Input validation

✓ Store abstraction

The manager keeps higher-level memory operations separate from the SQLite implementation.

---

## V7.4 — Memory Search

Module:

```text
memory/memory_search.py
```

Responsible for:

✓ Memory search

✓ SQLite-backed search

✓ Search result limiting

✓ Keyword matching

✓ Search result ordering

Maximum search result count:

```text
50
```

Search remains deterministic and local.

---

## V7.5 — Memory Retrieval

Module:

```text
memory/memory_retrieval.py
```

Responsible for:

✓ Deterministic memory reranking

✓ Relevance scoring

✓ Exact query matching

✓ Meaningful phrase matching

✓ Meaningful term matching

✓ Category matching

✓ Adjacent-word matching

✓ Result limiting

Important scoring behavior includes:

```text
Exact full query       +10

Meaningful phrase      +8

Meaningful term        +3

Category match         +2
```

The retrieval system includes:

```text
MEANINGFUL_PHRASE_BONUS = 8
```

Maximum retrieval results:

```text
10
```

The retrieval system was specifically validated against natural-language questions such as:

```text
what is my favourite programming language
```

and correctly ranked the relevant memory.

---

## V7.6 — Memory Context

Module:

```text
memory/memory_context.py
```

Responsible for:

✓ Building relevant memory context

✓ Context limiting

✓ Relevance thresholds

✓ Deterministic context generation

Default context limit:

```text
5
```

Maximum context limit:

```text
10
```

Minimum relevance score:

```text
1
```

The context builder does not directly call Ollama.

The context builder does not automatically save memory.

This keeps memory retrieval deterministic and controlled.

---

## V7.7 — Memory Commands

Module:

```text
memory/memory_commands.py
```

Responsible for:

✓ Natural-language memory command parsing

✓ Save commands

✓ Search commands

✓ List commands

✓ Count commands

✓ Delete commands

✓ Update commands

✓ Natural memory questions

✓ Favourite-subject precision

✓ Missing memory number handling

Memory update patterns include:

```text
update memory number <number> to <content>

change memory number <number> to <content>

edit memory number <number> to <content>
```

Memory deletion patterns include:

```text
forget memory number <number>

delete memory number <number>

remove memory number <number>

forget memory <number>

delete memory <number>

remove memory <number>
```

If a memory number is missing, JARVIS responds safely:

```text
Please specify the memory number.
```

---

## V7.8 — Memory Controller

Module:

```text
memory/memory_controller.py
```

Responsible for:

✓ Memory operation orchestration

✓ Memory save operations

✓ Memory retrieval operations

✓ Memory search

✓ Memory context retrieval

✓ Memory count

✓ Memory get operations

✓ Memory deletion

✓ Memory update

✓ Delete confirmation state

✓ Safe memory operations

The controller does not directly call the main runtime, voice system or Ollama.

This keeps the architecture modular.

---

## V7.9 — Ollama Memory Integration

Module:

```text
memory/memory_ollama.py
```

Responsible for:

✓ Local Ollama memory-context integration

✓ Providing relevant memory context to Ollama

✓ Preserving local-only AI architecture

✓ Testing memory context with the actual local Ollama model

Current local model:

```text
llama3.2:3b
```

V7.6 real Ollama End-to-End validation:

```text
3 PASSED
```

---

## V7.10 — Voice Integration

V7 integrates memory operations into the existing JARVIS voice pipeline.

Behavior:

```text
Wake Word

      ↓

Speech Recognition

      ↓

Memory Command Detection

      ↓

Memory Controller

      ↓

Memory Operation

      ↓

JARVIS Response

      ↓

Kokoro / am_adam
```

✓ Memory save through voice

✓ Memory search through voice

✓ Memory retrieval through voice

✓ Memory update through voice

✓ Memory deletion through voice

✓ Memory count through voice

✓ Natural memory questions

✓ Kokoro integration

✓ Wake-word integration

---

## V7.11 — Security / Confirmation

V7 preserves the existing safety architecture.

Memory deletion is confirmation controlled.

Destructive memory operations do not execute without the required confirmation.

The memory subsystem does not expose unrestricted database operations to Ollama.

The AI model does not directly control SQLite.

Memory commands are explicitly parsed and routed.

---

## V7.12 — Full Integration and End-to-End Testing

Dedicated V7 lifecycle testing validates the complete memory lifecycle.

The lifecycle includes:

```text
Save

  ↓

Search

  ↓

Retrieve

  ↓

Update

  ↓

Retrieve Updated Memory

  ↓

Delete

  ↓

Verify Deletion
```

V7.12 lifecycle End-to-End result:

```text
1 PASSED
```

V7 preserves the existing V1–V6 runtime behavior.

---

## V7.13 — Final Validation

V7 validation included:

✓ Memory module testing

✓ Memory store testing

✓ Memory manager testing

✓ Memory search testing

✓ Memory retrieval testing

✓ Memory context testing

✓ Memory command testing

✓ Memory Ollama testing

✓ Real Ollama End-to-End testing

✓ Memory lifecycle End-to-End testing

✓ V6 regression validation

✓ Full project test suite

✓ Tesseract OCR regression validation

Final full test suite:

```text
96 PASSED

0 FAILED

0 ERRORS

13 WARNINGS
```

The warnings were accepted as non-blocking.

The warnings consist primarily of:

✓ Older V6 End-to-End tests returning boolean values instead of assertions

✓ `speech_recognition` dependency deprecation warnings related to `aifc` and `audioop`

No test failures or errors remain.

---

## V7.14 — Final Freeze

**✓ COMPLETE**

V7 Memory is officially frozen.

Git commit:

```text
f127a2f
```

Freeze tag:

```text
v7.14-freeze
```

Commit message:

```text
Freeze JARVIS V7 Memory
```

Tag message:

```text
JARVIS V7.14 Memory Freeze
```

The working tree was verified clean after the freeze.

The V7 memory database remains excluded from Git:

```text
memory/data/
```

Generated screenshots remain excluded from Git:

```text
data/screenshots/
```

The following V7 memory modules are considered stable:

```text
memory/memory_commands.py

memory/memory_context.py

memory/memory_controller.py

memory/memory_manager.py

memory/memory_ollama.py

memory/memory_retrieval.py

memory/memory_search.py

memory/memory_store.py
```

These modules should not be unnecessarily rewritten during V8 development.

Future versions should integrate with the existing V7 interfaces rather than reconstructing the V7 memory system.

---

# V7 ARCHITECTURE

```text
                         JARVIS V7

                              │

                              ▼

                    ┌─────────────────┐
                    │    Wake Word    │
                    │  "Hey Jarvis"   │
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
                    │  Main Runtime   │
                    └────────┬────────┘
                             │
                       Intent / Command
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
   Memory Commands     Existing V1–V6     Normal AI
          │                Routing          Conversation
          ▼                  │                  │
   Memory Controller         │                  │
          │                  │                  │
     ┌────┼────┐             │                  │
     │    │    │             │                  │
     ▼    ▼    ▼             │                  │
   Store Search Context      │                  │
     │    │    │             │                  │
     └────┼────┘             │                  │
          │                  │                  │
          ▼                  ▼                  ▼
   Memory Retrieval    V6 / V5 / V4 / V3    Ollama
          │            Existing Tools          │
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                   Context / JARVIS Result
                             │
                             ▼
                    ┌─────────────────┐
                    │ Kokoro / am_adam│
                    └────────┬────────┘
                             │
                             ▼
                      Continue Conversation
```

---

# V7 FINAL TEST STATUS

```text
V7.1   Memory Architecture           ✓ PASS

V7.2   Local Memory Storage          ✓ PASS

V7.3   Memory Manager                ✓ PASS

V7.4   Memory Search                 ✓ PASS

V7.5   Memory Retrieval              ✓ PASS

V7.6   Memory Context / Ollama       ✓ PASS

V7.7   Memory Commands               ✓ PASS

V7.8   Memory Controller             ✓ PASS

V7.9   Ollama Integration            ✓ PASS

V7.10  Voice Integration             ✓ PASS

V7.11  Security / Confirmation       ✓ PASS

V7.12  End-to-End Testing            ✓ PASS

V7.13  Final Validation              ✓ PASS

V7.14  Final Freeze                  ✓ COMPLETE
```

**Final V7 full test result:**

```text
96 TESTS PASSED

0 TESTS FAILED

0 TEST ERRORS

13 WARNINGS
```

**V7.6 real Ollama E2E result:**

```text
3 TESTS PASSED
```

**V7.12 lifecycle E2E result:**

```text
1 TEST PASSED
```

---

# V7 IMPORTANT LIMITATIONS

V7 is a persistent memory foundation and does not yet provide unrestricted autonomous memory behavior.

Current limitations:

✓ Memory is explicitly stored and controlled.

✓ Memory retrieval is deterministic.

✓ Memory search is local.

✓ Memory is stored in SQLite.

✓ Memory context is limited to relevant results.

✓ Memory does not automatically save every conversation.

✓ Memory does not automatically modify itself from arbitrary AI output.

✓ Destructive memory operations remain confirmation controlled.

✓ Memory does not yet provide advanced semantic vector-database retrieval.

✓ Memory does not yet provide automatic long-term behavioral learning.

✓ Memory does not yet provide advanced user-profile inference.

These are future capabilities and should not be considered V7 failures.

---

# V7 SAFETY

V7 preserves the project's safety architecture.

✓ Memory commands are explicitly classified and routed.

✓ Memory deletion requires controlled confirmation.

✓ Ollama cannot directly execute unrestricted database operations.

✓ Memory operations remain inside dedicated modules.

✓ Existing V3 security architecture remains active.

✓ Existing V4 filesystem safety remains active.

✓ V5 web intelligence remains primarily read-oriented.

✓ V6 vision commands remain explicitly classified and controlled.

✓ Future automation must preserve the existing confirmation/security architecture.

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

├── main_v7.py

├── main_v2_backup.py

├── PROJECT_STATE.md

├── start_jarvis.py

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

# CURRENT TOOLS STRUCTURE

Important V3/V4/V5/V6/V7 modules inside `tools/` and `memory/`:

```text
tools/

├── router.py

├── router_web.py

├── web_intelligence.py

│

├── filesystem_control.py

├── filesystem2.py

│

├── app_control.py

├── system_control.py

├── window_control.py

│

├── vision_capture.py

├── vision_ocr.py

├── vision_analyzer.py

├── window_control_v6.py

├── vision_router.py

├── browser_control_v6.py

└── vision_command_layer.py


memory/

├── memory_commands.py

├── memory_context.py

├── memory_controller.py

├── memory_manager.py

├── memory_ollama.py

├── memory_retrieval.py

├── memory_search.py

├── memory_store.py

└── __init__.py
```

---

# CURRENT TEST STRUCTURE

```text
tests/

├── test_vision_capture.py

├── test_vision_ocr.py

├── test_vision_analyzer.py

├── test_window_control_v6.py

├── test_browser_control_v6.py

├── test_vision_router.py

├── test_vision_command_layer.py

├── test_v6_e2e.py

│

├── test_memory_commands.py

├── test_memory_context.py

├── test_memory_manager.py

├── test_memory_ollama.py

├── test_memory_retrieval.py

├── test_memory_search.py

├── test_memory_store.py

├── test_v7_6_ollama_e2e.py

└── test_v7_12_e2e.py
```

Existing V1–V6 tests remain part of the project where applicable.

---

# IMPORTANT CURRENT FILES

## `main.py`

Responsible for the overall V1–V6 JARVIS runtime:

```text
Wake Word

    ↓

Activation

    ↓

Conversation

    ↓

Command / AI Detection

    ↓

Vision Command Layer / Web Router / Command Router

        │

        ├── V6 Computer Vision

        ├── V5 Web Intelligence

        ├── V4 Filesystem2

        ├── Existing V4 Filesystem

        ├── Application Control

        ├── System Control

        └── Window Control

    ↓

Security / Tool Handling

    ↓

Windows / Filesystem / Web / Vision Tool

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

`main.py` remains the established V1–V6 runtime and should not become a large monolithic file.

New major functionality should be implemented in dedicated modules and connected to the appropriate runtime.

---

## `main_v7.py`

Responsible for the V7 runtime:

```text
Wake Word

    ↓

Activation

    ↓

Conversation

    ↓

Memory / V1–V6 Command Detection

    ↓

Memory Controller / Vision / Web / Filesystem / Laptop Tools

    ↓

Relevant Result

    ↓

Ollama AI when required

    ↓

Kokoro Text-to-Speech

    ↓

Conversation continues

    ↓

goodbye → Wake Word

exit → Shutdown
```

`main_v7.py` preserves V1–V6 behavior while integrating the V7 memory system.

`main_v7.py` is a large established V7 runtime and is officially frozen with V7.

---

## `start_jarvis.py`

Responsible for the permanent JARVIS startup entry point.

Normal daily startup:

```powershell
python start_jarvis.py
```

The launcher starts the currently authoritative JARVIS runtime.

Previous version runtimes and launchers should remain preserved for rollback/testing.

---

## `voice/wakeword.py`

Responsible for:

* Wake-word model

* Microphone stream

* `Hey Jarvis` detection

* Detection threshold

* Cooldown

* Model reset

---

## `voice/listener.py`

Responsible for:

* Microphone input

* Speech recognition

* Speech → text

---

## `voice/speaker.py`

Responsible for:

* Text → speech

* Kokoro local TTS

* `am_adam` JARVIS voice

* Offline voice generation

---

## `core/jarvis.py`

Responsible for:

* Core JARVIS AI interaction

* AI response generation

* Conversational responses

* Ollama integration

Current local model:

```text
llama3.2:3b
```

---

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

---

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

---

## `tools/web_intelligence.py`

Responsible for:

* Web searching

* Webpage fetching

* Compression handling

* HTML cleanup

* Main-content extraction

* Search-result formatting

* Webpage reading

---

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

This file remains the established V4 filesystem foundation.

---

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

---

## `tools/app_control.py`

Responsible for:

* Approved application launching

* Approved application closing

* Windows utility launching

* Safe application termination

* Last-opened application support

---

## `tools/system_control.py`

Responsible for:

* Volume control

* Mute/unmute

* Computer locking

---

## `tools/window_control.py`

Responsible for:

* Minimize

* Maximize

* Restore

* Show desktop

* Window switching

---

## `security/command_security.py`

Responsible for:

* Command security classification

* Safe commands

* Risky commands

* Blocked commands

* Confirmation handling

---

# V6 IMPORTANT FILES

## `tools/vision_capture.py`

Responsible for:

* Screen capture

* Screenshot creation

* Screenshot storage

---

## `tools/vision_ocr.py`

Responsible for:

* OCR

* Screen text extraction

* OCR result handling

---

## `tools/vision_analyzer.py`

Responsible for:

* Structured screen analysis

* OCR element detection

* Coordinates

* Dimensions

* Confidence

* Screen resolution

* Clean OCR elements

---

## `tools/window_control_v6.py`

Responsible for:

* Active window detection

* Window title

* Process name

* Process ID

* Process path

* Window class

* Window state

* Window geometry

---

## `tools/vision_router.py`

Responsible for:

* Vision tool coordination

* Screen capture

* Screen analysis

* Active-window detection

* Unified vision result

---

## `tools/browser_control_v6.py`

Responsible for:

* Browser detection

* URL validation

* URL normalization

* Opening websites

* Google search

* New tab

* Refresh

* Back

* Forward

* Browser keyboard control

* Browser status

---

## `tools/vision_command_layer.py`

Responsible for:

* V6 command classification

* V6 command detection

* Screen commands

* Active-window commands

* OCR commands

* Browser commands

* Search commands

* Browser navigation commands

* Safe unknown-command handling

* Vision command execution

Important architectural rule:

```text
classify()

    ↓

Determine action

    ↓

execute()

    ↓

Perform action once
```

The classifier must remain side-effect free.

---

# V7 IMPORTANT FILES

## `memory/memory_store.py`

Responsible for:

* SQLite persistent memory storage

* Database initialization

* Memory table creation

* Memory insertion

* Memory retrieval

* Memory updating

* Memory deletion

* Memory counting

* Injectable test database path

---

## `memory/memory_manager.py`

Responsible for:

* Memory CRUD operations

* Memory validation

* Memory save

* Memory retrieval

* Memory update

* Memory deletion

* Memory counting

---

## `memory/memory_search.py`

Responsible for:

* Memory search

* SQLite search

* Search result limiting

* Search result handling

---

## `memory/memory_retrieval.py`

Responsible for:

* Deterministic memory reranking

* Relevance scoring

* Exact query matching

* Meaningful phrase matching

* Meaningful term matching

* Category matching

* Adjacent-word matching

* Retrieval result limiting

---

## `memory/memory_context.py`

Responsible for:

* Relevant memory context generation

* Context limiting

* Relevance thresholds

* Deterministic context generation

---

## `memory/memory_commands.py`

Responsible for:

* Natural-language memory command detection

* Save commands

* Search commands

* List commands

* Count commands

* Update commands

* Delete commands

* Natural memory questions

* Missing memory number handling

---

## `memory/memory_controller.py`

Responsible for:

* Memory operation orchestration

* Memory retrieval

* Memory context

* Memory count

* Memory save

* Memory update

* Memory deletion

* Confirmation state

---

## `memory/memory_ollama.py`

Responsible for:

* Local Ollama memory-context integration

* Supplying relevant memory context to Ollama

* Local AI memory reasoning

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

This rule applies to V5, V6, V7 and all future versions.

---

## 4. Version-by-version development

Complete and test the current version before moving to the next major version.

Do not restart completed versions without a debugging reason.

V1–V7 are completed.

The next development phase is V8.

---

## 5. Safety

Laptop/system/file actions must use controlled tool routing.

Never allow unrestricted system commands simply because an AI model generated them.

Destructive filesystem functionality must remain controlled and should receive additional confirmation/security treatment when the security architecture is expanded.

Web intelligence should remain primarily read-oriented and should not automatically execute arbitrary online actions.

Vision commands should remain explicitly classified and controlled.

Memory deletion must remain confirmation controlled.

Memory data must remain locally stored and user controlled.

Future automation must preserve confirmation and security controls.

---

## 6. Backward compatibility

New versions must preserve working functionality from previous versions unless there is a clear architectural reason to change it.

V7 preserves V1–V6 behavior.

V8 must preserve V1–V7 behavior.

---

## 7. Test before advancing

Every major feature must be manually tested and, where practical, automated tests should be added.

V6 passed final End-to-End testing with:

```text
11 PASSED

0 FAILED
```

V7 passed the complete project test suite with:

```text
96 PASSED

0 FAILED

0 ERRORS

13 WARNINGS
```

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

## 10. Frozen-version rule

Once a major version has passed its final End-to-End validation and has been frozen:

* Do not modify stable modules unnecessarily.

* Do not refactor working code without a real requirement.

* New versions should build on the existing interfaces.

* Fix frozen-version code only when a real regression or integration bug is discovered.

V6 is frozen under this rule.

V7 is now also frozen under this rule.

---

# V7 FINAL POSITION

```text
Phase 0  ████████████████████ COMPLETE

V1       ████████████████████ COMPLETE

V2       ████████████████████ COMPLETE

V3       ████████████████████ COMPLETE

V4       ████████████████████ COMPLETE

V5       ████████████████████ COMPLETE

V6       ████████████████████ COMPLETE — FROZEN

V7       ████████████████████ COMPLETE — FROZEN

V8       ░░░░░░░░░░░░░░░░░░░░ NEXT

V9       ░░░░░░░░░░░░░░░░░░░░

V10      ░░░░░░░░░░░░░░░░░░░░

V11      ░░░░░░░░░░░░░░░░░░░░

V12      ░░░░░░░░░░░░░░░░░░░░
```

---

# V7 FINAL SUMMARY

V7 — Memory is complete and frozen.

Completed:

✓ Memory architecture

✓ Local SQLite memory storage

✓ Memory save

✓ Memory retrieval

✓ Memory search

✓ Memory update

✓ Memory deletion

✓ Memory count

✓ Deterministic memory retrieval

✓ Relevance scoring

✓ Meaningful phrase matching

✓ Session memory context

✓ Persistent memory context

✓ Local Ollama memory integration

✓ Voice-controlled memory operations

✓ Memory confirmation handling

✓ V7.6 real Ollama End-to-End testing

✓ V7.12 memory lifecycle End-to-End testing

✓ V7 full test suite

✓ V6 regression validation

✓ Tesseract OCR regression validation

✓ V7.14 final freeze

**Final V7 full test result: 96 PASSED / 0 FAILED / 0 ERRORS.**

**V7.6 Ollama E2E result: 3 PASSED.**

**V7.12 lifecycle E2E result: 1 PASSED.**

V7 is officially complete and frozen.

---

# CURRENT POSITION

```text
Phase 0  COMPLETE

V1       COMPLETE

V2       COMPLETE

V3       COMPLETE

V4       COMPLETE

V5       COMPLETE

V6       COMPLETE — FROZEN

V7       COMPLETE — FROZEN

V8       NEXT
```

**Next development session: Begin V8 — Personal Automation.**

Do not restart V1/V2/V3/V4/V5/V6/V7 unless debugging an existing feature.

V8 should be developed incrementally while preserving the frozen V6 Computer Vision foundation and the frozen V7 Memory foundation.
