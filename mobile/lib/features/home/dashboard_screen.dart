import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/constants.dart';
import '../../services/api_service.dart';
import '../../widgets/price_tile.dart';
import '../alerts/alerts_screen.dart';
import '../portfolio/portfolio_screen.dart';
import '../signals/signals_screen.dart';
import '../news/news_screen.dart';
import '../settings/settings_screen.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});
  static const routeName = '/dashboard';

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  late Future<List<Map<String, dynamic>>> _symbolsFuture;

  @override
  void initState() {
    super.initState();
    _symbolsFuture = _fetchSymbols();
  }

  Future<List<Map<String, dynamic>>> _fetchSymbols() async {
    final dio = ref.read(dioProvider);
    final response = await dio.get('/market/symbols');
    return List<Map<String, dynamic>>.from(response.data as List);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Money Trader'),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications),
            onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const AlertsScreen())),
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => Navigator.of(context).pushNamed(SettingsScreen.routeName),
          ),
        ],
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _symbolsFuture,
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snapshot.data!;
          return ListView(
            padding: const EdgeInsets.all(16),
            children: [
              const Text('Top Markets', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              for (final symbol in data.take(6))
                PriceTile(symbol: symbol['symbol'] as String, description: symbol['description'] as String),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const SignalsScreen())),
                child: const Text('View AI Signals'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const PortfolioScreen())),
                child: const Text('Manage Portfolio'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.of(context).push(MaterialPageRoute(builder: (_) => const NewsScreen())),
                child: const Text('News & Calendar'),
              ),
              const SizedBox(height: 24),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text('Upgrade to Pro', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      SizedBox(height: 8),
                      Text('Unlock more alerts, signals, and remove ads with Pro or Elite tiers.'),
                    ],
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}
