"""
JARVIS Unified Runtime Loop

Extracted from jarvis_unified.py.

Preserves the V7 runtime architecture and adds V8 automation.
"""

from __future__ import annotations


def run_unified_runtime(
    *,
    jarvis,
    listener,
    speaker,
    wakeword,
    router,
    security,
    vision_layer,
    memory_controller,
    automation_manager,
    automation_handler,
    automation_workflow_runner,
    web_router,
    CommandSecurity,
    sr,
    is_tool_command,
    handle_pending_memory_confirmation,
    handle_memory_result,
    handle_vision_result,
    handle_tool_result,
    confirm_risky_command,
    is_automation_command,
    handle_automation_command,
):
    running = True

    while running:

        try:

            wakeword.wait_for_wake_word()

            print(
                "\n>>> HEY JARVIS DETECTED <<<"
            )

            speaker.speak(
                "Yes, sir."
            )

            conversation_active = True

            while conversation_active:

                try:

                    command = (
                        listener.listen()
                        .lower()
                        .strip()
                    )

                    if not command:
                        continue

                    if (
                        memory_controller is not None
                        and memory_controller.has_pending_confirmation()
                    ):

                        if handle_pending_memory_confirmation(
                            command
                        ):
                            continue

                    if command in [
                        "exit",
                        "shut down",
                        "shutdown",
                        "terminate",
                    ]:

                        speaker.speak(
                            "Goodbye, sir."
                        )

                        running = False
                        conversation_active = False

                        continue

                    if command in [
                        "bye",
                        "goodbye",
                        "talk to you later",
                    ]:

                        speaker.speak(
                            "Goodbye, sir."
                        )

                        conversation_active = False

                        continue

                    if is_tool_command(command):

                        if (
                            memory_controller is not None
                            and memory_controller.is_memory_command(
                                command
                            )
                        ):

                            result = (
                                memory_controller.execute(
                                    command
                                )
                            )

                            handle_memory_result(
                                result
                            )

                            continue

                        vision_result = (
                            vision_layer.execute(
                                command
                            )
                        )

                        if (
                            vision_result["action"]
                            != "unknown"
                        ):

                            security_level = (
                                security.check(
                                    command
                                )
                            )

                            if (
                                security_level
                                == CommandSecurity.BLOCKED
                            ):

                                speaker.speak(
                                    "I cannot perform that "
                                    "command because it is "
                                    "blocked for safety, sir."
                                )

                                continue

                            if (
                                security_level
                                == CommandSecurity.RISKY
                            ):

                                if not confirm_risky_command(
                                    command
                                ):
                                    continue

                            handle_vision_result(
                                vision_result
                            )

                            continue

                        if is_automation_command(command):

                            result = (
                                handle_automation_command(
                                    command,
                                    automation_manager,
                                    automation_handler,
                                    automation_workflow_runner,
                                )
                            )

                            handle_tool_result(
                                result
                            )

                            continue

                        security_level = (
                            security.check(
                                command
                            )
                        )

                        if (
                            security_level
                            == CommandSecurity.BLOCKED
                        ):

                            speaker.speak(
                                "I cannot perform that "
                                "command because it is "
                                "blocked for safety, sir."
                            )

                            continue

                        if (
                            security_level
                            == CommandSecurity.RISKY
                        ):

                            if not confirm_risky_command(
                                command
                            ):
                                continue

                        if web_router.is_web_command(
                            command
                        ):

                            result = (
                                web_router.execute(
                                    command
                                )
                            )

                        else:

                            result = (
                                router.route(
                                    command
                                )
                            )

                        if result:
                            handle_tool_result(
                                result
                            )

                        continue

                    response = (
                        jarvis.respond(
                            command
                        )
                    )

                    speaker.speak(
                        response
                    )

                except sr.UnknownValueError:

                    speaker.speak(
                        "Sorry, sir. I didn't "
                        "understand that."
                    )

                    continue

                except sr.RequestError as exc:

                    print(
                        "JARVIS: Speech recognition error:",
                        exc,
                    )

                    speaker.speak(
                        "Sorry, sir. Speech recognition "
                        "is currently unavailable."
                    )

                    continue

                except Exception as exc:

                    print(
                        "JARVIS conversation error:",
                        type(exc).__name__,
                        repr(exc),
                    )

                    speaker.speak(
                        "Sorry, sir. Something went wrong."
                    )

                    continue

            if running:

                print(
                    "\nWaiting for 'Hey Jarvis'..."
                )

        except KeyboardInterrupt:

            print(
                "\n\nShutting down JARVIS."
            )

            try:

                speaker.speak(
                    "Goodbye, sir."
                )

            except Exception:

                pass

            running = False

        except Exception as exc:

            print(
                "JARVIS error:",
                type(exc).__name__,
                repr(exc),
            )

    print(
        "\nJARVIS has been shut down."
    )
