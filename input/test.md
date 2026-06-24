# test

> Авто-конвертация из `test.docx`. Проверьте таблицы и диаграммы; при расхождениях сверяйтесь с исходным docx.

Процедура наличия справки для налоговой через сервисы AdInsure

Проверить наличие справок по договору за выбранный отчетный год:

| API | {{SERVER_URI}}/api/entity-infrastructure/shared/datasource/execute?configurationCodeName=GetAccountingCertificateDataSource |
| --- | --- |
| METHOD | POST |
| BODY №1 | { "data": { "criteria": { "contractNumber": "82500-99000150", "accountingYear": "2025" } } } |
| RESPONSE EXAMPLE №1 (certificate found) | { "data": [ { "resultData": { "accountingCertificateNumber": "СПРАВКА-20250000550", "accountingCertificateState": "Issued", "accountingCertificateSeqNumber": "0", "accountingCertificateStateDescription": "Подтверждена", "accountingCertificateConfigurationName":"AccountingCertificate", "originalDocumentNumber": "СПРАВКА-20250000550", "contractNumber": "82500-99000150", "contractCodeName": "AccumulatedLifeInsurancePolicy", "applicantFullName": "Воробьева Анастасия Кирилловна", "requestDate": "2025-09-02", "accountingYear": "2025", "correctionNumber": 0, "amountOfPremiumPaid": 199151.96, "certificateIssueDate": "2025-09-02", "incomeSource": "Интерфейс AdInsure", "taxCertificateFormat": "PDF", "hasAttachment": true, "transitionCommitor": "Administrator Administrator Administrator" } } ], "paging": { "numberOfResults": 1 } } |
| BODY №2 | { "data": { "criteria": { "contractNumber": "82500-99000151", "accountingYear": "2025" } } } |
| RESPONSE EXAMPLE №2 (certificate not found) | { "data": [], "paging": { "numberOfResults": 0 } } |
