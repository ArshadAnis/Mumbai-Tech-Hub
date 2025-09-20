import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});
  static const routeName = '/settings';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: const [
          ListTile(
            title: Text('Theme'),
            subtitle: Text('Follow system'),
          ),
          ListTile(
            title: Text('Notifications'),
            subtitle: Text('Price alerts via push when available.'),
          ),
          ListTile(
            title: Text('Data Privacy'),
            subtitle: Text('Export or delete data from profile.'),
          ),
          Padding(
            padding: EdgeInsets.all(16),
            child: Text('Money Trader does not execute trades. Signals are educational only.'),
          ),
        ],
      ),
    );
  }
}
