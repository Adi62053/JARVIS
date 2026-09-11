# JARVIS PROJECT STATE

## Current Version

**V6 — COMPUTER VISION**

## Current Status

**V6 COMPLETED AND FROZEN**

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
* Local offline Kokoro TTS voice

V6 preserves all working V1, V2, V3, V4 and V5 capabilities and adds controlled Computer Vision capabilities.

**V6 final End-to-End validation: 11 PASSED / 0 FAILED.**

**V6 is officially frozen.**

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
| **V6**  | **Computer Vision** | **Screen understanding and visual interaction.**                                           |
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
 Screen      Active     Browser
 Capture     Window     Control
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

---

# CURRENT TOOLS STRUCTURE

Important V3/V4/V5/V6 modules inside `tools/`:

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
└── test_v6_e2e.py
```

Existing V1–V5 tests remain part of the project where applicable.

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

`main.py` should not become a large monolithic file.

New major functionality should be implemented in dedicated modules and connected to the runtime.

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

This rule applies to V5, V6 and all future versions.

---

## 4. Version-by-version development

Complete and test the current version before moving to the next major version.

Do not restart completed versions without a debugging reason.

V1–V6 are completed.

The next development phase is V7.

---

## 5. Safety

Laptop/system/file actions must use controlled tool routing.

Never allow unrestricted system commands simply because an AI model generated them.

Destructive filesystem functionality must remain controlled and should receive additional confirmation/security treatment when the security architecture is expanded.

Web intelligence should remain primarily read-oriented and should not automatically execute arbitrary online actions.

Vision commands should remain explicitly classified and controlled.

---

## 6. Backward compatibility

New versions must preserve working functionality from previous versions unless there is a clear architectural reason to change it.

V7 must preserve V1–V6 behavior.

---

## 7. Test before advancing

Every major feature must be manually tested and, where practical, automated tests should be added.

V6 has passed final End-to-End testing with:

```text
11 PASSED
0 FAILED
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

V6 is currently frozen under this rule.

---

# V6 FINAL POSITION

```text
Phase 0  ████████████████████ COMPLETE

V1       ████████████████████ COMPLETE

V2       ████████████████████ COMPLETE

V3       ████████████████████ COMPLETE

V4       ████████████████████ COMPLETE

V5       ████████████████████ COMPLETE

V6       ████████████████████ COMPLETE

V7       ░░░░░░░░░░░░░░░░░░░░ NEXT

V8       ░░░░░░░░░░░░░░░░░░░░

V9       ░░░░░░░░░░░░░░░░░░░░

V10      ░░░░░░░░░░░░░░░░░░░░

V11      ░░░░░░░░░░░░░░░░░░░░

V12      ░░░░░░░░░░░░░░░░░░░░
```

---

# V6 FINAL SUMMARY

V6 — Computer Vision is complete and frozen.

Completed:

✓ Screen capture

✓ Screenshot storage

✓ OCR

✓ Structured screen analysis

✓ Active-window detection

✓ Browser control

✓ Browser navigation

✓ Google opening

✓ Web search through browser control

✓ Screen text reading

✓ Vision command classification

✓ Vision command execution

✓ Pure command classification

✓ V6 main runtime integration

✓ Wake-word integration

✓ Kokoro integration

✓ V1–V5 backward compatibility

✓ V6 safety handling

✓ V6.1–V6.8 feature validation

✓ V6.9 End-to-End testing

✓ V6.10 final freeze

**Final V6 E2E result: 11 PASSED / 0 FAILED.**

V6 is officially complete and frozen.

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

V7       NEXT
```

**Next development session: Begin V7 — Memory.**

Do not restart V1/V2/V3/V4/V5/V6 unless debugging an existing feature.

V7 should be developed incrementally while preserving the frozen V6 Computer Vision foundation.
