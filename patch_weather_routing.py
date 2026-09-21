from pathlib import Path

# ============================================================
# 1. jarvis_unified.py
#    Make V5 weather commands tool-owned.
# ============================================================

path = Path("jarvis_unified.py")
text = path.read_text(encoding="utf-8")

old = '''    # ========================================================
    # V8 AUTOMATION
    # ========================================================

    if is_automation_command(command):

        return True
'''

new = '''    # ========================================================
    # V5 WEATHER
    # ========================================================

    if web_router._is_weather_command(command):

        return True

    # ========================================================
    # V8 AUTOMATION
    # ========================================================

    if is_automation_command(command):

        return True
'''

assert old in text, "jarvis_unified.py target block not found"

assert "if web_router._is_weather_command(command):" not in text, \
    "jarvis_unified.py weather patch already exists"

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")


# ============================================================
# 2. jarvis_unified_runtime.py
#    Route V5 weather to WebRouter.
# ============================================================

path = Path("jarvis_unified_runtime.py")
text = path.read_text(encoding="utf-8")

old = '''                        is_explicit_web = any(
                            command.startswith(prefix)
                            for prefix in explicit_web_prefixes
                        )
'''

new = '''                        is_explicit_web = any(
                            command.startswith(prefix)
                            for prefix in explicit_web_prefixes
                        ) or web_router._is_weather_command(command)
'''

assert old in text, \
    "jarvis_unified_runtime.py target block not found"

assert "or web_router._is_weather_command(command)" not in text, \
    "jarvis_unified_runtime.py weather routing already exists"

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")


# ============================================================
# 3. tools/router_web.py
#    Accept natural "weather of <city>" phrasing.
# ============================================================

path = Path("tools/router_web.py")
text = path.read_text(encoding="utf-8")

old = '''    "weather in ", "weather at ",
    "temperature in ", "temperature at ",
    "forecast in ", "forecast at ",
    "what is the weather in ", "what's the weather in ",
    "what is the weather at ", "what's the weather at ",
    "what is the temperature in ", "what's the temperature in ",
    "what is the temperature at ", "what's the temperature at ",
'''

new = '''    "weather in ", "weather at ", "weather of ",
    "temperature in ", "temperature at ", "temperature of ",
    "forecast in ", "forecast at ", "forecast of ",
    "what is the weather in ", "what's the weather in ",
    "what is the weather at ", "what's the weather at ",
    "what is the weather of ", "what's the weather of ",
    "what is the temperature in ", "what's the temperature in ",
    "what is the temperature at ", "what's the temperature at ",
    "what is the temperature of ", "what's the temperature of ",
'''

assert old in text, \
    "tools/router_web.py weather prefix block not found"

text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")


print("PATCH COMPLETE")
