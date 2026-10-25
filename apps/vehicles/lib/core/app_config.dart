import 'package:flutter/material.dart';

/// Per-app settings. When you clone the template for a new app, this and the
/// files in assets/ are the only things that normally change.
class AppConfig {
  AppConfig._();

  /// Languages that have a file in assets/i18n/<code>.json.
  /// Keys are language codes, values are the language's own name.
  static const Map<String, String> languages = {
    'en': 'English',
    'fr': 'Français',
    'de': 'Deutsch',
    'es': 'Español',
    'it': 'Italiano',
    'pt': 'Português',
    'nl': 'Nederlands',
    'pl': 'Polski',
    'ja': '日本語',
  };

  /// Used when the device language is not in [languages], and for any
  /// string missing from a translation.
  static const String fallbackLanguage = 'en';

  static const Color seedColor = Color(0xFFFB8C00);

  /// Colors offered in the palette. Saved progress stores the index into this
  /// list, so only ever append to it; never reorder or remove entries.
  static const List<Color> palette = [
    Color(0xFFE53935), // red
    Color(0xFFFB8C00), // orange
    Color(0xFFFDD835), // yellow
    Color(0xFF9CCC65), // lime
    Color(0xFF2E7D32), // green
    Color(0xFF29B6F6), // sky blue
    Color(0xFF1E88E5), // blue
    Color(0xFF8E24AA), // purple
    Color(0xFFF48FB1), // pink
    Color(0xFF6D4C41), // brown
    Color(0xFF9E9E9E), // grey
    Color(0xFFFFFFFF), // white (works as an eraser)
  ];
}
