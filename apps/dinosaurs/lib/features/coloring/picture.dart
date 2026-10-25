import 'dart:convert';
import 'dart:ui';

import 'package:flutter/services.dart' show rootBundle;

/// One fillable area of a picture. Geometry is in a 100 x 100 coordinate
/// dinosaurs, so the same picture works at any screen size.
class Region {
  Region(this.path);

  final Path path;

  factory Region.fromJson(Map<String, dynamic> json) {
    final path = Path();
    switch (json['type'] as String) {
      case 'poly':
        final points = (json['points'] as List)
            .map((p) => Offset((p[0] as num).toDouble(), (p[1] as num).toDouble()))
            .toList();
        path.addPolygon(points, true);
      case 'circle':
        final c = json['c'] as List;
        final r = (json['r'] as num).toDouble();
        path.addOval(Rect.fromCircle(
          center: Offset((c[0] as num).toDouble(), (c[1] as num).toDouble()),
          radius: r,
        ));
      case 'ellipse':
        final ec = json['c'] as List;
        path.addOval(Rect.fromCenter(
          center: Offset((ec[0] as num).toDouble(), (ec[1] as num).toDouble()),
          width: (json['rx'] as num).toDouble() * 2,
          height: (json['ry'] as num).toDouble() * 2,
        ));
      case 'rect':
        path.addRect(Rect.fromLTWH(
          (json['x'] as num).toDouble(),
          (json['y'] as num).toDouble(),
          (json['w'] as num).toDouble(),
          (json['h'] as num).toDouble(),
        ));
      default:
        throw FormatException('Unknown region type: ${json['type']}');
    }
    return Region(path);
  }
}

/// A coloring picture: a list of regions drawn in order, later ones on top.
class Picture {
  Picture({required this.id, required this.nameKey, required this.regions});

  /// Side length of the square coordinate dinosaurs all pictures are drawn in.
  static const double unit = 100;

  final String id;

  /// Key in assets/i18n/<lang>.json for the picture's display name.
  final String nameKey;
  final List<Region> regions;

  factory Picture.fromJson(Map<String, dynamic> json) {
    return Picture(
      id: json['id'] as String,
      nameKey: json['name_key'] as String,
      regions: (json['regions'] as List)
          .map((r) => Region.fromJson(r as Map<String, dynamic>))
          .toList(),
    );
  }

  /// Index of the top-most region containing [point] (in the 0..100 dinosaurs),
  /// or null if the point is outside every region.
  int? hitTest(Offset point) {
    for (var i = regions.length - 1; i >= 0; i--) {
      if (regions[i].path.contains(point)) return i;
    }
    return null;
  }
}

/// Loads every picture listed in assets/pictures/index.json.
class PictureLibrary {
  PictureLibrary._();

  static Future<List<Picture>> load() async {
    final indexRaw = await rootBundle.loadString('assets/pictures/index.json');
    final ids = (jsonDecode(indexRaw) as List).cast<String>();
    final pictures = <Picture>[];
    for (final id in ids) {
      final raw = await rootBundle.loadString('assets/pictures/$id.json');
      pictures.add(Picture.fromJson(jsonDecode(raw) as Map<String, dynamic>));
    }
    return pictures;
  }
}
