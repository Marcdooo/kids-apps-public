import 'dart:convert';

import 'package:flutter/services.dart' show rootBundle;

import 'app_config.dart';

/// Tiny translation lookup backed by assets/i18n/<code>.json.
/// A key missing from the chosen language falls back to English, and a key
/// missing everywhere shows the key itself, so a gap is visible but never
/// crashes the app.
class Strings {
  Strings._(this.languageCode, this._table, this._fallback);

  final String languageCode;
  final Map<String, String> _table;
  final Map<String, String> _fallback;

  static Future<Strings> load(String code) async {
    final fallback = await _read(AppConfig.fallbackLanguage);
    final table =
        code == AppConfig.fallbackLanguage ? fallback : await _read(code);
    return Strings._(code, table, fallback);
  }

  static Future<Map<String, String>> _read(String code) async {
    final raw = await rootBundle.loadString('assets/i18n/$code.json');
    final decoded = jsonDecode(raw) as Map<String, dynamic>;
    return decoded.map((key, value) => MapEntry(key, value as String));
  }

  /// Looks up [key]; each `{name}` in the text is replaced from [args].
  String t(String key, [Map<String, String> args = const {}]) {
    var text = _table[key] ?? _fallback[key] ?? key;
    args.forEach((name, value) {
      text = text.replaceAll('{$name}', value);
    });
    return text;
  }
}
