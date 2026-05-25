import 'dart:io';

import 'api_service.dart';

class DocumentService {
  Future<Map<String, dynamic>> uploadImage(
      File image, String category) async {
    final result = await ApiService.uploadFile(
      '/documents/upload/',
      image,
      'image',
      fields: {'category': category},
    );
    return result as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> validateDocument(
      String id, Map<String, dynamic> fields) async {
    final result = await ApiService.put('/documents/$id/validate/', body: fields);
    return result as Map<String, dynamic>;
  }

  Future<List<dynamic>> listDocuments() async {
    final result = await ApiService.get('/documents/');
    return result as List<dynamic>;
  }

  Future<Map<String, dynamic>> getDocument(String id) async {
    final result = await ApiService.get('/documents/$id/');
    return result as Map<String, dynamic>;
  }
}
