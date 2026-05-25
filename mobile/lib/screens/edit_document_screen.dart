import 'package:flutter/material.dart';

import '../services/document_service.dart';

class EditDocumentScreen extends StatefulWidget {
  final String documentId;
  final Map<String, dynamic> extractedFields;
  final String rawText;

  const EditDocumentScreen({
    super.key,
    required this.documentId,
    required this.extractedFields,
    required this.rawText,
  });

  @override
  State<EditDocumentScreen> createState() => _EditDocumentScreenState();
}

class _EditDocumentScreenState extends State<EditDocumentScreen> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _dateCtrl;
  late TextEditingController _amountCtrl;
  late TextEditingController _vatCtrl;
  late TextEditingController _supplierCtrl;
  String _category = 'achat';
  bool _isValidating = false;

  final DocumentService _docService = DocumentService();

  @override
  void initState() {
    super.initState();
    _dateCtrl = TextEditingController(text: widget.extractedFields['date'] ?? '');
    _amountCtrl = TextEditingController(
        text: widget.extractedFields['amount_ttc']?.toString() ?? '');
    _vatCtrl = TextEditingController(
        text: widget.extractedFields['vat']?.toString() ?? '');
    _supplierCtrl = TextEditingController(
        text: widget.extractedFields['supplier'] ?? '');
    _category = widget.extractedFields['category'] ?? 'achat';
  }

  @override
  void dispose() {
    _dateCtrl.dispose();
    _amountCtrl.dispose();
    _vatCtrl.dispose();
    _supplierCtrl.dispose();
    super.dispose();
  }

  Future<void> _validate() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _isValidating = true);

    try {
      await _docService.validateDocument(widget.documentId, {
        'validated_date': _dateCtrl.text,
        'validated_amount': _amountCtrl.text,
        'validated_vat': _vatCtrl.text,
        'validated_supplier': _supplierCtrl.text,
        'validated_category': _category,
      });
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Document validé et écriture comptable créée')),
      );
      Navigator.pop(context);
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Erreur: $e')),
      );
    } finally {
      if (mounted) setState(() => _isValidating = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Valider le document')),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            if (widget.rawText.isNotEmpty) ...[
              const Text('Texte extrait :',
                  style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 4),
              Container(
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.grey[100],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(widget.rawText, style: const TextStyle(fontSize: 12)),
              ),
              const SizedBox(height: 16),
            ],
            TextFormField(
              controller: _dateCtrl,
              decoration: const InputDecoration(labelText: 'Date (JJ/MM/AAAA)'),
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _amountCtrl,
              decoration: const InputDecoration(labelText: 'Montant TTC'),
              keyboardType: TextInputType.number,
              validator: (v) => v?.isEmpty == true ? 'Requis' : null,
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _vatCtrl,
              decoration: const InputDecoration(labelText: 'TVA'),
              keyboardType: TextInputType.number,
            ),
            const SizedBox(height: 12),
            TextFormField(
              controller: _supplierCtrl,
              decoration: const InputDecoration(labelText: 'Fournisseur'),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<String>(
              initialValue: _category,
              decoration: const InputDecoration(labelText: 'Catégorie'),
              items: const [
                DropdownMenuItem(value: 'achat', child: Text('Achat')),
                DropdownMenuItem(value: 'vente', child: Text('Vente')),
                DropdownMenuItem(value: 'cotisation', child: Text('Cotisation')),
                DropdownMenuItem(value: 'don', child: Text('Don')),
              ],
              onChanged: (v) => setState(() => _category = v ?? 'achat'),
            ),
            const SizedBox(height: 24),
            FilledButton(
              onPressed: _isValidating ? null : _validate,
              child: _isValidating
                  ? const CircularProgressIndicator()
                  : const Text('Valider'),
            ),
          ],
        ),
      ),
    );
  }
}
