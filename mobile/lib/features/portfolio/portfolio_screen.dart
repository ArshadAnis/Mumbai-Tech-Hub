import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../services/api_service.dart';

final portfolioProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/portfolio');
  return List<Map<String, dynamic>>.from(response.data as List);
});

class PortfolioScreen extends ConsumerWidget {
  const PortfolioScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final positions = ref.watch(portfolioProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Portfolio')),
      body: positions.when(
        data: (items) => ListView(
          padding: const EdgeInsets.all(16),
          children: [
            for (final position in items)
              Card(
                child: ListTile(
                  title: Text(position['symbol'] as String),
                  subtitle: Text('Qty: ${position['quantity']} @ ${position['entry_price']}'),
                ),
              ),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Unable to load portfolio: $error')),
      ),
    );
  }
}
