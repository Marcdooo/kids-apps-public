import 'package:flutter/foundation.dart';

import '../features/coloring/picture.dart';
import 'settings_store.dart';
import 'strings.dart';

/// Holds the app-wide state: current language, saved progress, the pictures.
class AppController extends ChangeNotifier {
  AppController({
    required this.store,
    required Strings strings,
    required this.pictures,
  }) : _strings = strings;

  final SettingsStore store;
  final List<Picture> pictures;
  Strings _strings;

  Strings get strings => _strings;

  Future<void> setLanguage(String code) async {
    _strings = await Strings.load(code);
    await store.setLanguageCode(code);
    notifyListeners();
  }
}
