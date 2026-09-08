"""
JARVIS V4 - Additional Filesystem Operations

Contains:
- Rename file
- Rename folder
- Delete file
- Delete folder
- Copy file
- Copy folder
- Move file
- Move folder
"""

import os
import shutil
from pathlib import Path


class FileSystem2:
    """
    Additional filesystem operations for JARVIS V4.
    """

    # ==========================================================
    # PATH RESOLUTION
    # ==========================================================

    def resolve_path(self, value):
        """
        Resolve a user-provided path.

        Relative paths are searched in:
        - Current directory
        - Desktop
        - Documents
        - Downloads
        """

        value = str(value).strip().strip('"').strip("'")

        if not value:
            return None

        path = Path(value).expanduser()

        # Absolute path
        if path.is_absolute():
            return path

        # Direct relative path
        if path.exists():
            return path.resolve()

        home = Path.home()

        locations = [
            home / "Desktop",
            home / "Documents",
            home / "Downloads",
        ]

        # Search exact name
        for location in locations:

            candidate = location / value

            if candidate.exists():
                return candidate.resolve()

        # Return Desktop path for operations
        # where the item may not exist yet.
        return (home / "Desktop" / value).resolve()

    # ==========================================================
    # RENAME
    # ==========================================================

    def rename(self, source, new_name):
        """
        Rename a file or folder.
        """

        source_path = Path(source).expanduser()

        if not source_path.exists():
            return f"Sir, I could not find '{source}'."

        new_name = str(new_name).strip()

        if not new_name:
            return "Sir, the new name cannot be empty."

        if new_name in (".", ".."):
            return "Sir, that is not a valid name."

        invalid_chars = '<>:"/\\|?*'

        if any(char in new_name for char in invalid_chars):
            return f"Sir, '{new_name}' contains invalid characters."

        if new_name.endswith(" ") or new_name.endswith("."):
            return (
                "Sir, a Windows file or folder name cannot "
                "end with a space or period."
            )

        destination = source_path.parent / new_name

        if destination.exists():
            return f"Sir, '{new_name}' already exists."

        try:
            item_type = (
                "folder"
                if source_path.is_dir()
                else "file"
            )

            old_name = source_path.name

            source_path.rename(destination)

            return (
                f"Sir, I renamed the {item_type} "
                f"'{old_name}' to '{new_name}'."
                f"|||VOICE|||"
                f"Sir, I renamed the {item_type} to {new_name}."
            )

        except PermissionError:
            return "Sir, I don't have permission to rename that."

        except OSError as error:
            return f"Sir, I could not rename it. {error}"

    # ==========================================================
    # DELETE
    # ==========================================================

    def delete(self, target):
        """
        Delete a file or folder.
        """

        target_path = Path(target).expanduser()

        if not target_path.exists():
            return f"Sir, I could not find '{target}'."

        try:

            if target_path.is_dir():

                name = target_path.name

                shutil.rmtree(target_path)

                return (
                    f"Sir, I deleted the folder '{name}'."
                    f"|||VOICE|||"
                    f"Sir, I deleted the folder {name}."
                )

            name = target_path.name

            target_path.unlink()

            return (
                f"Sir, I deleted the file '{name}'."
                f"|||VOICE|||"
                f"Sir, I deleted the file {name}."
            )

        except PermissionError:
            return "Sir, I don't have permission to delete that."

        except OSError as error:
            return f"Sir, I could not delete it. {error}"

    # ==========================================================
    # COPY
    # ==========================================================

    def copy(self, source, destination):
        """
        Copy a file or folder to a destination.
        """

        source_path = Path(source).expanduser()
        destination_path = Path(destination).expanduser()

        if not source_path.exists():
            return f"Sir, I could not find '{source}'."

        try:

            if source_path.is_dir():

                # Destination is an existing folder
                if destination_path.exists():

                    if not destination_path.is_dir():
                        return (
                            f"Sir, the destination "
                            f"'{destination}' is not a folder."
                        )

                    final_destination = (
                        destination_path / source_path.name
                    )

                    if final_destination.exists():
                        return (
                            f"Sir, '{final_destination.name}' "
                            f"already exists there."
                        )

                else:
                    final_destination = destination_path

                shutil.copytree(
                    source_path,
                    final_destination
                )

                return (
                    f"Sir, I copied the folder "
                    f"'{source_path.name}'."
                    f"|||VOICE|||"
                    f"Sir, I copied the folder "
                    f"{source_path.name}."
                )

            # ==================================================
            # FILE COPY
            # ==================================================

            if destination_path.exists() and destination_path.is_dir():

                final_destination = (
                    destination_path / source_path.name
                )

            else:

                final_destination = destination_path

            if final_destination.exists():
                return (
                    f"Sir, '{final_destination.name}' "
                    f"already exists."
                )

            shutil.copy2(
                source_path,
                final_destination
            )

            return (
                f"Sir, I copied the file "
                f"'{source_path.name}'."
                f"|||VOICE|||"
                f"Sir, I copied the file "
                f"{source_path.name}."
            )

        except PermissionError:
            return "Sir, I don't have permission to copy that."

        except OSError as error:
            return f"Sir, I could not copy it. {error}"

    # ==========================================================
    # MOVE
    # ==========================================================

    def move(self, source, destination):
        """
        Move a file or folder to a destination.
        """

        source_path = Path(source).expanduser()
        destination_path = Path(destination).expanduser()

        if not source_path.exists():
            return f"Sir, I could not find '{source}'."

        try:

            if (
                destination_path.exists()
                and destination_path.is_dir()
            ):

                final_destination = (
                    destination_path / source_path.name
                )

            else:

                final_destination = destination_path

            if final_destination.exists():
                return (
                    f"Sir, '{final_destination.name}' "
                    f"already exists at the destination."
                )

            item_type = (
                "folder"
                if source_path.is_dir()
                else "file"
            )

            name = source_path.name

            shutil.move(
                str(source_path),
                str(final_destination)
            )

            return (
                f"Sir, I moved the {item_type} "
                f"'{name}'."
                f"|||VOICE|||"
                f"Sir, I moved the {item_type} {name}."
            )

        except PermissionError:
            return "Sir, I don't have permission to move that."

        except OSError as error:
            return f"Sir, I could not move it. {error}"

    # ==========================================================
    # COMMAND PARSER
    # ==========================================================

    def execute(self, command):
        """
        Execute a V4 filesystem2 command.

        Supported commands:

        rename file X to Y
        rename folder X to Y

        delete file X
        delete folder X

        copy file X to Y
        copy folder X to Y

        move file X to Y
        move folder X to Y
        """

        command = str(command).lower().strip()

        # ======================================================
        # RENAME
        # ======================================================

        rename_match = re_match(
            command,
            r"^rename\s+(file|folder)\s+(.+?)\s+to\s+(.+)$"
        )

        if rename_match:

            item_type = rename_match.group(1)
            source_name = rename_match.group(2).strip()
            new_name = rename_match.group(3).strip()

            source_path = self.resolve_path(source_name)

            if not source_path.exists():
                return f"Sir, I could not find the {item_type} '{source_name}'."

            if item_type == "file" and not source_path.is_file():
                return f"Sir, '{source_name}' is not a file."

            if item_type == "folder" and not source_path.is_dir():
                return f"Sir, '{source_name}' is not a folder."

            return self.rename(
                source_path,
                new_name
            )

        # ======================================================
        # DELETE
        # ======================================================

        delete_match = re_match(
            command,
            r"^(delete|remove)\s+(file|folder)\s+(.+)$"
        )

        if delete_match:

            item_type = delete_match.group(2)
            target_name = delete_match.group(3).strip()

            target_path = self.resolve_path(target_name)

            if not target_path.exists():
                return (
                    f"Sir, I could not find the "
                    f"{item_type} '{target_name}'."
                )

            if item_type == "file" and not target_path.is_file():
                return f"Sir, '{target_name}' is not a file."

            if item_type == "folder" and not target_path.is_dir():
                return f"Sir, '{target_name}' is not a folder."

            return self.delete(target_path)

        # ======================================================
        # COPY
        # ======================================================

        copy_match = re_match(
            command,
            r"^copy\s+(file|folder)\s+(.+?)\s+to\s+(.+)$"
        )

        if copy_match:

            item_type = copy_match.group(1)
            source_name = copy_match.group(2).strip()
            destination_name = copy_match.group(3).strip()

            source_path = self.resolve_path(source_name)

            if not source_path.exists():
                return (
                    f"Sir, I could not find the "
                    f"{item_type} '{source_name}'."
                )

            if item_type == "file" and not source_path.is_file():
                return f"Sir, '{source_name}' is not a file."

            if item_type == "folder" and not source_path.is_dir():
                return f"Sir, '{source_name}' is not a folder."

            destination_path = self.resolve_path(
                destination_name
            )

            return self.copy(
                source_path,
                destination_path
            )

        # ======================================================
        # MOVE
        # ======================================================

        move_match = re_match(
            command,
            r"^move\s+(file|folder)\s+(.+?)\s+to\s+(.+)$"
        )

        if move_match:

            item_type = move_match.group(1)
            source_name = move_match.group(2).strip()
            destination_name = move_match.group(3).strip()

            source_path = self.resolve_path(source_name)

            if not source_path.exists():
                return (
                    f"Sir, I could not find the "
                    f"{item_type} '{source_name}'."
                )

            if item_type == "file" and not source_path.is_file():
                return f"Sir, '{source_name}' is not a file."

            if item_type == "folder" and not source_path.is_dir():
                return f"Sir, '{source_name}' is not a folder."

            destination_path = self.resolve_path(
                destination_name
            )

            return self.move(
                source_path,
                destination_path
            )

        # ======================================================
        # UNKNOWN
        # ======================================================

        return (
            "Sir, I couldn't understand that filesystem "
            "operation."
        )


# ==============================================================
# REGEX HELPER
# ==============================================================

def re_match(command, pattern):
    """
    Small wrapper around re.match.
    """

    import re

    return re.match(
        pattern,
        command,
        re.IGNORECASE
    )