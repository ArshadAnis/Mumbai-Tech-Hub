import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../core/constants.dart';

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(baseUrl: apiBaseUrl));
  dio.interceptors.add(InterceptorsWrapper(
    onRequest: (options, handler) {
      options.headers['X-App-Disclaimer'] = 'Not financial advice. Trading involves risk.';
      handler.next(options);
    },
  ));
  return dio;
});
