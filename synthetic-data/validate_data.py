"""
Synthetic Data Validation Script

Validates all generated evidence files and extraction JSONs against requirements.
"""

import os
import json
import sys
from typing import Dict, List, Set


def validate_file_existence() -> bool:
    """Check that all required files exist"""
    print("\n[1/9] Validating file existence...")

    expected_files = {
        'evidence/pdfs': [
            'financial_statement_techventures_2026q1.pdf',
            'contract_cryptoholdings_offshore.pdf',
            'bank_statement_chen_personal_202606.pdf',
            'corporate_filing_cryptoholdings.pdf',
            'invoice_pharma_001234.pdf',
            'email_screenshot_chen_rodriguez.pdf'
        ],
        'evidence/images': [
            'id_card_chen_marcus.png',
            'receipt_restaurant_meeting.jpg',
            'whiteboard_meeting_notes.jpg',
            'check_image_250k.png',
            'text_message_screenshot.png',
            'business_card_kim_david.jpg'
        ],
        'evidence/audio': [
            'phone_call_chen_rodriguez_20260315.wav',
            'voicemail_kim_to_martinez_20260420.wav',
            'meeting_recording_techventures_20260522.wav',
            'phone_call_morgan_parker_20260610.wav'
        ],
        'evidence/csv': [
            'transactions_techventures_2026_q2.csv',
            'phone_records_chen_202601_202606.csv',
            'pharma_transactions_202603_202607.csv'
        ]
    }

    all_exist = True
    total_count = 0

    for directory, files in expected_files.items():
        for filename in files:
            filepath = os.path.join(directory, filename)
            if os.path.exists(filepath):
                total_count += 1
            else:
                print(f"  ✗ Missing: {filepath}")
                all_exist = False

    # Check extraction JSONs
    extraction_dir = 'prepared-extractions'
    expected_json_count = 19
    json_count = 0
    if os.path.exists(extraction_dir):
        json_files = [f for f in os.listdir(extraction_dir) if f.endswith('.json')]
        json_count = len(json_files)

    if json_count < expected_json_count:
        print(f"  ✗ Expected {expected_json_count} JSON files, found {json_count}")
        all_exist = False

    if all_exist:
        print(f"  ✓ All files exist: {total_count} evidence files, {json_count} extraction JSONs")

    return all_exist


def validate_file_sizes() -> bool:
    """Check that files are within size constraints"""
    print("\n[2/9] Validating file sizes...")

    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50 MB

    total_size = 0
    oversized_files = []

    for root, dirs, files in os.walk('evidence'):
        for filename in files:
            filepath = os.path.join(root, filename)
            size = os.path.getsize(filepath)
            total_size += size

            if size > MAX_FILE_SIZE:
                oversized_files.append((filepath, size))

    if oversized_files:
        print(f"  ✗ Files exceeding 5 MB:")
        for filepath, size in oversized_files:
            print(f"    {filepath}: {size / 1024 / 1024:.2f} MB")
        return False

    if total_size > MAX_TOTAL_SIZE:
        print(f"  ✗ Total evidence size exceeds 50 MB: {total_size / 1024 / 1024:.2f} MB")
        return False

    print(f"  ✓ All files within size limits (total: {total_size / 1024 / 1024:.2f} MB)")
    return True


def validate_json_schema() -> bool:
    """Validate JSON structure and required fields"""
    print("\n[3/9] Validating JSON schema...")

    required_fields = ['evidence_id', 'evidence_filename', 'extraction_type',
                      'extraction_timestamp', 'raw_text', 'entities',
                      'relationships', 'transactions', 'metadata']

    valid_extraction_types = ['ocr', 'transcription', 'csv_parse']
    valid_entity_types = ['PERSON', 'ORGANIZATION', 'PHONE', 'EMAIL',
                         'BANK_ACCOUNT', 'CRYPTO_WALLET', 'LOCATION', 'IP_ADDRESS']
    valid_relationship_types = ['OWNS', 'CONTROLS', 'CALLS', 'ASSOCIATED_WITH',
                               'TRANSFERRED_FUNDS', 'LOCATED_AT']

    all_valid = True
    json_dir = 'prepared-extractions'

    if not os.path.exists(json_dir):
        print(f"  ✗ Directory not found: {json_dir}")
        return False

    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for json_file in json_files:
        filepath = os.path.join(json_dir, json_file)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check required fields
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields:
                print(f"  ✗ {json_file}: Missing fields: {missing_fields}")
                all_valid = False
                continue

            # Validate extraction type
            if data['extraction_type'] not in valid_extraction_types:
                print(f"  ✗ {json_file}: Invalid extraction_type: {data['extraction_type']}")
                all_valid = False

            # Validate entity types
            for entity in data['entities']:
                if entity['type'] not in valid_entity_types:
                    print(f"  ✗ {json_file}: Invalid entity type: {entity['type']}")
                    all_valid = False

                # Check confidence score
                if not (0.0 <= entity.get('confidence', 0) <= 1.0):
                    print(f"  ✗ {json_file}: Invalid confidence score: {entity.get('confidence')}")
                    all_valid = False

            # Validate relationship types
            for rel in data['relationships']:
                if rel['type'] not in valid_relationship_types:
                    print(f"  ✗ {json_file}: Invalid relationship type: {rel['type']}")
                    all_valid = False

        except json.JSONDecodeError as e:
            print(f"  ✗ {json_file}: Invalid JSON: {e}")
            all_valid = False
        except Exception as e:
            print(f"  ✗ {json_file}: Error: {e}")
            all_valid = False

    if all_valid:
        print(f"  ✓ All {len(json_files)} JSON files have valid schema")

    return all_valid


