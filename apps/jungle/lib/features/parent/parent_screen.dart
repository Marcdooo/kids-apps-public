import 'package:flutter/material.dart';

import '../../core/app_config.dart';
import '../../core/app_controller.dart';

/// Grown-ups area (opened only after the parent gate): language and privacy.
class ParentScreen extends StatelessWidget {
  const ParentScreen({super.key, required this.controller});

  final AppController controller;

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        final strings = controller.strings;
        return Scaffold(
          appBar: AppBar(title: Text(strings.t('parent_area'))),
          body: SafeArea(
            child: ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Text(
                  strings.t('language'),
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                for (final entry in AppConfig.languages.entries)
                  ListTile(
                    title: Text(entry.value),
                    trailing: entry.key == strings.languageCode
                        ? const Icon(Icons.check)
                        : null,
                    onTap: () => controller.setLanguage(entry.key),
                  ),
                const Divider(height: 32),
                Text(
                  strings.t('privacy_title'),
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 8),
                Text(strings.t('privacy_text')),
              ],
            ),
          ),
        );
      },
    );
  }
}
