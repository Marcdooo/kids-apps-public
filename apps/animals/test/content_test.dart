import 'dart:convert';
import 'dart:io';
import 'dart:ui';

import 'package:flutter_test/flutter_test.dart';
import 'package:animals/features/coloring/picture.dart';

void main() {
  test('hit test returns the top-most region', () {
    final picture = Picture.fromJson({
      'id': 't',
      'name_key': 'pic_t',
      'regions': [
        {'type': 'rect', 'x': 0, 'y': 0, 'w': 100, 'h': 100},
        {'type': 'circle', 'c': [50, 50], 'r': 10},
      ],
    });
    expect(picture.hitTest(const Offset(50, 50)), 1);
    expect(picture.hitTest(const Offset(5, 5)), 0);
    expect(picture.hitTest(const Offset(150, 150)), isNull);
  });

  test('every picture file parses and has a name in every language', () {
    final ids = (jsonDecode(File('assets/pictures/index.json').readAsStringSync())
            as List)
        .cast<String>();
    final languages = Directory('assets/i18n')
        .listSync()
        .whereType<File>()
        .where((f) => f.path.endsWith('.json'))
        .map((f) => jsonDecode(f.readAsStringSync()) as Map<String, dynamic>)
        .toList();
    expect(languages, isNotEmpty);

    for (final id in ids) {
      final json = jsonDecode(File('assets/pictures/$id.json').readAsStringSync())
          as Map<String, dynamic>;
      final picture = Picture.fromJson(json);
      expect(picture.regions, isNotEmpty);
      for (final table in languages) {
        expect(table.containsKey(picture.nameKey), isTrue,
            reason: 'missing ${picture.nameKey}');
      }
    }
  });

  test('all languages have the same keys as English', () {
    final english =
        jsonDecode(File('assets/i18n/en.json').readAsStringSync())
            as Map<String, dynamic>;
    for (final file in Directory('assets/i18n').listSync().whereType<File>()) {
      if (!file.path.endsWith('.json')) continue;
      final table = jsonDecode(file.readAsStringSync()) as Map<String, dynamic>;
      expect(table.keys.toSet(), english.keys.toSet(), reason: file.path);
    }
  });
}
