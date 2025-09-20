import 'dart:convert';

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import '../core/constants.dart';

class PriceStreamService {
  WebSocketChannel? _channel;

  Stream<Map<String, dynamic>> connect(List<String> symbols) {
    final uri = Uri.parse('$wsBaseUrl/ws/price?symbols=${symbols.join(',')}');
    _channel = WebSocketChannel.connect(uri);
    return _channel!.stream.map((event) => Map<String, dynamic>.from(jsonDecode(event)));
  }

  void dispose() {
    _channel?.sink.close();
  }
}

final priceStreamProvider = Provider<PriceStreamService>((ref) {
  final service = PriceStreamService();
  ref.onDispose(service.dispose);
  return service;
});
