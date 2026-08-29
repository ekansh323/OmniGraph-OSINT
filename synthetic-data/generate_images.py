"""
Image Evidence Generation

Generates 6 image files using Pillow:
1. ID card (Chen's California driver's license)
2. Restaurant receipt (Chen + Kim meeting)
3. Whiteboard photo (network diagram)
4. Check image (TechVentures to CryptoHoldings $250K)
5. Text message screenshot (Chen and Kim)
6. Business card (David Kim)
"""

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def get_default_font(size=12):
    """Get a default font, trying common system fonts"""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        try:
            return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", size)
        except:
            return ImageFont.load_default()


def generate_id_card(output_dir: str, scenario):
    """Generate California driver's license for Marcus Chen"""
    filename = os.path.join(output_dir, "id_card_chen_marcus.png")

    # Create image (CA DL dimensions ratio)
    img = Image.new('RGB', (1200, 800), color='#F4E4C1')
    draw = ImageDraw.Draw(img)

    # Header
    font_large = get_default_font(40)
    font_medium = get_default_font(24)
    font_small = get_default_font(18)

    draw.rectangle([0, 0, 1200, 100], fill='#003366')
    draw.text((50, 30), "CALIFORNIA", font=font_large, fill='white')
    draw.text((400, 40), "DRIVER LICENSE", font=font_medium, fill='white')

    # Photo placeholder
    draw.rectangle([50, 150, 350, 550], fill='#CCCCCC')
    draw.text((120, 330), "PHOTO", font=font_large, fill='#666666')

    # Personal info
    y_offset = 150
    draw.text((400, y_offset), "DL D1234567", font=font_medium, fill='black')
    y_offset += 50
    draw.text((400, y_offset), "Name: CHEN, MARCUS", font=font_small, fill='black')
    y_offset += 40
    draw.text((400, y_offset), "DOB: 03/15/1985", font=font_small, fill='black')
    y_offset += 40
    draw.text((400, y_offset), "Address: 2847 Pacific Ave", font=font_small, fill='black')
    y_offset += 30
    draw.text((400, y_offset), "San Francisco, CA 94115", font=font_small, fill='black')
    y_offset += 50
    draw.text((400, y_offset), "Issued: 01/20/2024", font=font_small, fill='black')
    y_offset += 30
    draw.text((400, y_offset), "Expires: 01/20/2029", font=font_small, fill='black')
    y_offset += 40
    draw.text((400, y_offset), "Class: C", font=font_small, fill='black')

    # Barcode placeholder
    draw.rectangle([50, 600, 1150, 750], fill='black')
    for i in range(20, 1100, 40):
        draw.rectangle([i, 610, i+20, 740], fill='white')

    img.save(filename)
    print(f"  ✓ Generated: {filename}")


