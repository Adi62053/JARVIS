import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from security.v9_protection_manager import ProtectionLevel
from security.v9_service_manager import V9ServiceManager


manager = V9ServiceManager()

services = manager.list_services()

print("service_count:", len(services))

if not services:
    raise RuntimeError(
        "No Windows services were returned"
    )

print(
    "service_list_available:",
    len(services) > 0,
)

protected = [
    service
    for service in services
    if service.protection_level == ProtectionLevel.PROTECTED
]

print(
    "protected_service_count:",
    len(protected),
)

event_log = manager.get_service("eventlog")

print(
    "eventlog_found:",
    event_log is not None,
)

if event_log is not None:
    print(
        "eventlog_status:",
        event_log.status,
    )

    print(
        "eventlog_protection:",
        event_log.protection_level.value,
    )

    if (
        event_log.protection_level
        != ProtectionLevel.PROTECTED
    ):
        raise RuntimeError(
            "Event Log service should be protected"
        )

unknown = manager.get_service(
    "V9_Test_Service_Does_Not_Exist"
)

print(
    "unknown_service:",
    unknown,
)

if unknown is not None:
    raise RuntimeError(
        "Unknown service unexpectedly returned"
    )

print("V9.13 service inspection test complete")
