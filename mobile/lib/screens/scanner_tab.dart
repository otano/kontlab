import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_cropper/image_cropper.dart';
import 'package:image_picker/image_picker.dart';

import '../services/document_service.dart';
import 'edit_document_screen.dart';

class ScannerTab extends StatefulWidget {
  const ScannerTab({super.key});

  @override
  State<ScannerTab> createState() => _ScannerTabState();
}

class _ScannerTabState extends State<ScannerTab> {
  final DocumentService _docService = DocumentService();
  bool _isUploading = false;

  Future<void> _pickAndUpload() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.camera, maxWidth: 2048);
    if (picked == null) return;

    File image = File(picked.path);
    final cropped = await ImageCropper().cropImage(
      sourcePath: picked.path,
      maxWidth: 2048,
      maxHeight: 2048,
    );
    if (cropped != null) image = File(cropped.path);

    setState(() => _isUploading = true);

    try {
      final result = await _docService.uploadImage(image, 'achat');
      if (!mounted) return;
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => EditDocumentScreen(
            documentId: result['id'],
            extractedFields: result['extracted_fields'] as Map<String, dynamic>? ?? {},
            rawText: result['raw_text'] as String? ?? '',
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e')),
      );
    } finally {
      if (mounted) setState(() => _isUploading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: _isUploading
          ? const Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                CircularProgressIndicator(),
                SizedBox(height: 16),
                Text('Analyse en cours…'),
              ],
            )
          : Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.camera_alt, size: 80, color: Colors.grey),
                const SizedBox(height: 16),
                const Text('Scannez un ticket ou une facture'),
                const SizedBox(height: 24),
                FilledButton.icon(
                  onPressed: _pickAndUpload,
                  icon: const Icon(Icons.camera),
                  label: const Text('Prendre une photo'),
                ),
              ],
            ),
    );
  }
}
