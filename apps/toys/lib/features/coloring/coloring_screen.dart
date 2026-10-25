import 'package:flutter/material.dart';

import '../../core/app_config.dart';
import '../../core/app_controller.dart';
import 'picture.dart';
import 'picture_painter.dart';

class ColoringScreen extends StatefulWidget {
  const ColoringScreen({
    super.key,
    required this.controller,
    required this.picture,
  });

  final AppController controller;
  final Picture picture;

  @override
  State<ColoringScreen> createState() => _ColoringScreenState();
}

class _ColoringScreenState extends State<ColoringScreen> {
  static const int _maxUndo = 50;

  late Map<int, int> _fills;
  final List<Map<int, int>> _history = [];
  int _selected = 0;

  @override
  void initState() {
    super.initState();
    _fills = widget.controller.store.loadFills(widget.picture.id);
  }

  void _save() {
    widget.controller.store.saveFills(widget.picture.id, _fills);
  }

  void _pushHistory() {
    _history.add(Map<int, int>.of(_fills));
    if (_history.length > _maxUndo) _history.removeAt(0);
  }

  void _onTap(Offset local, double side) {
    final point = Offset(
      local.dx / side * Picture.unit,
      local.dy / side * Picture.unit,
    );
    final hit = widget.picture.hitTest(point);
    if (hit == null || _fills[hit] == _selected) return;
    setState(() {
      _pushHistory();
      _fills[hit] = _selected;
    });
    _save();
  }

  void _undo() {
    if (_history.isEmpty) return;
    setState(() => _fills = _history.removeLast());
    _save();
  }

  void _clear() {
    if (_fills.isEmpty) return;
    setState(() {
      _pushHistory();
      _fills = {};
    });
    _save();
  }

  @override
  Widget build(BuildContext context) {
    final strings = widget.controller.strings;
    return Scaffold(
      appBar: AppBar(
        title: Text(strings.t(widget.picture.nameKey)),
        actions: [
          IconButton(
            tooltip: strings.t('undo'),
            icon: const Icon(Icons.undo),
            onPressed: _history.isEmpty ? null : _undo,
          ),
          IconButton(
            tooltip: strings.t('clear'),
            icon: const Icon(Icons.delete_outline),
            onPressed: _fills.isEmpty ? null : _clear,
          ),
        ],
      ),
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            final landscape = constraints.maxWidth > constraints.maxHeight;
            return Flex(
              direction: landscape ? Axis.horizontal : Axis.vertical,
              children: [
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Center(
                      child: AspectRatio(
                        aspectRatio: 1,
                        child: LayoutBuilder(
                          builder: (context, box) {
                            final side = box.maxWidth;
                            return GestureDetector(
                              onTapDown: (d) => _onTap(d.localPosition, side),
                              child: CustomPaint(
                                size: Size.square(side),
                                painter: PicturePainter(
                                  picture: widget.picture,
                                  fills: _fills,
                                ),
                              ),
                            );
                          },
                        ),
                      ),
                    ),
                  ),
                ),
                _buildPalette(landscape),
              ],
            );
          },
        ),
      ),
    );
  }

  Widget _buildPalette(bool landscape) {
    // Scrollable so a short landscape phone screen can't overflow.
    return Container(
      width: landscape ? 150 : null,
      padding: const EdgeInsets.all(12),
      child: SingleChildScrollView(
        child: Wrap(
          spacing: 10,
          runSpacing: 10,
          alignment: WrapAlignment.center,
          children: [
            for (var i = 0; i < AppConfig.palette.length; i++)
              GestureDetector(
                onTap: () => setState(() => _selected = i),
                child: Container(
                  width: 48,
                  height: 48,
                  decoration: BoxDecoration(
                    color: AppConfig.palette[i],
                    shape: BoxShape.circle,
                    border: Border.all(
                      color: i == _selected
                          ? const Color(0xFF263238)
                          : const Color(0xFFB0BEC5),
                      width: i == _selected ? 4 : 1.5,
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