def generate_receipt(output_dir: str, scenario):
    """Generate restaurant receipt from Boulevard Restaurant"""
    filename = os.path.join(output_dir, "receipt_restaurant_meeting.jpg")

    img = Image.new('RGB', (1000, 1500), color='white')
    draw = ImageDraw.Draw(img)

    font_title = get_default_font(32)
    font_normal = get_default_font(20)
    font_handwriting = get_default_font(24)

    # Receipt header
    y = 50
    draw.text((400, y), "BOULEVARD", font=font_title, fill='black')
    y += 50
    draw.text((300, y), "1 Mission St, San Francisco, CA", font=font_normal, fill='black')
    y += 40
    draw.text((400, y), "Tel: 415-555-0199", font=font_normal, fill='black')
    y += 80

    # Date and time
    draw.text((50, y), "Date: 04/20/2026", font=font_normal, fill='black')
    draw.text((650, y), "Time: 7:45 PM", font=font_normal, fill='black')
    y += 40
    draw.text((50, y), "Server: Jessica", font=font_normal, fill='black')
    draw.text((650, y), "Table: 12", font=font_normal, fill='black')
    y += 60

    # Line
    draw.line([50, y, 950, y], fill='black', width=2)
    y += 40

    # Items
    items = [
        ("Grilled Salmon", "2", "$42.00", "$84.00"),
        ("Caesar Salad", "2", "$16.00", "$32.00"),
        ("House Wine (Bottle)", "1", "$55.00", "$55.00"),
        ("Espresso", "2", "$6.00", "$12.00"),
        ("Crème Brûlée", "2", "$14.00", "$28.00"),
    ]

    draw.text((50, y), "Item", font=font_normal, fill='black')
    draw.text((600, y), "Qty", font=font_normal, fill='black')
    draw.text((700, y), "Price", font=font_normal, fill='black')
    draw.text((850, y), "Total", font=font_normal, fill='black')
    y += 35

    for item, qty, price, total in items:
        draw.text((50, y), item, font=font_normal, fill='black')
        draw.text((600, y), qty, font=font_normal, fill='black')
        draw.text((700, y), price, font=font_normal, fill='black')
        draw.text((850, y), total, font=font_normal, fill='black')
        y += 35

    y += 20
    draw.line([50, y, 950, y], fill='black', width=1)
    y += 40

    # Totals
    draw.text((650, y), "Subtotal:", font=font_normal, fill='black')
    draw.text((850, y), "$211.00", font=font_normal, fill='black')
    y += 35
    draw.text((650, y), "Tax (8.5%):", font=font_normal, fill='black')
    draw.text((850, y), "$17.94", font=font_normal, fill='black')
    y += 35
    draw.text((650, y), "Tip (20%):", font=font_normal, fill='black')
    draw.text((850, y), "$42.20", font=font_normal, fill='black')
    y += 35
    draw.line([650, y, 950, y], fill='black', width=2)
    y += 40
    draw.text((650, y), "TOTAL:", font=font_title, fill='black')
    draw.text((850, y), "$271.14", font=font_title, fill='black')
    y += 80

    # Handwritten note
    draw.text((50, y), "Guests: M. Chen + D. Kim", font=font_handwriting, fill='#0000AA')
    y += 50
    draw.text((300, y), "Thank you for dining with us!", font=font_normal, fill='black')

    img.save(filename, 'JPEG', quality=90)
    print(f"  ✓ Generated: {filename}")


def generate_whiteboard(output_dir: str, scenario):
    """Generate whiteboard photo with network diagram"""
    filename = os.path.join(output_dir, "whiteboard_meeting_notes.jpg")

    img = Image.new('RGB', (1920, 1080), color='#FAFAFA')
    draw = ImageDraw.Draw(img)

    font_large = get_default_font(40)
    font_medium = get_default_font(28)

    # Title
    draw.text((700, 50), "Money Flow - Q2 2026", font=font_large, fill='#0000CC')

    # Draw boxes for entities
    boxes = [
        (300, 250, 600, 350, "Chen Personal\n***1234"),
        (900, 250, 1200, 350, "TechVentures LLC\n***5678"),
        (300, 550, 600, 650, "CryptoHoldings\n***9012"),
        (900, 550, 1200, 650, "OffshoreConsult\nCrypto: 0x7a8b..."),
        (1450, 550, 1750, 650, "Pacific Trust\n***2468"),
    ]

    for x1, y1, x2, y2, label in boxes:
        draw.rectangle([x1, y1, x2, y2], outline='#CC0000', width=3)
        # Draw label
        lines = label.split('\n')
        ly = y1 + 30
        for line in lines:
            draw.text((x1 + 20, ly), line, font=font_medium, fill='black')
            ly += 40

    # Draw arrows
    arrow_color = '#CC0000'
    draw.line([600, 300, 900, 300], fill=arrow_color, width=4)
    draw.polygon([(900, 300), (880, 290), (880, 310)], fill=arrow_color)
    draw.text((720, 250), "$300K", font=font_medium, fill='#CC0000')

    draw.line([1050, 350, 1050, 550], fill=arrow_color, width=4)
    draw.polygon([(1050, 550), (1040, 530), (1060, 530)], fill=arrow_color)
    draw.text((1080, 430), "$300K", font=font_medium, fill='#CC0000')

    draw.line([600, 600, 900, 600], fill=arrow_color, width=4)
    draw.polygon([(900, 600), (880, 590), (880, 610)], fill=arrow_color)
    draw.text((720, 560), "$280K", font=font_medium, fill='#CC0000')

    draw.line([1200, 600, 1450, 600], fill=arrow_color, width=4)
    draw.polygon([(1450, 600), (1430, 590), (1430, 610)], fill=arrow_color)
    draw.text((1280, 560), "$270K", font=font_medium, fill='#CC0000')

    # Cycle arrow back
    draw.line([1600, 550, 1600, 400], fill=arrow_color, width=4)
    draw.line([1600, 400, 450, 400], fill=arrow_color, width=4)
    draw.line([450, 400, 450, 350], fill=arrow_color, width=4)
    draw.polygon([(450, 350), (440, 370), (460, 370)], fill=arrow_color)
    draw.text((900, 360), "$260K back", font=font_medium, fill='#CC0000')

    # Total amount
    draw.rectangle([700, 850, 1220, 950], outline='#0000CC', width=5, fill='#FFFFCC')
    draw.text((750, 880), "Total Cycle: $850K", font=font_large, fill='#CC0000')

    img.save(filename, 'JPEG', quality=85)
    print(f"  ✓ Generated: {filename}")


