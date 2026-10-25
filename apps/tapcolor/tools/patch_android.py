#!/usr/bin/env python3
"""Applies this repo's standard changes to a freshly generated android/ folder.

    python3 tools/patch_android.py

Run once, right after `flutter create` (the Bootstrap Android workflow does it):
  * release signing: build.gradle.kts uses android/key.properties when present
    (CI writes it from repo secrets), otherwise the debug key
  * the launcher name comes from string resources, one per language, taken from
    app_title in assets/i18n/<lang>.json (values-<lang>/strings.xml)
"""
import json
import os
import re
import sys
from xml.sax.saxutils import escape

ROOT = os.path.join(os.path.dirname(__file__), "..")
ANDROID = os.path.join(ROOT, "android")
GRADLE = os.path.join(ANDROID, "app", "build.gradle.kts")
MANIFEST = os.path.join(ANDROID, "app", "src", "main", "AndroidManifest.xml")
RES = os.path.join(ANDROID, "app", "src", "main", "res")
I18N = os.path.join(ROOT, "assets", "i18n")

HEADER = '''import java.io.FileInputStream
import java.util.Properties

// Release signing: android/key.properties is written by CI from repo secrets
// (see .github/workflows/build-apk.yml). Without it, builds use the debug key.
val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

'''

SIGNING = '''    signingConfigs {
        create("release") {
            if (keystorePropertiesFile.exists()) {
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
                storeFile = rootProject.file(keystoreProperties["storeFile"] as String)
                storePassword = keystoreProperties["storePassword"] as String
            }
        }
    }

'''

RELEASE_OLD = re.compile(
    r"        release \{.*?signingConfig = signingConfigs\.getByName\(\"debug\"\)\n        \}",
    re.S)
RELEASE_NEW = '''        release {
            signingConfig = if (keystorePropertiesFile.exists()) {
                signingConfigs.getByName("release")
            } else {
                signingConfigs.getByName("debug")
            }
        }'''


def patch_gradle():
    text = open(GRADLE, encoding="utf-8").read()
    if "keystoreProperties" in text:
        print("build.gradle.kts already patched")
        return
    if not RELEASE_OLD.search(text):
        sys.exit("build.gradle.kts: release block not found (Flutter template changed?)")
    text = RELEASE_OLD.sub(RELEASE_NEW, text, count=1)
    text = text.replace("    buildTypes {", SIGNING + "    buildTypes {", 1)
    open(GRADLE, "w", encoding="utf-8").write(HEADER + text)
    print("build.gradle.kts patched")


def patch_manifest():
    text = open(MANIFEST, encoding="utf-8").read()
    new = re.sub(r'android:label="[^"]*"', 'android:label="@string/app_name"', text, count=1)
    if new == text and "@string/app_name" not in text:
        sys.exit("AndroidManifest.xml: label not found")
    open(MANIFEST, "w", encoding="utf-8").write(new)
    print("manifest label -> @string/app_name")


def write_names():
    for fname in sorted(os.listdir(I18N)):
        if not fname.endswith(".json"):
            continue
        lang = fname[:-5]
        title = json.load(open(os.path.join(I18N, fname), encoding="utf-8"))["app_title"]
        folder = "values" if lang == "en" else "values-" + lang
        os.makedirs(os.path.join(RES, folder), exist_ok=True)
        with open(os.path.join(RES, folder, "strings.xml"), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
                    f'    <string name="app_name">{escape(title)}</string>\n</resources>\n')
        print(f"{folder}/strings.xml: {title}")


if __name__ == "__main__":
    if not os.path.isdir(ANDROID):
        sys.exit("android/ not found: run flutter create first")
    patch_gradle()
    patch_manifest()
    write_names()
