import argparse
import os
import shutil
import sys

import execute
from format_print import fprint
from tools_wrapper import AuaxAPK

"""
Welcome to the main file for the APK editor by Auax (2006).
---------------------------------------------------------------------
Warning:
The AuaxAPK.rename_package method might not work during the build of the APK.
It's not recommended to use it for now. Therefore it's not enabled as a CLI option.

"""


def exit_c(b):
    if not b:
        sys.exit(-1)


def main():
    # Path to the project's root folder
    root = os.path.dirname(os.path.abspath(__file__))

    # Arguments
    try:
        parser = argparse.ArgumentParser(description="Auax's APK Editor")
        parser.add_argument("-i",
                            "--input",
                            metavar="APK input path",
                            type=str,
                            help="APK input path.",
                            required=True)

        parser.add_argument("-instr",
                            "--instring",
                            metavar="Input string",
                            type=str,
                            help="Input string that will be replaced with the ouput string in the Strings.xml file.",
                            required=True)

        parser.add_argument("-outstr",
                            "--outstring",
                            metavar="Output string",
                            type=str,
                            help="The output string that will replace the input string in the Strings.xml file.",
                            required=True)

        parser.add_argument("-o",
                            "--output",
                            metavar="target",
                            type=str,
                            nargs="?",
                            help="APK output path.")

        parser.add_argument("-apt",
                            "-apktool",
                            metavar="apktool path",
                            type=str,
                            nargs="?",
                            help="The path to the apktool JAR file.")

        parser.add_argument("-aps",
                            "-apksigner",
                            metavar="apktool path",
                            type=str,
                            nargs="?",
                            help="The path to the apksigner JAR file.")

        parser.add_argument("-w",
                            "--overwrite",
                            metavar="overwrite",
                            type=str,
                            nargs="?",
                            help="Overwrite files if necessary.")

        args = parser.parse_args()  # Parse args

    except ValueError:
        fprint.logger("Argument", "Please pass the correct arguments! Add -h for help.", mode="error")
        sys.exit(-1)

    # Handle errors
    if not os.path.exists(args.input):
        fprint.logger("Argument", "APK path does not exist!", mode="error")
        sys.exit(-1)

    if args.apt and args.aps:
        apktool_path = args.apt
        apksigner_path = args.aps

    # APKTool
    if not args.apt:
        fprint.logger("Argument", "Trying to automatically detect the path to the apktool JAR file...", mode="info")
        fprint.logger("Default 'apktool' name", "apktool.jar", mode="info")
        apktool_path = os.path.join(root, "libs", "apktool", "apktool.jar")

        if not os.path.exists(apktool_path):
            fprint.logger("APKTOOL not found",
                          "It should be inside the root folder of the project, under libs/apktool",
                          mode="error")
            sys.exit(-1)
        fprint.logger("Found", "apksigner", mode="success")

    # APKSigner
    if not args.aps:
        fprint.logger("Argument", "Trying to automatically detect the path to the apksigner JAR file...", mode="info")
        fprint.logger("Default 'apksigner' name", "apksigner.jar", mode="info")
        apksigner_path = os.path.join(root, "libs", "apksigner", "apksigner.jar")

        if not os.path.exists(apksigner_path):
            fprint.logger("APKSIGNER not found",
                          "It should be inside the root folder of the project, under libs/apksigner",
                          mode="error")
            sys.exit(-1)
        fprint.logger("Found", "apksigner", mode="success")

    input_path = args.input
    output_path = args.output
    overwrite = args.overwrite
    instring = args.instring
    outstring = args.outstring

    apk = AuaxAPK(apktool_path, apksigner_path, input_path)
    exit_c(apk.decompile())
    exit_c(apk.rename_app(instring, outstring))
    exit_c(apk.build())
    exit_c(apk.sign(output_path if output_path else None))

    if output_path:
        ask = input("Remove decompiled folder? (y/n): ")
        if "y" in ask.lower():
            shutil.rmtree(apk.decompile_dir)
            fprint.logger("Folder deleted", apk.decompile_dir, mode="success")

    ask = input("Open Folder? (y/n): ")
    if "y" in ask.lower():
        print(apk.last_generated_apk)
        execute.command(f"explorer {os.path.dirname(apk.last_generated_apk)}")


if __name__ == "__main__":
    try:
        os.system("cls" if os.name == "nt" else "clear")
        print("AUAX APK EDITOR\n" + "-" * 50 + "\n")
        main()
        print("\n\nThanks for using APKEditor (by AUAX). Happy coding! ❤️")

    except KeyboardInterrupt:
        fprint.logger("Exiting...", "KeyboardInterrupt detected!", "success")
        sys.exit(-1)
