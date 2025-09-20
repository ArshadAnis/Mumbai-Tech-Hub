import 'package:flutter/material.dart';

import '../home/dashboard_screen.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Spacer(),
              Text('Money Trader', style: Theme.of(context).textTheme.displayMedium),
              const SizedBox(height: 16),
              const Text('Signals and alerts for crypto and forex traders. Not financial advice. Trading involves risk.'),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () => Navigator.of(context).pushReplacementNamed(DashboardScreen.routeName),
                child: const Text('Get Started'),
              ),
              TextButton(
                onPressed: () {},
                child: const Text('View Terms & Privacy'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
