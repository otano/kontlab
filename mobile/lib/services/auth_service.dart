import 'api_service.dart';

class AuthService {
  Future<Map<String, dynamic>> login(String username, String password) async {
    final data = await ApiService.post('/auth/login/', body: {
      'username': username,
      'password': password,
    });
    await ApiService.saveToken(data['access']);
    await ApiService.saveRefreshToken(data['refresh']);
    return data;
  }

  Future<void> register(
      String username, String email, String password) async {
    await ApiService.post('/auth/register/', body: {
      'username': username,
      'email': email,
      'password': password,
    });
  }

  Future<void> logout() async {
    await ApiService.clearTokens();
  }

  Future<bool> isLoggedIn() async {
    final token = await ApiService.getToken();
    return token != null;
  }
}
