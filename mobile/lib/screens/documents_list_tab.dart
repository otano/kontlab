import 'package:flutter/material.dart';

import '../services/document_service.dart';
import 'document_detail_screen.dart';

class DocumentsListTab extends StatefulWidget {
  const DocumentsListTab({super.key});

  @override
  State<DocumentsListTab> createState() => _DocumentsListTabState();
}

class _DocumentsListTabState extends State<DocumentsListTab> {
  final DocumentService _docService = DocumentService();
  List<dynamic> _documents = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() => _isLoading = true);
    try {
      final docs = await _docService.listDocuments();
      if (mounted) setState(() => _documents = docs);
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
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_documents.isEmpty) {
      return const Center(child: Text('Aucun document'));
    }
    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        itemCount: _documents.length,
        itemBuilder: (context, i) {
          final doc = _documents[i] as Map<String, dynamic>;
          return ListTile(
            leading: Icon(
              doc['status'] == 'validated'
                  ? Icons.check_circle
                  : Icons.hourglass_empty,
              color: doc['status'] == 'validated' ? Colors.green : Colors.orange,
            ),
            title: Text('Document ${doc['id'].toString().substring(0, 8)}…'),
            subtitle: Text(doc['category'] ?? ''),
            trailing: Text(doc['status'] == 'validated' ? 'Validé' : 'En attente'),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (_) => DocumentDetailScreen(documentId: doc['id']),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