def generate_check(output_dir: str, scenario):
    """Generate check image from TechVentures to CryptoHoldings"""
    filename = os.path.join(output_dir, "check_image_250k.png")

    img = Image.new('RGB', (1200, 600), color='#E8F4F8')
    draw = ImageDraw.Draw(img)

    font_large = get_default_font(28)
    font_medium = get_default_font(20)
    font_small = get_default_font(16)

    # Border
    draw.rectangle([20, 20, 1180, 580], outline='#003366', width=3)

    # Bank info
    draw.text((50, 50), "FIRST NATIONAL BANK", font=font_large, fill='#003366')
    draw.text((50, 85), "1 Montgomery St, San Francisco, CA 94104", font=font_small, fill='black')

    # Check number and date
    draw.text((950, 50), "Check #1234", font=font_medium, fill='black')
    draw.text((950, 85), "Date: 03/15/2026", font=font_medium, fill='black')

    # Pay to the order of
    y = 180
    draw.text((50, y), "Pay to the", font=font_medium, fill='black')
    draw.text((50, y+30), "order of:", font=font_medium, fill='black')
    draw.line([200, y+50, 1100, y+50], fill='black', width=2)
    draw.text((210, y+20), "CryptoHoldings Inc", font=font_large, fill='black')

    # Amount box
    draw.rectangle([1000, 170, 1160, 220], outline='black', width=2)
    draw.text((1010, 180), "$250,000.00", font=font_large, fill='black')

    # Amount in words
    y = 280
    draw.line([50, y+50, 1100, y+50], fill='black', width=2)
    draw.text((60, y+20), "Two Hundred Fifty Thousand and 00/100 Dollars", font=font_medium, fill='black')

    # Memo
    y = 380
    draw.text((50, y), "Memo:", font=font_medium, fill='black')
    draw.line([150, y+30, 600, y+30], fill='black', width=1)
    draw.text((160, y+5), "Consulting Services - Q1 2026", font=font_medium, fill='black')

    # Account info
    y = 500
    draw.text((50, y), "TechVentures LLC", font=font_medium, fill='black')
    draw.text((50, y+30), "Account: ***5678", font=font_small, fill='black')

    # Signature line
    draw.line([700, 520, 1100, 520], fill='black', width=2)
    draw.text((710, 490), "Marcus Chen (signature)", font=font_medium, fill='#0000AA')

    # MICR line (magnetic ink at bottom)
    draw.text((50, 540), ":987654321:  1234  9876543210", font=font_small, fill='black')

    img.save(filename)
    print(f"  ✓ Generated: {filename}")


