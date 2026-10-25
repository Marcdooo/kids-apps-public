import 'package:flutter/material.dart';

import '../../core/app_config.dart';
import 'picture.dart';

/// Draws a picture with the given fills (region index -> palette index).
/// Unfilled regions are white.
class PicturePainter extends CustomPainter {
  PicturePainter({required this.picture, required this.fills});

  final Picture picture;
  final Map<int, int> fills;

  static const Color _outline = Color(0xFF263238);

  @override
  void paint(Canvas canvas, Size size) {
    canvas.clipRect(Offset.zero & size);
    canvas.save();
    canvas.scale(size.width / Picture.unit, size.height / Picture.unit);

    final fillPaint = Paint()..style = PaintingStyle.fill;
    final linePaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = 0.9
      ..strokeJoin = StrokeJoin.round
      ..color = _outline;

    for (var i = 0; i < picture.regions.length; i++) {
      final paletteIndex = fills[i];
      fillPaint.color =
          (paletteIndex != null && paletteIndex < AppConfig.palette.length)
              ? AppConfig.palette[paletteIndex]
              : Colors.white;
      canvas.drawPath(picture.regions[i].path, fillPaint);
      canvas.drawPath(picture.regions[i].path, linePaint);
    }
    canvas.restore();
  }

  // Cheap enough to always repaint, and avoids stale pictures if the same
  // fills map is mutated in place.
  @override
  bool shouldRepaint(covariant PicturePainter oldDelegate) => true;
}
