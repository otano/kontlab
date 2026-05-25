import 'package:flutter/material.dart';

import '../services/document_service.dart';

class DocumentDetailScreen extends StatefulWidget {
  final String documentId;

  const DocumentDetailScreen({super.key, required this.documentId});

  @override
  State<DocumentDetailScreen> createState() => _DocumentDetailScreenState();
}

class _DocumentDetailScreenState extends State<DocumentDetailScreen> {
  final DocumentService _docService = DocumentService();
  Map<String, dynamic>? _doc;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final doc = await _docService.getDocument(widget.documentId);
      if (mounted) setState(() => _doc = doc);
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erreur: $e')),
        );
      }
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Détail du document')),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _doc == null
              ? const Center(child: Text('Document introuvable'))
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: [
                    _field('Statut', _doc!['status']?.toString() ?? ''),
                    _field('Catégorie', _doc!['category']?.toString() ?? ''),
                    const SizedBox(height: 16),
                    const Text('Champs extraits',
                        style: TextStyle(fontWeight: FontWeight.bold)),
                    _field('Date', _doc!['extracted_date']?.toString() ?? ''),
                    _field('Montant', _doc!['extracted_amount']?.toString() ?? ''),
                    _field('TVA', _doc!['extracted_vat']?.toString() ?? ''),
                    _field('Fournisseur', _doc!['extracted_supplier']?.toString() ?? ''),
                    const SizedBox(height: 16),
                    const Text('Texte brut',
                        style: TextStyle(fontWeight: FontWeight.bold)),
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.grey[100],
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(_doc!['raw_text'] ?? ''),
                    ),
                  ],
                ),
    );
  }

  Widget _field(String label, String value) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          SizedBox(width: 120, child: Text('$label :',
              style: const TextStyle(fontWeight: FontWeight.w500))),
          Expanded(child: Text(value)),
        ],
      ),
    );
  }
}
