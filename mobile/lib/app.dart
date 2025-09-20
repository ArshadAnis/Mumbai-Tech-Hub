import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme.dart';
import 'features/auth/onboarding_screen.dart';
import 'features/home/dashboard_screen.dart';
import 'features/settings/settings_screen.dart';

final navigationIndexProvider = StateProvider<int>((ref) => 0);

class MoneyTraderApp extends ConsumerWidget {
  const MoneyTraderApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MaterialApp(
      title: 'Money Trader',
      theme: buildLightTheme(),
      darkTheme: buildDarkTheme(),
      themeMode: ThemeMode.system,
      home: const OnboardingScreen(),
      routes: {
        DashboardScreen.routeName: (_) => const DashboardScreen(),
        SettingsScreen.routeName: (_) => const SettingsScreen(),
      },
    );
  }
}
