import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

/// Everything the app remembers lives here, on the device only.
/// Nothing is sent anywhere.
class SettingsStore {
  SettingsStore._(this._prefs);

  final SharedPreferences _prefs;

  static Future<SettingsStore> load() async =>
      SettingsStore._(await SharedPreferences.getInstance());

  String? get languageCode => _prefs.getString('lang');

  Future<void> setLanguageCode(String code) =>
      _prefs.setString('lang', code);

  /// Saved coloring for one picture: region index -> palette index.
  Map<int, int> loadFills(String pictureId) {
    final raw = _prefs.getString('fills_$pictureId');
    if (raw == null) return {};
    try {
      final decoded = jsonDecode(raw) as Map<String, dynamic>;
      return decoded.map((k, v) => MapEntry(int.parse(k), v as int));
    } catch (_) {
      return {};
    }
  }

  Future<void> saveFills(String pictureId, Map<int, int> fills) {
    final encodable = fills.map((k, v) => MapEntry(k.toString(), v));
    return _prefs.setString('fills_$pictureId', jsonEncode(encodable));
  }
}
