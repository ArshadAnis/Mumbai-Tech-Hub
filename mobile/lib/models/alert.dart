class PriceAlert {
  PriceAlert({required this.id, required this.symbol, required this.triggerPrice, required this.direction});

  final int id;
  final String symbol;
  final double triggerPrice;
  final String direction;

  factory PriceAlert.fromJson(Map<String, dynamic> json) {
    return PriceAlert(
      id: json['id'] as int,
      symbol: json['symbol'] as String,
      triggerPrice: (json['trigger_price'] as num).toDouble(),
      direction: json['direction'] as String,
    );
  }
}
