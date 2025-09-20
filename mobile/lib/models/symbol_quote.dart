class SymbolQuote {
  SymbolQuote({required this.symbol, required this.price, required this.timestamp});

  final String symbol;
  final double price;
  final DateTime timestamp;

  factory SymbolQuote.fromJson(Map<String, dynamic> json) {
    return SymbolQuote(
      symbol: json['symbol'] as String,
      price: (json['price'] as num).toDouble(),
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }
}
