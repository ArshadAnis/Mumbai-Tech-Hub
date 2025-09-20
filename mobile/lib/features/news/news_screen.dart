import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../services/api_service.dart';

final newsProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/news');
  return List<Map<String, dynamic>>.from(response.data as List);
});

final calendarProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  final dio = ref.read(dioProvider);
  final response = await dio.get('/calendar');
  return List<Map<String, dynamic>>.from(response.data as List);
});

class NewsScreen extends ConsumerWidget {
  const NewsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final news = ref.watch(newsProvider);
    final calendar = ref.watch(calendarProvider);
    return Scaffold(
      appBar: AppBar(title: const Text('News & Calendar')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text('Latest News', style: TextStyle(fontWeight: FontWeight.bold)),
          news.when(
            data: (items) => Column(
              children: [
                for (final item in items)
                  ListTile(
                    title: Text(item['title'] as String),
                    subtitle: Text(item['summary'] as String),
                  ),
              ],
            ),
            loading: () => const Padding(padding: EdgeInsets.all(24), child: CircularProgressIndicator()),
            error: (error, stack) => Text('Failed to load news: $error'),
          ),
          const SizedBox(height: 24),
          const Text('Economic Calendar', style: TextStyle(fontWeight: FontWeight.bold)),
          calendar.when(
            data: (items) => Column(
              children: [
                for (final item in items)
                  ListTile(
                    title: Text(item['event'] as String),
                    subtitle: Text('Impact: ${item['impact']} at ${item['time']}'),
                  ),
              ],
            ),
            loading: () => const Padding(padding: EdgeInsets.all(24), child: CircularProgressIndicator()),
            error: (error, stack) => Text('Failed to load calendar: $error'),
          ),
        ],
      ),
    );
  }
}
