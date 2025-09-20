import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../models/alert.dart';
import '../../services/api_service.dart';

final alertsProvider = FutureProvider<List<PriceAlert>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/alerts');
  return (response.data as List).map((json) => PriceAlert.fromJson(Map<String, dynamic>.from(json))).toList();
});

class AlertsScreen extends ConsumerWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final alerts = ref.watch(alertsProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('Alerts')),
      body: alerts.when(
        data: (items) => ListView(
          children: [
            for (final alert in items)
              ListTile(
                title: Text('${alert.symbol} @ ${alert.triggerPrice.toStringAsFixed(2)}'),
                subtitle: Text('Direction: ${alert.direction}'),
              ),
          ],
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(child: Text('Failed to load alerts: $error')),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showCreateAlertDialog(context, ref),
        child: const Icon(Icons.add_alert),
      ),
    );
  }

  Future<void> _showCreateAlertDialog(BuildContext context, WidgetRef ref) async {
    final formKey = GlobalKey<FormState>();
    final symbolController = TextEditingController(text: 'BTCUSDT');
    final priceController = TextEditingController(text: '30000');
    String direction = 'above';

    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Create Alert'),
        content: Form(
          key: formKey,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextFormField(controller: symbolController, decoration: const InputDecoration(labelText: 'Symbol')),
              TextFormField(controller: priceController, decoration: const InputDecoration(labelText: 'Trigger Price')),
              DropdownButtonFormField<String>(
                value: direction,
                items: const [
                  DropdownMenuItem(value: 'above', child: Text('Above')),
                  DropdownMenuItem(value: 'below', child: Text('Below')),
                ],
                onChanged: (value) => direction = value ?? 'above',
              ),
            ],
          ),
        ),
        actions: [
          TextButton(onPressed: () => Navigator.of(context).pop(), child: const Text('Cancel')),
          ElevatedButton(
            onPressed: () async {
              final dio = ref.read(dioProvider);
              await dio.post('/alerts', data: {
                'symbol': symbolController.text,
                'trigger_price': double.tryParse(priceController.text) ?? 0,
                'direction': direction,
              });
              Navigator.of(context).pop();
              ref.refresh(alertsProvider);
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }
}
