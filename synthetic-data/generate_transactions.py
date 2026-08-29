"""
CSV Transaction Generation

Generates 3 CSV files using pandas:
1. TechVentures transactions (Q2 2026) - 80 transactions
2. Phone records (Jan-Jun 2026) - 150 call records
3. PharmaCorp transactions (Mar-Jul 2026) - 40 transactions
"""

import os
import pandas as pd
from datetime import datetime, timedelta
import random


RANDOM_SEED = 20260828


def generate_techventures_transactions(output_dir: str, scenario):
    """Generate transaction CSV for TechVentures Q2 2026 with patterns"""
    filename = os.path.join(output_dir, "transactions_techventures_2026_q2.csv")

    transactions = []

    # The main cycle transactions
    transactions.append({
        'date': '2026-02-15',
        'sender_account': '***1234',
        'receiver_account': '***9010',
        'amount': 300000.00,
        'currency': 'USD',
        'description': 'Investment capital'
    })

    transactions.append({
        'date': '2026-03-10',
        'sender_account': '***9010',
        'receiver_account': '***9012',
        'amount': 300000.00,
        'currency': 'USD',
        'description': 'Consulting services'
    })

    transactions.append({
        'date': '2026-04-22',
        'sender_account': '***9012',
        'receiver_account': '0x7a8b...',
        'amount': 280000.00,
        'currency': 'USD',
        'description': 'Advisory fees'
    })

    transactions.append({
        'date': '2026-05-30',
        'sender_account': '0x7a8b...',
        'receiver_account': '0x3c4d...',
        'amount': 270000.00,
        'currency': 'USD',
        'description': 'Service payment'
    })

    transactions.append({
        'date': '2026-07-15',
        'sender_account': '0x3c4d...',
        'receiver_account': '***1234',
        'amount': 260000.00,
        'currency': 'USD',
        'description': 'Crypto conversion'
    })

    # Repeated Chen -> Rodriguez transfers (structuring pattern)
    base_date = datetime(2026, 3, 1)
    for i in range(15):
        transactions.append({
            'date': (base_date + timedelta(days=i*6)).strftime('%Y-%m-%d'),
            'sender_account': '***1234',
            'receiver_account': '***2345',
            'amount': 9500.00,
            'currency': 'USD',
            'description': random.choice(['Bonus payment', 'Commission', 'Performance award'])
        })

    # More structuring transactions
    structuring_dates = ['2026-03-12', '2026-03-12', '2026-03-12', '2026-04-08', '2026-04-08',
                        '2026-04-08', '2026-04-08', '2026-05-14', '2026-05-14', '2026-05-14',
                        '2026-06-05', '2026-06-05', '2026-06-05', '2026-06-05']

    receivers = ['***3456', '***4567', '***5678', '***9012']
    amounts = [9000, 9200, 9500, 9700, 9850, 9900]

    for date in structuring_dates:
        transactions.append({
            'date': date,
            'sender_account': '***1234',
            'receiver_account': random.choice(receivers),
            'amount': random.choice(amounts),
            'currency': 'USD',
            'description': 'Business expense'
        })

    # High-value transactions
    high_value_txns = [
        ('2026-03-15', '***9010', '***9012', 250000.00, 'Large consulting payment'),
        ('2026-04-18', '***9012', '***1357', 200000.00, 'Advisory services'),
        ('2026-06-10', '***1357', '***2468', 180000.00, 'Service fees'),
        ('2026-07-01', '***2468', '***7777', 175000.00, 'Offshore transfer'),
    ]

    for date, sender, receiver, amount, desc in high_value_txns:
        transactions.append({
            'date': date,
            'sender_account': sender,
            'receiver_account': receiver,
            'amount': amount,
            'currency': 'USD',
            'description': desc
        })

    # Normal business transactions (fill to 80 total)
    normal_accounts = ['***5678', '***6789', '***7890', '***8901']
    normal_descriptions = ['Office supplies', 'Utilities', 'Software license', 'Travel expense',
                          'Marketing services', 'Legal fees', 'Insurance', 'Equipment']

    current_date = datetime(2026, 4, 1)
    while len(transactions) < 80:
        transactions.append({
            'date': current_date.strftime('%Y-%m-%d'),
        'sender_account': '***9010',
            'receiver_account': random.choice(normal_accounts),
            'amount': round(random.uniform(500, 5000), 2),
            'currency': 'USD',
            'description': random.choice(normal_descriptions)
        })
        current_date += timedelta(days=random.randint(1, 3))

    df = pd.DataFrame(transactions)
    df = df.sort_values('date').reset_index(drop=True)
    df.to_csv(filename, index=False)
    print(f"  ✓ Generated: {filename} ({len(df)} transactions)")


