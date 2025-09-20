import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/signal.dart';
import '../../services/api_service.dart';

final signalsProvider = FutureProvider<List<TradingSignal>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/signals');
  return (response.data as List).map((json) => TradingSignal.fromJson(Map<String, dynamic>.from(json))).toList();
});

class SignalsScreen extends ConsumerWidget {
  const SignalsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final signals = ref.watch(signalsProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('AI Signals')),
      body: signals.when(
        data: (items) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            for (final signal in items)
              Card(
                child: ListTile(
                  title: Text(signal.symbol),
                  subtitle: Text(signal.rationale),
                  trailing: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(signal.direction.toUpperCase()),
                      Text('${(signal.confidence * 100).toStringAsFixed(0)}%'),
                    ],
                  ),
                ),
              ),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Failed to load signals: $error')),
      ),
    );
  }
}
