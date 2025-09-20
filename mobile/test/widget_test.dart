import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:money_trader/app.dart';

void main() {
  testWidgets('Onboarding renders disclaimer', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: MoneyTraderApp()));
    expect(find.textContaining('Not financial advice'), findsOneWidget);
  });
}
