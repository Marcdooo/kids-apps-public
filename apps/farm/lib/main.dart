import 'package:flutter/material.dart';

import 'core/app_config.dart';
import 'core/app_controller.dart';
import 'core/settings_store.dart';
import 'core/strings.dart';
import 'features/coloring/home_screen.dart';
import 'features/coloring/picture.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final store = await SettingsStore.load();
  final deviceLanguage =
      WidgetsBinding.instance.platformDispatcher.locale.languageCode;
  final saved = store.languageCode;
  final language = AppConfig.languages.containsKey(saved)
      ? saved!
      : AppConfig.languages.containsKey(deviceLanguage)
          ? deviceLanguage
          : AppConfig.fallbackLanguage;

  final controller = AppController(
    store: store,
    strings: await Strings.load(language),
    pictures: await PictureLibrary.load(),
  );

  runApp(KidsApp(controller: controller));
}

class KidsApp extends StatelessWidget {
  const KidsApp({super.key, required this.controller});

  final AppController controller;

  @override
  Widget build(BuildContext context) {
    return ListenableBuilder(
      listenable: controller,
      builder: (context, _) {
        return MaterialApp(
          title: controller.strings.t('app_title'),
          debugShowCheckedModeBanner: false,
          theme: ThemeData(
            useMaterial3: true,
            colorSchemeSeed: AppConfig.seedColor,
          ),
          home: HomeScreen(controller: controller),
        );
      },
    );
  }
}
