# tapcolor: kids app template + first app (tap-to-fill coloring)

An offline Flutter app for young children: pick a picture, pick a color, tap an
area to fill it. No ads, no analytics, no accounts, no internet permission, no
third-party SDKs except `shared_preferences` (saves progress on the device).
Languages: English, French, Polish (more are just another JSON file).

This is also the **template** for the rest of your apps: a new app is a new
content pack (pictures + text + icon), not new code. See "Making the next app".

## Status: what is and isn't verified

- **Verified here (scripts):** all 6 pictures parse, every region has enough
  visible area to be tapped, translation files have identical keys and
  placeholders, `tools/new_app.py` clones and renames correctly.
- **NOT verified:** the Dart code has never been compiled or run. Flutter could
  not be installed in the workspace this was written in. Expect to fix a few
  small compile errors or lint warnings on first build. Run `flutter analyze`
  and `flutter test` first, then try it on a real Fire tablet.
- **Not done yet:** app icon, store screenshots, store listing text, signing keys.
- **Translations:** French and Polish were written by an AI model, not a native
  proofreader. They are short, but have them checked before publishing.

## First run (once per computer)

1. Install Flutter (https://docs.flutter.dev/get-started/install) and Android Studio
   (for the Android SDK). Run `flutter doctor` until Android is green.
2. In this folder, generate the Android project (not included in the template):

       flutter create --org com.YOURNAME --project-name tapcolor .
       flutter pub get
       flutter analyze
       flutter test
       flutter run            # with a tablet or emulator connected

   Pick `--org` once and keep it for all apps (e.g. `com.badrapps`). The app id
   becomes `<org>.<project-name>` and **cannot be changed after publishing**.
3. Set the app name shown under the icon: in `android/app/src/main/AndroidManifest.xml`
   change `android:label` (this name is not translated; the in-app title is).
4. Remove permissions you don't use. The template needs none; `flutter create`
   adds only INTERNET in debug builds.

## Release builds

- **Google Play:** `flutter build appbundle --release` (needs an upload key:
  https://docs.flutter.dev/deployment/android#sign-the-app).
- **Amazon Appstore:** `flutter build apk --release`. As far as I know Amazon
  takes APK files; confirm in the Developer Console when you upload.
- Use the **same signing keystore for all apps** and back it up. If you lose it
  you lose the ability to update every app.
- Test on a real Fire tablet before publishing there. Fire OS is an Android fork,
  but behavior (fonts, back button, performance on low-end tablets) can differ.

## Store checklist (every app)

Do these in each console; exact form fields change, so read them as you go.

- [ ] Declare the app as **child-directed / for children** in both stores.
- [ ] Privacy policy URL (one shared page is fine). The text can be: collects no
      personal data, no ads, no analytics, progress stored only on the device.
- [ ] Data safety / data collection forms: collects nothing.
- [ ] Content rating questionnaire.
- [ ] Price: start at $0.99 / the local equivalent, paid upfront (no in-app purchase
      code is needed for this).
- [ ] Listing text, screenshots, and icon in **every language you ship**.
      Search in each store for your app name first so you don't collide with an
      existing app or trademark.
- [ ] Artwork is original (it is, in this template). If you add licensed art or
      sound, keep the license text.

## Adding things

**A picture:** add a function in `tools/make_pictures.py` (regions in a 100 x 100
space, later regions are drawn on top), add its name to `PICTURES`, add a
`pic_<id>` line to every `assets/i18n/*.json`, then run:

    python3 tools/make_pictures.py
    python3 tools/validate_content.py --preview-dir /tmp/preview   # look at preview.png

Keep every region big enough for a small finger; the validator enforces a minimum
visible area.

**A language:** copy `assets/i18n/en.json` to `<code>.json`, translate the values
(keep `{a}` / `{b}` as they are), and add the code to `languages` in
`lib/core/app_config.dart`. `validate_content.py` fails if anything is missing.
Also translate the store listing for that language.

**A palette color:** append to `AppConfig.palette`. Never reorder or remove, or
children's saved pictures change color.

## Making the next app

    python3 tools/new_app.py ../sea_coloring --name sea_coloring
    cd ../sea_coloring
    flutter create --org com.YOURNAME --project-name sea_coloring .

Then replace the pictures, titles and picture names, add an icon
(e.g. with the `flutter_launcher_icons` package), validate, build.
The coloring engine can carry many different apps (animals, vehicles, dinosaurs,
numbers) just by swapping the picture pack. Other app types (matching game,
sound board, counting) would be new feature folders reusing `core/`.

## Layout

    lib/core/               language lookup, saved progress, parent gate, config
    lib/features/coloring/  picture model, painter, home grid, coloring screen
    lib/features/parent/    grown-ups area (language, privacy text)
    assets/pictures/        one JSON file per picture + index.json
    assets/i18n/            one JSON file per language
    tools/                  make_pictures, validate_content, new_app (Python 3, Pillow)
    test/                   content tests (run with `flutter test`)

The parent gate is a small addition question; it only guards the grown-ups
screen. Nothing in the app links out to the web or to stores.
