# AUAX APK EDITOR


## Usage 

Run the `apk_editor.py` file and add the flag `-h` to get help.

    python3 apk_editor.py [-h] -i APK input path -instr *Input string* -outstr Output string
    [-o [target]] [-apt [apktool path]] [-aps [apktool path]]
    [-w [overwrite]]

### **Arguments:**
| **Command** | **Description**                                                                                                                                                           | **Required** |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| **-i**      | APK input path.                                                                                                                                                           | Yes          |
| **-instr**  | Input string will be replaced with the output string in the Strings.xml file. Recommended to set this to the app name                                                     | Yes          |
| **-outstr** | The output string will replace the input string in the Strings.xml file.                                                                                                  | Yes          |
| **-o**      | APK output path. (Final signed APK).                                                                                                                                      | No           |
| **-apt**    | The path to the Apktool JAR file. (Included under the ./libs folder). If you don't specify the argument, the program will try to find the file in the ./lib folder.       | No           |
| **-aps**    | The path to the Apksigner JAR file. (Included under the ./libs folder). If you don't specify the argument, the program will try to find the file in the ./lib folder.     | No           |
| **-w**      | Overwrite files if necessary.                                                                                                                                             | No           |


### **Example:**
    python3 apk_editor.py -i apkpure.apk --instr APKPure --outstr Auax -o new.apk -w 

Will locate the **APK** `apkpure.apk` (in the same folder), and replace the string *APKPure* (app name) for the new string *Auax*. Then it will sign the APK and save it with the name *new.apk*.

---

## Todo 
1. Fix the *rename_package* method. (Disabled because sometimes there's trouble trying to sign the APK).
2. Improve the renaming methodology.
3. Add new functionality. You can suggest anything through my email or GitHub.

---

## About the *Lib* files

**APKTOOL** v2.6.0 (https://github.com/iBotPeaches/Apktool)

**APKSIGNER**: v1.2.1 (https://github.com/patrickfav/uber-apk-signer)