def generate_text_message(output_dir: str, scenario):
    """Generate text message screenshot between Chen and Kim"""
    filename = os.path.join(output_dir, "text_message_screenshot.png")

    img = Image.new('RGB', (800, 1400), color='white')
    draw = ImageDraw.Draw(img)

    font_header = get_default_font(24)
    font_message = get_default_font(18)
    font_time = get_default_font(14)

    # Phone header
    draw.rectangle([0, 0, 800, 80], fill='#F0F0F0')
    draw.text((300, 30), "David Kim", font=font_header, fill='black')

    # Messages
    y = 120

    # Message from Chen (right side, blue)
    messages = [
        ("right", "Hey David, need to discuss the", "10:23 AM"),
        ("right", "offshore arrangement. Call me.", "10:23 AM"),
        ("left", "Sure. Give me 10 mins.", "10:25 AM"),
        ("right", "The paperwork from Martinez looks", "10:38 AM"),
        ("right", "good. OffshoreConsult is ready.", "10:38 AM"),
        ("left", "Perfect. I'll handle the CryptoHoldings", "10:40 AM"),
        ("left", "side. $280K transfer tomorrow?", "10:40 AM"),
        ("right", "Yes. Keep it quiet. Sarah knows", "10:42 AM"),
        ("right", "but no one else should.", "10:42 AM"),
        ("left", "Understood. Will coordinate.", "10:43 AM"),
    ]

    for side, text, time in messages:
        if side == "right":
            # Sender's messages (blue, right aligned)
            box_width = min(500, len(text) * 10 + 40)
            x1 = 800 - box_width - 20
            x2 = 780
            draw.rounded_rectangle([x1, y, x2, y+50], radius=10, fill='#007AFF')
            draw.text((x1+10, y+15), text, font=font_message, fill='white')
            draw.text((x2-80, y+55), time, font=font_time, fill='#888888')
        else:
            # Receiver's messages (gray, left aligned)
            box_width = min(500, len(text) * 10 + 40)
            x1 = 20
            x2 = 20 + box_width
            draw.rounded_rectangle([x1, y, x2, y+50], radius=10, fill='#E5E5EA')
            draw.text((x1+10, y+15), text, font=font_message, fill='black')
            draw.text((x1+10, y+55), time, font=font_time, fill='#888888')

        y += 90

    img.save(filename)
    print(f"  ✓ Generated: {filename}")


def generate_business_card(output_dir: str, scenario):
    """Generate David Kim's business card"""
    filename = os.path.join(output_dir, "business_card_kim_david.jpg")

    img = Image.new('RGB', (600, 400), color='#1A1A2E')
    draw = ImageDraw.Draw(img)

    font_large = get_default_font(32)
    font_medium = get_default_font(20)
    font_small = get_default_font(16)

    # Border
    draw.rectangle([10, 10, 590, 390], outline='#16C79A', width=3)

    # Company logo area
    draw.rectangle([30, 30, 150, 150], fill='#16C79A')
    draw.text((50, 70), "CH", font=get_default_font(50), fill='white')

    # Company name
    draw.text((180, 40), "CryptoHoldings Inc", font=font_large, fill='#16C79A')
    draw.text((180, 80), "Digital Asset Management", font=font_small, fill='#AAAAAA')

    # Name and title
    y = 180
    draw.text((30, y), "David Kim", font=get_default_font(36), fill='white')
    y += 50
    draw.text((30, y), "Director", font=font_medium, fill='#16C79A')

    # Contact info
    y = 280
    draw.text((30, y), "Phone: +1-415-555-0103", font=font_small, fill='white')
    y += 30
    draw.text((30, y), "Email: dkim@cryptoholdings.com", font=font_small, fill='white')
    y += 30
    draw.text((30, y), "450 Sutter St, Suite 1200, San Francisco, CA 94108", font=font_small, fill='white')

    img.save(filename, 'JPEG', quality=95)
    print(f"  ✓ Generated: {filename}")


def generate_all_images(scenarios: dict):
    """Generate all image evidence files"""
    output_dir = "evidence/images"
    os.makedirs(output_dir, exist_ok=True)

    scenario_1 = scenarios['scenario_1']

    print("Generating image evidence files...")
    generate_id_card(output_dir, scenario_1)
    generate_receipt(output_dir, scenario_1)
    generate_whiteboard(output_dir, scenario_1)
    generate_check(output_dir, scenario_1)
    generate_text_message(output_dir, scenario_1)
    generate_business_card(output_dir, scenario_1)

    return [
        "id_card_chen_marcus.png",
        "receipt_restaurant_meeting.jpg",
        "whiteboard_meeting_notes.jpg",
        "check_image_250k.png",
        "text_message_screenshot.png",
        "business_card_kim_david.jpg"
    ]


if __name__ == "__main__":
    from scenarios import load_scenarios
    scenarios = load_scenarios()
    generate_all_images(scenarios)
