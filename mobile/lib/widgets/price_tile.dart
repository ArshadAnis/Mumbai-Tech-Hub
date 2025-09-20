import 'package:flutter/material.dart';

class PriceTile extends StatelessWidget {
  const PriceTile({super.key, required this.symbol, required this.description});

  final String symbol;
  final String description;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(symbol),
        subtitle: Text(description),
        trailing: const Text('Live'),
      ),
    );
  }
}
