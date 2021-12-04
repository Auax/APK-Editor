import logging
import os
import re
from pathlib import Path
from typing import Union

import execute
from format_print import fprint
from re_patterns import RePatterns


class AuaxAPK:
    def __init__(self,
                 apktool_path: Union[str, Path],
                 apksigner_path: Union[str, Path],
                 apk_path: Union[str, Path]):
        # Get the root directory of the file
        self.root = os.path.dirname(os.path.abspath(__file__))

        # Tool paths
        self.apktool_path = apktool_path
        self.apksigner_path = apksigner_path

        # APK Path
        self.apk_path = apk_path

        # Path to the last APK created
        self.last_generated_apk = None

        # Global variables
        self.decompile_dir = None
        self.manifest_path = None
        self.strings_path = None

    def decompile(self, output: Union[str, Path] = None, overwrite: bool = True) -> bool:
        """
        Decompile an APK file.
        :param output: the output folder
        :param overwrite: whether to overwrite a folder
        :return: str (path to the decompiled folder)
        """

        # Create the command
        command = f'java -jar {self.apktool_path} d {self.apk_path}'
        if output:
            command += f" -o {output}"
        if overwrite:
            command += " -f"

        # Print the commands
        fprint.logger("Command", command, mode="info")
        fprint.logger("Decompile", "Trying to decompile APK...", mode="info")

        _, stderr = execute.command(command)

        # Exit if there's an error
        if stderr:
            logging.error(stderr)
            fprint.logger("Decompile", stderr, mode="error")
            return False

        # Get the decompiled APK folder (same name as the base APK)
        directory = os.path.join(self.root,
                                 os.path.basename(self.apk_path).replace(".apk", "")) if not output else output

        fprint.logger("Status", "APK Decompiled successfuly", mode="success")
        fprint.logger("Path", f"The decompiled APK is in: {directory}", mode="info")

        # Assign the manifest path
        self.manifest_path = os.path.join(directory, "AndroidManifest.xml")
        # Assign the strings.xml file path
        self.strings_path = os.path.join(directory, "res", "values", "strings.xml")

        self.decompile_dir = directory
        return True

    def rename_package(self, val: str) -> bool:
        """
        Update the manifest located inside the decompiled APK file.
        Changes the AndroidManifest.xml.
        :return:
        """
        if not self.manifest_path:
            logging.error("self.manifest_path not defined")
            fprint.logger("Status", "Please decompile the APK or set the paths of the already decompiled APK manually.",
                          mode="error")
            return False

        # Open the manifest file
        try:
            with open(self.manifest_path, "r") as file:
                manifest = file.read()

        except FileNotFoundError:
            # If the manifest is not found
            logging.error(FileNotFoundError)
            fprint.logger("Rename Package", f"Manifest not found in: {self.decompile_dir}", mode="error")
            return False

        fprint.logger("Manifest found", self.manifest_path, mode="success")

        # Get the package name
        package_name = re.search(RePatterns.package_name, manifest)
        fprint.logger("Package Name Found", package_name.group(0), mode="success")

        # Remove the com.app from the package name = ("com.app.example" -> "example")
        name = package_name.group(0).replace("com.app.", "")
        # Replace all the occurrences of the name with the new one
        new_xml = re.sub(name, val, manifest, flags=re.IGNORECASE)

        # Write the new manifest
        with open(self.manifest_path, "w") as file:
            manifest = file.write(new_xml)

        fprint.logger("Manifest Updated", self.manifest_path, mode="success")

        return True

    def rename_app(self, val1: str, val2: str) -> bool:
        """
        Get all the lines with the string "app_name".
        Then replace the val1 for the val2 only in those lines.
        :param val1: val1
        :param val2: val2
        :return: bool
        """

        if not self.strings_path:
            logging.error("self.strings_path not defined")
            fprint.logger("Status", "Please decompile the APK or set the paths of the already decompiled APK manually.",
                          mode="error")
            return False

        # Open the strings file
        try:
            with open(self.strings_path, "r", encoding="utf-8") as file:
                strings = file.read()

        except FileNotFoundError:
            # If the file is not found
            logging.error(FileNotFoundError)
            fprint.logger("Status", f"File strings.xml not found in: {self.decompile_dir}", mode="error")
            return False

        fprint.logger("File found", self.strings_path, mode="success")

        lines = []
        for line in strings.splitlines():
            if "app_name" in line:
                line = re.sub(val1, val2, line, flags=re.IGNORECASE)
            lines.append(line)

        new_strings = "\n".join(lines) + "\n"

        if new_strings == strings:
            fprint.logger("Rename", "No values replaced!", mode="error")
            return False

        with open(self.strings_path, "w", encoding="utf-8") as file:
            file.write(new_strings)

        fprint.logger("Rename", "Values replaced!", mode="success")

        return True

    def build(self, output: Union[str, Path] = None) -> bool:
        fprint.logger("Status", "Trying to build the new APK...", mode="info")

        # Create the command
        command = f'java -jar {self.apktool_path} b {self.decompile_dir}'
        # Add params to the command
        command += f" -o {output} --use-aapt2" if output else " --use-aapt2"

        fprint.logger("Command", command, mode="info")

        # Build the solution directory with the updated file(s)
        _, stderr = execute.command(command)

        if stderr:
            logging.error(stderr)
            fprint.logger("Status", "Couldn't build the APK", "error")
            return False

        if output:
            self.last_generated_apk = output
            fprint.logger("Built", "The APK has been built successfully", mode="success")
        else:
            self.last_generated_apk = os.path.join(self.decompile_dir, "dist", os.path.basename(self.apk_path))
            fprint.logger("Built", "The APK has been built successfully inside the dist directory", mode="success")

        return True

    def sign(self, output: Union[str, Path] = None) -> bool:
        """
        Generate a new signed APK valid for installation.
        :param output: path to save the signed APK
        :return: bool
        """
        fprint.logger("Status", "Trying to sign the APK...", mode="info")

        # Create the command
        command = f'java -jar {self.apksigner_path} --apks {self.last_generated_apk}'

        self.last_generated_apk = os.path.join(self.decompile_dir, "dist", ".".join(
            os.path.basename(self.apk_path).split('.')[:-1]) + "aligned-debugSigned.apk")

        if output:
            self.last_generated_apk = output
            command += f" -o {output}"

        fprint.logger("Command", command, mode="info")
        # Sign the APK
        stdout, stderr = execute.command(command)

        if not stderr:
            fprint.logger("Signed", "Successfully signed APK!", mode="success")
            fprint.logger("Find your signed APK in", self.last_generated_apk, mode="info")
            return True
        logging.error(stderr)
        fprint.logger("Status", "Couldn't sign the APK", mode="error")
        return False