def generate_phone_records(output_dir: str, scenario):
    """Generate phone call records CSV"""
    filename = os.path.join(output_dir, "phone_records_chen_202601_202606.csv")

    records = []

    # Key relationships with high frequency
    call_patterns = [
        ('+1-415-555-0101', '+1-415-555-0102', 45),  # Chen -> Rodriguez
        ('+1-415-555-0101', '+1-415-555-0103', 23),  # Chen -> Kim
        ('+1-415-555-0103', '+1-415-555-0105', 15),  # Kim -> Martinez
        ('+1-415-555-0101', '+1-415-555-0107', 12),  # Chen -> Brown
        ('+1-415-555-0102', '+1-415-555-0104', 10),  # Rodriguez -> White
    ]

    base_date = datetime(2026, 1, 15, 9, 0)

    for from_num, to_num, count in call_patterns:
        for i in range(count):
            call_date = base_date + timedelta(days=random.randint(0, 165),
                                             hours=random.randint(0, 12))
            records.append({
                'datetime': call_date.strftime('%Y-%m-%d %H:%M:%S'),
                'from_number': from_num,
                'to_number': to_num,
                'duration_seconds': random.randint(45, 600),
                'call_type': 'outgoing'
            })

    # Additional random calls to fill to 150
    all_numbers = ['+1-415-555-0101', '+1-415-555-0102', '+1-415-555-0103',
                   '+1-415-555-0104', '+1-415-555-0105', '+1-415-555-0106',
                   '+1-415-555-0107', '+1-415-555-0108']

    while len(records) < 150:
        call_date = base_date + timedelta(days=random.randint(0, 165),
                                         hours=random.randint(0, 15))
        from_num = random.choice(all_numbers)
        to_num = random.choice([n for n in all_numbers if n != from_num])
        records.append({
            'datetime': call_date.strftime('%Y-%m-%d %H:%M:%S'),
            'from_number': from_num,
            'to_number': to_num,
            'duration_seconds': random.randint(30, 300),
            'call_type': 'outgoing'
        })

    df = pd.DataFrame(records)
    df = df.sort_values('datetime').reset_index(drop=True)
    df.to_csv(filename, index=False)
    print(f"  ✓ Generated: {filename} ({len(df)} call records)")


def generate_pharma_transactions(output_dir: str, scenario):
    """Generate PharmaCorp kickback transactions"""
    filename = os.path.join(output_dir, "pharma_transactions_202603_202607.csv")

    transactions = []

    # Kickback payments (PharmaCorp -> Morgan Medical)
    kickback_dates = ['2026-03-15', '2026-04-10', '2026-04-28', '2026-05-12',
                     '2026-05-30', '2026-06-15', '2026-06-28', '2026-07-10']
    kickback_amounts = [12000, 15000, 13500, 18000, 14000, 16500, 17000, 19000]

    for date, amount in zip(kickback_dates, kickback_amounts):
        transactions.append({
            'date': date,
            'from_account': '***6666',
            'to_account': '***5555',
            'amount': amount,
            'currency': 'USD',
            'memo': random.choice(['Consulting fees', 'Advisory services', 'Training services'])
        })

    # Morgan Medical billing HealthInsure (inflated amounts)
    billing_dates = ['2026-03-20', '2026-04-15', '2026-05-05', '2026-05-20',
                    '2026-06-05', '2026-06-20', '2026-07-05', '2026-07-15']

    for i, date in enumerate(billing_dates):
        # Billing is roughly 2x the actual cost
        base_amount = random.randint(40000, 80000)
        transactions.append({
            'date': date,
            'from_account': '***5555',
            'to_account': '***7788',
            'amount': base_amount,
            'currency': 'USD',
            'memo': 'Medical services billing'
        })

    # Normal pharmaceutical purchases
    purchase_count = 24
    base_date = datetime(2026, 3, 5)

    for i in range(purchase_count):
        date = base_date + timedelta(days=i*4)
        transactions.append({
            'date': date.strftime('%Y-%m-%d'),
            'from_account': '***5555',
            'to_account': '***6666',
            'amount': round(random.uniform(15000, 35000), 2),
            'currency': 'USD',
            'memo': 'Pharmaceutical order'
        })

    df = pd.DataFrame(transactions)
    df = df.sort_values('date').reset_index(drop=True)
    df.to_csv(filename, index=False)
    print(f"  ✓ Generated: {filename} ({len(df)} transactions)")


def generate_all_transactions(scenarios: dict):
    """Generate all CSV transaction files"""
    random.seed(RANDOM_SEED)
    output_dir = "evidence/csv"
    os.makedirs(output_dir, exist_ok=True)

    scenario_1 = scenarios['scenario_1']
    scenario_2 = scenarios['scenario_2']

    print("Generating CSV transaction files...")
    generate_techventures_transactions(output_dir, scenario_1)
    generate_phone_records(output_dir, scenario_1)
    generate_pharma_transactions(output_dir, scenario_2)

    return [
        "transactions_techventures_2026_q2.csv",
        "phone_records_chen_202601_202606.csv",
        "pharma_transactions_202603_202607.csv"
    ]


if __name__ == "__main__":
    from scenarios import load_scenarios
    scenarios = load_scenarios()
    generate_all_transactions(scenarios)
