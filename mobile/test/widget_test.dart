import 'package:flutter_test/flutter_test.dart';

import 'package:kontlab/main.dart';

void main() {
  testWidgets('App renders login screen', (WidgetTester tester) async {
    await tester.pumpWidget(const KontlabApp());
    await tester.pumpAndSettle();
    expect(find.text('Kontlab'), findsOneWidget);
    expect(find.text('Se connecter'), findsOneWidget);
  });
}
