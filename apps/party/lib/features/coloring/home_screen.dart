import 'package:flutter/material.dart';

import '../../core/app_controller.dart';
import '../../core/parent_gate.dart';
import '../parent/parent_screen.dart';
import 'coloring_screen.dart';
import 'picture_painter.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key, required this.controller});

  final AppController controller;

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Future<void> _openParentArea() async {
    final strings = widget.controller.strings;
    final passed = await showParentGate(context, strings);
    if (!passed || !mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ParentScreen(controller: widget.controller),
      ),
    );
  }

  Future<void> _openPicture(int index) async {
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ColoringScreen(
          controller: widget.controller,
          picture: widget.controller.pictures[index],
        ),
      ),
    );
    // Refresh thumbnails with whatever was colored.
    if (mounted) setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    final strings = widget.controller.strings;
    final pictures = widget.controller.pictures;
    return Scaffold(
      appBar: AppBar(
        title: Text(strings.t('app_title')),
        actions: [
          IconButton(
            tooltip: strings.t('parent_area'),
            icon: const Icon(Icons.lock_outline),
            onPressed: _openParentArea,
          ),
        ],
      ),
      body: SafeArea(
        child: GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
            maxCrossAxisExtent: 240,
            mainAxisSpacing: 16,
            crossAxisSpacing: 16,
            childAspectRatio: 0.9,
          ),
          itemCount: pictures.length,
          itemBuilder: (context, index) {
            final picture = pictures[index];
            final fills = widget.controller.store.loadFills(picture.id);
            return Card(
              clipBehavior: Clip.antiAlias,
              child: InkWell(
                onTap: () => _openPicture(index),
                child: Column(
                  children: [
                    Expanded(
                      child: Padding(
                        padding: const EdgeInsets.all(8),
                        child: AspectRatio(
                          aspectRatio: 1,
                          child: CustomPaint(
                            painter: PicturePainter(
                              picture: picture,
                              fills: fills,
                            ),
                          ),
                        ),
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(bottom: 10),
                      child: Text(
                        strings.t(picture.nameKey),
                        style: Theme.of(context).textTheme.titleMedium,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
