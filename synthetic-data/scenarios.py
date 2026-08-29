"""
OmniGraph OSINT - Synthetic Investigation Scenarios

Defines two fictional investigation scenarios with entities, relationships, and transactions.
All data is completely synthetic and safe for public repositories.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class Person:
    """Individual person entity"""
    id: str
    name: str
    aliases: List[str]
    phone: str
    email: str
    role: str
    address: Optional[str] = None

@dataclass
class Organization:
    """Company or organization entity"""
    id: str
    name: str
    registration_number: str
    address: str
    type: str = "company"  # company, shell, legitimate

@dataclass
class Account:
    """Financial account (bank or crypto)"""
    id: str
    account_number: str  # Masked format: ***1234
    account_type: str  # bank or crypto
    owner_entity_id: str
    bank_name: str
    full_number: Optional[str] = None  # For internal use only

@dataclass
class Location:
    """Physical location"""
    id: str
    name: str
    address: str
    type: str  # office, residence, meeting_place

@dataclass
class Relationship:
    """Relationship between entities"""
    source_id: str
    target_id: str
    type: str  # OWNS, CONTROLS, CALLS, ASSOCIATED_WITH, TRANSFERRED_FUNDS, LOCATED_AT
    confidence: float
    evidence_file: str
    context: str
    timestamp: Optional[datetime] = None

@dataclass
class Transaction:
    """Financial transaction"""
    sender_account_id: str
    receiver_account_id: str
    amount: float
    currency: str
    timestamp: datetime
    description: str

@dataclass
class Scenario:
    """Investigation scenario container"""
    name: str
    timeline_start: datetime
    timeline_end: datetime
    people: List[Person]
    organizations: List[Organization]
    accounts: List[Account]
    locations: List[Location]
    relationships: List[Relationship]
    transactions: List[Transaction]


def get_scenario_1() -> Scenario:
    """
    Scenario 1: Shadow Holdings Network

    Tech entrepreneur Marcus Chen uses shell companies to hide assets and funnel
    money through cryptocurrency accounts. Demonstrates transaction cycles, structuring,
    and multi-hop relationships.

    Timeline: January 2026 - August 2026 (8 months)
    """

    # People
    people = [
        Person(
            id="person_chen_001",
            name="Marcus Chen",
            aliases=["M. Chen", "Mark Chen"],
            phone="+1-415-555-0101",
            email="mchen@techventures.com",
            role="CEO, TechVentures LLC",
            address="2847 Pacific Ave, San Francisco, CA 94115"
        ),
        Person(
            id="person_rodriguez_001",
            name="Sarah Rodriguez",
            aliases=["S. Rodriguez"],
            phone="+1-415-555-0102",
            email="srodriguez@techventures.com",
            role="CFO, TechVentures LLC",
            address="1234 Valencia St, San Francisco, CA 94110"
        ),
        Person(
            id="person_kim_001",
            name="David Kim",
            aliases=["D. Kim"],
            phone="+1-415-555-0103",
            email="dkim@cryptoholdings.com",
            role="Director, CryptoHoldings Inc",
            address="567 Divisadero St, San Francisco, CA 94117"
        ),
        Person(
            id="person_white_001",
            name="Jennifer White",
            aliases=["J. White", "Jenny White"],
            phone="+1-415-555-0104",
            email="jwhite@accounting-sf.com",
            role="Senior Accountant",
            address="890 Folsom St, San Francisco, CA 94107"
        ),
        Person(
            id="person_martinez_001",
            name="Robert Martinez",
            aliases=["R. Martinez", "Bob Martinez"],
            phone="+1-415-555-0105",
            email="rmartinez@martinez-law.com",
            role="Corporate Attorney",
            address="555 California St, Suite 3100, San Francisco, CA 94104"
        ),
        Person(
            id="person_thompson_001",
            name="Lisa Thompson",
            aliases=["L. Thompson"],
            phone="+1-415-555-0106",
            email="lthompson@techventures.com",
            role="Executive Assistant to Marcus Chen",
            address="321 Hayes St, San Francisco, CA 94102"
        ),
        Person(
            id="person_brown_001",
            name="Michael Brown",
            aliases=["M. Brown", "Mike Brown"],
            phone="+1-415-555-0107",
            email="mbrown@cryptotraders.io",
            role="Cryptocurrency Specialist",
            address="789 Market St, Suite 400, San Francisco, CA 94103"
        ),
        Person(
            id="person_davis_001",
            name="Amanda Davis",
            aliases=["A. Davis"],
            phone="+1-415-555-0108",
            email="adavis@firstnationalbank.com",
            role="Commercial Banking Manager",
            address="1 Montgomery St, San Francisco, CA 94104"
        ),
    ]

    # Organizations
    organizations = [
        Organization(
            id="org_techventures_001",
            name="TechVentures LLC",
            registration_number="DE-2024-887654",
            address="1500 Market St, Suite 2000, San Francisco, CA 94102",
            type="company"
        ),
        Organization(
            id="org_cryptoholdings_001",
            name="CryptoHoldings Inc",
            registration_number="DE-2025-991234",
            address="450 Sutter St, Suite 1200, San Francisco, CA 94108",
            type="shell"
        ),
        Organization(
            id="org_offshoreconsult_001",
            name="OffshoreConsult Ltd",
            registration_number="DE-2025-003456",
            address="789 Delaware Ave, Wilmington, DE 19801",
            type="shell"
        ),
        Organization(
            id="org_pacifictrust_001",
            name="Pacific Trust Services",
            registration_number="NV-2025-112233",
            address="555 E Washington Ave, Las Vegas, NV 89101",
            type="shell"
        ),
        Organization(
            id="org_firstnational_001",
            name="First National Bank",
            registration_number="CA-BANK-1001",
            address="1 Montgomery St, San Francisco, CA 94104",
            type="legitimate"
        ),
    ]

    # Accounts
    accounts = [
        # Personal bank accounts
        Account("account_chen_personal_001", "***1234", "bank", "person_chen_001", "First National Bank", "4532-8876-9012-1234"),
        Account("account_rodriguez_personal_001", "***2345", "bank", "person_rodriguez_001", "First National Bank", "4532-8876-9012-2345"),
        Account("account_kim_personal_001", "***3456", "bank", "person_kim_001", "Wells Fargo", "5421-7543-2109-3456"),
        Account("account_white_personal_001", "***4567", "bank", "person_white_001", "Chase Bank", "6011-3245-8765-4567"),
        Account("account_martinez_personal_001", "***5678", "bank", "person_martinez_001", "Bank of America", "3782-9876-5432-5678"),
        Account("account_thompson_personal_001", "***6789", "bank", "person_thompson_001", "Wells Fargo", "5421-1234-5678-6789"),
        Account("account_brown_personal_001", "***7890", "bank", "person_brown_001", "Chase Bank", "6011-8765-4321-7890"),
        Account("account_davis_personal_001", "***8901", "bank", "person_davis_001", "First National Bank", "4532-9012-3456-8901"),

        # Business bank accounts
        Account("account_techventures_001", "***9010", "bank", "org_techventures_001", "First National Bank", "9876-5432-1098-9010"),
        Account("account_cryptoholdings_001", "***9012", "bank", "org_cryptoholdings_001", "Silicon Valley Bank", "8765-4321-0987-9012"),
        Account("account_offshoreconsult_001", "***1357", "bank", "org_offshoreconsult_001", "International Trust Bank", "7654-3210-9876-1357"),
        Account("account_pacifictrust_001", "***2468", "bank", "org_pacifictrust_001", "Nevada State Bank", "6543-2109-8765-2468"),
        Account("account_firstnational_001", "***9999", "bank", "org_firstnational_001", "First National Bank", "1111-2222-3333-9999"),

        # Offshore accounts
        Account("account_chen_offshore_001", "***7777", "bank", "person_chen_001", "Cayman International Bank", "9999-8888-7777-7777"),
        Account("account_chen_offshore_002", "***8888", "bank", "person_chen_001", "Panama Trust Bank", "8888-7777-6666-8888"),

        # Crypto wallets
        Account("account_chen_crypto_001", "0x3c4d...", "crypto", "person_chen_001", "Ethereum Mainnet", "0x3c4def123456789abcdef"),
        Account("account_chen_crypto_002", "0x9f2a...", "crypto", "person_chen_001", "Bitcoin Network", "0x9f2a987654321fedcba"),
        Account("account_rodriguez_crypto_001", "0x5e8b...", "crypto", "person_rodriguez_001", "Ethereum Mainnet", "0x5e8b234567890abcdef"),
        Account("account_brown_crypto_001", "0x7a1c...", "crypto", "person_brown_001", "Bitcoin Network", "0x7a1c345678901bcdef"),
        Account("account_kim_crypto_001", "0x2d9e...", "crypto", "person_kim_001", "Ethereum Mainnet", "0x2d9e456789012cdef"),
        Account("account_cryptoholdings_crypto_001", "0x7a8b...", "crypto", "org_cryptoholdings_001", "Ethereum Mainnet", "0x7a8b567890123def"),
        Account("account_techventures_crypto_001", "0x1b3c...", "crypto", "org_techventures_001", "Bitcoin Network", "0x1b3c678901234ef"),
        Account("account_pacifictrust_crypto_001", "0x4f7d...", "crypto", "org_pacifictrust_001", "Ethereum Mainnet", "0x4f7d789012345f"),
    ]

    # Locations
    locations = [
        Location("location_techventures_hq", "TechVentures HQ", "1500 Market St, Suite 2000, San Francisco, CA 94102", "office"),
        Location("location_chen_residence", "Chen's Residence", "2847 Pacific Ave, San Francisco, CA 94115", "residence"),
        Location("location_cryptoholdings_office", "CryptoHoldings Office", "450 Sutter St, Suite 1200, San Francisco, CA 94108", "office"),
        Location("location_bank_branch", "First National Bank Branch", "1 Montgomery St, San Francisco, CA 94104", "office"),
        Location("location_restaurant_meeting", "Boulevard Restaurant", "1 Mission St, San Francisco, CA 94105", "meeting_place"),
        Location("location_martinez_office", "Martinez Law Office", "555 California St, Suite 3100, San Francisco, CA 94104", "office"),
    ]

    # Relationships (will be populated by extraction JSONs)
    relationships = []

    # Transactions
    transactions = []

    return Scenario(
        name="Shadow Holdings Network",
        timeline_start=datetime(2026, 1, 1),
        timeline_end=datetime(2026, 8, 28),
        people=people,
        organizations=organizations,
        accounts=accounts,
        locations=locations,
        relationships=relationships,
        transactions=transactions
    )


def get_scenario_2() -> Scenario:
    """
    Scenario 2: PharmaCorp Kickback Scheme

    Healthcare fraud involving overbilling and kickback payments between a medical
    clinic and pharmaceutical distributor. Simpler pattern for contrast.

    Timeline: March 2026 - July 2026 (5 months)
    """

    people = [
        Person(
            id="person_morgan_001",
            name="Dr. Elizabeth Morgan",
            aliases=["E. Morgan", "Dr. Morgan"],
            phone="+1-408-555-0201",
            email="emorgan@morganmedical.com",
            role="Owner, Morgan Medical Clinic",
            address="456 Oak Street, San Jose, CA 95113"
        ),
        Person(
            id="person_parker_001",
            name="James Parker",
            aliases=["J. Parker"],
            phone="+1-408-555-0202",
            email="jparker@morganmedical.com",
            role="Billing Manager",
            address="123 Elm Street, San Jose, CA 95114"
        ),
        Person(
            id="person_lee_001",
            name="Susan Lee",
            aliases=["S. Lee"],
            phone="+1-408-555-0203",
            email="slee@pharmacorp.com",
            role="Sales Representative, PharmaCorp",
            address="789 Pine Ave, San Jose, CA 95116"
        ),
        Person(
            id="person_wilson_001",
            name="Tom Wilson",
            aliases=["T. Wilson"],
            phone="+1-408-555-0204",
            email="twilson@healthinsure.com",
            role="Fraud Investigator",
            address="2500 Insurance Plaza, Sacramento, CA 95814"
        ),
    ]

    organizations = [
        Organization(
            id="org_morganmedical_001",
            name="Morgan Medical Clinic",
            registration_number="CA-MED-45678",
            address="789 Health Way, San Jose, CA 95110",
            type="company"
        ),
        Organization(
            id="org_pharmacorp_001",
            name="PharmaCorp Distributors",
            registration_number="CA-2023-556677",
            address="1200 Industrial Pkwy, San Jose, CA 95112",
            type="company"
        ),
        Organization(
            id="org_healthinsure_001",
            name="HealthInsure Co",
            registration_number="CA-INS-9988",
            address="2500 Insurance Plaza, Sacramento, CA 95814",
            type="legitimate"
        ),
    ]

    accounts = [
        Account("account_morgan_personal_001", "***1122", "bank", "person_morgan_001", "Bank of America", "3456-7890-1234-1122"),
        Account("account_parker_personal_001", "***0123", "bank", "person_parker_001", "Wells Fargo", "4567-8901-2345-0123"),
        Account("account_lee_personal_001", "***2233", "bank", "person_lee_001", "Chase Bank", "5678-9012-3456-2233"),
        Account("account_wilson_personal_001", "***3344", "bank", "person_wilson_001", "Capital One", "6789-0123-4567-3344"),
        Account("account_morganmedical_001", "***5555", "bank", "org_morganmedical_001", "Wells Fargo Business", "7890-1234-5678-5555"),
        Account("account_pharmacorp_001", "***6666", "bank", "org_pharmacorp_001", "Chase Business", "8901-2345-6789-6666"),
        Account("account_healthinsure_001", "***7788", "bank", "org_healthinsure_001", "Bank of America Business", "9012-3456-7890-7788"),
    ]

    locations = [
        Location("location_clinic", "Morgan Medical Clinic", "789 Health Way, San Jose, CA 95110", "office"),
        Location("location_warehouse", "PharmaCorp Warehouse", "1200 Industrial Pkwy, San Jose, CA 95112", "office"),
        Location("location_morgan_residence", "Dr. Morgan's Residence", "456 Oak Street, San Jose, CA 95113", "residence"),
        Location("location_parker_residence", "Parker's Residence", "123 Elm Street, San Jose, CA 95114", "residence"),
    ]

    relationships = []
    transactions = []

    return Scenario(
        name="PharmaCorp Kickback Scheme",
        timeline_start=datetime(2026, 3, 1),
        timeline_end=datetime(2026, 7, 31),
        people=people,
        organizations=organizations,
        accounts=accounts,
        locations=locations,
        relationships=relationships,
        transactions=transactions
    )


def load_scenarios():
    """Load all defined scenarios"""
    return {
        "scenario_1": get_scenario_1(),
        "scenario_2": get_scenario_2()
    }
