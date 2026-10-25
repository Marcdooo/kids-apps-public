import 'dart:math';

import 'package:flutter/material.dart';

import 'strings.dart';

/// Asks a simple addition question so young children can't wander into the
/// grown-ups area. Returns true only if the right answer was tapped.
Future<bool> showParentGate(BuildContext context, Strings strings) async {
  final random = Random();
  final a = 11 + random.nextInt(18); // 11..28
  final b = 3 + random.nextInt(7); // 3..9
  final answer = a + b;

  final options = <int>{answer};
  while (options.length < 4) {
    final candidate = answer + random.nextInt(11) - 5; // answer-5 .. answer+5
    if (candidate > 0) options.add(candidate);
  }
  final shuffled = options.toList()..shuffle(random);

  final passed = await showDialog<bool>(
    context: context,
    builder: (dialogContext) => AlertDialog(
      title: Text(strings.t('gate_title')),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(strings.t('gate_prompt')),
          const SizedBox(height: 16),
          Text(
            strings.t('gate_question', {'a': '$a', 'b': '$b'}),
            style: Theme.of(dialogContext).textTheme.headlineMedium,
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 12,
            runSpacing: 12,
            alignment: WrapAlignment.center,
            children: [
              for (final option in shuffled)
                SizedBox(
                  width: 72,
                  height: 56,
                  child: OutlinedButton(
                    onPressed: () =>
                        Navigator.of(dialogContext).pop(option == answer),
                    child: Text('$option'),
                  ),
                ),
            ],
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(dialogContext).pop(false),
          child: Text(strings.t('cancel')),
        ),
      ],
    ),
  );
  return passed ?? false;
}