def validate_entity_consistency() -> bool:
    """Check for cross-file entity consistency"""
    print("\n[4/9] Validating entity consistency...")

    entity_occurrences = {}
    json_dir = 'prepared-extractions'

    if not os.path.exists(json_dir):
        return False

    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for json_file in json_files:
        filepath = os.path.join(json_dir, json_file)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entity in data['entities']:
                entity_id = entity['entity_id']
                if entity_id not in entity_occurrences:
                    entity_occurrences[entity_id] = []
                entity_occurrences[entity_id].append(json_file)

        except Exception:
            pass

    # Check for entities appearing in multiple files
    multi_file_entities = {eid: files for eid, files in entity_occurrences.items() if len(files) > 1}

    if not multi_file_entities:
        print(f"  ✗ No entities found in multiple files (cross-file correlation required)")
        return False

    print(f"  ✓ Found {len(multi_file_entities)} entities appearing in multiple files")
    print(f"    Examples:")
    for i, (entity_id, files) in enumerate(list(multi_file_entities.items())[:5]):
        print(f"      {entity_id}: {len(files)} files")

    return True


def validate_entity_counts() -> bool:
    """Validate minimum entity counts"""
    print("\n[5/9] Validating entity counts...")

    entity_types_count = {
        'PERSON': 0,
        'ORGANIZATION': 0,
        'BANK_ACCOUNT': 0,
        'CRYPTO_WALLET': 0,
        'LOCATION': 0
    }

    unique_entities = set()
    json_dir = 'prepared-extractions'

    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue

        filepath = os.path.join(json_dir, json_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entity in data['entities']:
                entity_id = entity['entity_id']
                entity_type = entity['type']
                unique_entities.add(entity_id)

                if entity_type in entity_types_count:
                    entity_types_count[entity_type] += 1
        except Exception:
            pass

    # Deduplicate counts
    entity_ids_by_type = {t: set() for t in entity_types_count.keys()}

    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue
        filepath = os.path.join(json_dir, json_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for entity in data['entities']:
                entity_type = entity['type']
                if entity_type in entity_ids_by_type:
                    entity_ids_by_type[entity_type].add(entity['entity_id'])
        except Exception:
            pass

    requirements = {
        'PERSON': 12,
        'ORGANIZATION': 8,
        'LOCATION': 10
    }

    total_accounts = len(entity_ids_by_type['BANK_ACCOUNT']) + len(entity_ids_by_type['CRYPTO_WALLET'])

    all_met = True
    for entity_type, required_count in requirements.items():
        actual_count = len(entity_ids_by_type[entity_type])
        status = "✓" if actual_count >= required_count else "✗"
        print(f"  {status} {entity_type}: {actual_count} (required: {required_count})")
        if actual_count < required_count:
            all_met = False

    status = "✓" if total_accounts >= 23 else "✗"
    print(f"  {status} ACCOUNTS (BANK + CRYPTO): {total_accounts} (required: 23)")
    if total_accounts < 23:
        all_met = False

    return all_met


def validate_transaction_patterns() -> bool:
    """Validate required transaction patterns"""
    print("\n[6/9] Validating transaction patterns...")

    all_transactions = []
    json_dir = 'prepared-extractions'

    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue

        filepath = os.path.join(json_dir, json_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            all_transactions.extend(data.get('transactions', []))
        except Exception:
            pass

    # Check for transaction cycle
    cycle_found = False
    accounts = set()
    for txn in all_transactions:
        accounts.add(txn.get('sender', ''))
        accounts.add(txn.get('receiver', ''))

    # Simple check: look for ***1234 appearing as both sender and receiver
    chen_account = '***1234'
    chen_as_sender = any(txn.get('sender') == chen_account for txn in all_transactions)
    chen_as_receiver = any(txn.get('receiver') == chen_account for txn in all_transactions)
    cycle_found = chen_as_sender and chen_as_receiver

    # Count repeated transfers (same sender-receiver pairs)
    sender_receiver_pairs = {}
    for txn in all_transactions:
        pair = (txn.get('sender'), txn.get('receiver'))
        sender_receiver_pairs[pair] = sender_receiver_pairs.get(pair, 0) + 1

    repeated_count = sum(1 for count in sender_receiver_pairs.values() if count >= 10)

    # Count high-value transactions
    high_value_count = sum(1 for txn in all_transactions if txn.get('amount', 0) > 100000)

    # Count structuring transactions
    structuring_count = sum(1 for txn in all_transactions if 9000 <= txn.get('amount', 0) < 10000)

    print(f"  {'✓' if cycle_found else '✗'} Transaction cycle detected: {cycle_found}")
    print(f"  {'✓' if repeated_count >= 1 else '✗'} Repeated transfers (>= 10 txns same pair): {repeated_count}")
    print(f"  {'✓' if high_value_count >= 5 else '✗'} High-value transactions (> $100K): {high_value_count} (required: 5)")
    print(f"  {'✓' if structuring_count >= 15 else '✗'} Structuring transactions ($9K-$10K): {structuring_count} (required: 15)")

    return cycle_found and repeated_count >= 1 and high_value_count >= 5 and structuring_count >= 15


def validate_relationships() -> bool:
    """Validate relationship integrity"""
    print("\n[7/9] Validating relationship integrity...")

    all_entity_ids = set()
    all_relationships = []
    json_dir = 'prepared-extractions'

    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue

        filepath = os.path.join(json_dir, json_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for entity in data['entities']:
                all_entity_ids.add(entity['entity_id'])

            all_relationships.extend(data['relationships'])
        except Exception:
            pass

    # Check that relationship entity IDs reference defined entities
    invalid_refs = 0
    for rel in all_relationships:
        if rel['source_entity_id'] not in all_entity_ids:
            invalid_refs += 1
        if rel['target_entity_id'] not in all_entity_ids:
            invalid_refs += 1

    # Count relationship types
    rel_types = set(rel['type'] for rel in all_relationships)

    if invalid_refs > 0:
        print(f"  ✗ {invalid_refs} relationships reference undefined entities")
        return False

    print(f"  ✓ All relationship references are valid")
    print(f"  ✓ Found {len(rel_types)} different relationship types: {', '.join(sorted(rel_types))}")

    return True


def validate_timeline() -> bool:
    """Validate timestamps are within scenario timeline"""
    print("\n[8/9] Validating timeline...")

    from datetime import datetime

    min_date = datetime(2026, 1, 1)
    max_date = datetime(2026, 8, 28)

    invalid_timestamps = []
    json_dir = 'prepared-extractions'

    for json_file in os.listdir(json_dir):
        if not json_file.endswith('.json'):
            continue

        filepath = os.path.join(json_dir, json_file)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            for txn in data.get('transactions', []):
                if 'timestamp' in txn:
                    try:
                        ts = datetime.fromisoformat(txn['timestamp'].replace('Z', '+00:00'))
                        if not (min_date <= ts <= max_date):
                            invalid_timestamps.append((json_file, txn['timestamp']))
                    except Exception:
                        pass
        except Exception:
            pass

    if invalid_timestamps:
        print(f"  ✗ {len(invalid_timestamps)} timestamps outside timeline")
        return False

    print(f"  ✓ All timestamps within scenario timeline (2026-01-01 to 2026-08-28)")
    return True


def validate_evidence_json_matching() -> bool:
    """Validate evidence files have matching JSONs"""
    print("\n[9/9] Validating evidence-JSON matching...")

    evidence_files = []
    for root, dirs, files in os.walk('evidence'):
        for filename in files:
            evidence_files.append(filename)

    json_dir = 'prepared-extractions'
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    # Check each evidence file has a JSON
    missing_jsons = []
    for evidence_file in evidence_files:
        base_name = os.path.splitext(evidence_file)[0]
        json_name = f"{base_name}.json"
        if json_name not in json_files:
            missing_jsons.append(evidence_file)

    if missing_jsons:
        print(f"  ✗ Evidence files without extraction JSON:")
        for filename in missing_jsons[:5]:
            print(f"    {filename}")
        return False

    print(f"  ✓ All {len(evidence_files)} evidence files have extraction JSONs")
    return True


def main():
    """Run all validation checks"""
    print("=" * 60)
    print("OmniGraph OSINT - Synthetic Data Validation")
    print("=" * 60)

    checks = [
        validate_file_existence,
        validate_file_sizes,
        validate_json_schema,
        validate_entity_consistency,
        validate_entity_counts,
        validate_transaction_patterns,
        validate_relationships,
        validate_timeline,
        validate_evidence_json_matching
    ]

    passed = 0
    failed = 0

    for check in checks:
        try:
            if check():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ Check failed with error: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Validation Results: {passed}/{len(checks)} checks passed")
    print("=" * 60)

    if failed == 0:
        print("✅ All validation checks passed!")
        return 0
    else:
        print(f"❌ {failed} validation check(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
