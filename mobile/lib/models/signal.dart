class TradingSignal {
  TradingSignal({required this.symbol, required this.direction, required this.confidence, required this.rationale, required this.generatedAt});

  final String symbol;
  final String direction;
  final double confidence;
  final String rationale;
  final DateTime generatedAt;

  factory TradingSignal.fromJson(Map<String, dynamic> json) {
    return TradingSignal(
      symbol: json['symbol'] as String,
      direction: json['direction'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      rationale: json['rationale'] as String,
      generatedAt: DateTime.parse(json['generated_at'] as String),
    );
  }
}
