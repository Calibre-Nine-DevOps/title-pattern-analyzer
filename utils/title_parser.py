"""
Title parser utility for extracting product attributes and patterns.
"""
import re
from typing import Optional
from config.attributes import BRANDS, get_category_attributes, detect_category, get_brands_for_category


def normalize(text: str) -> str:
    """Normalize text for matching (lowercase, strip)."""
    return text.lower().strip()


def find_attribute_in_original(original_title: str, current_title: str, values: list[str]) -> tuple[Optional[str], int, str]:
    """
    Find an attribute in the title.
    Returns: (matched_value, position_in_original, remaining_title)

    Position is the character index in the ORIGINAL title for correct ordering.
    """
    current_lower = current_title.lower()
    original_lower = original_title.lower()

    for value in values:  # Already sorted by length (longest first)
        value_lower = value.lower()

        # Try to find as whole word (with word boundaries) in current string
        pattern = r'\b' + re.escape(value_lower) + r'\b'
        match = re.search(pattern, current_lower)

        if match:
            # Remove the matched part from current title
            remaining = current_title[:match.start()] + current_title[match.end():]
            remaining = re.sub(r'\s+', ' ', remaining).strip()  # Clean up extra spaces

            # Find position in ORIGINAL title for correct ordering
            original_match = re.search(pattern, original_lower)
            original_pos = original_match.start() if original_match else match.start()

            return value, original_pos, remaining

    return None, -1, current_title


def find_quantity_regex(original_title: str, current_title: str) -> tuple[Optional[str], int, str]:
    """
    Find quantity using regex patterns.
    Matches: "x 24 Pack", "x24 pack", "24 Pack", "Set of 4", "12pk", "Dozen", "Single"
    """
    patterns = [
        # "x 24 Pack" or "x24 Pack" or "x 24 pack"
        r'\bx\s?\d+\s?pack\b',
        # "24 Pack" or "24 pack"
        r'\b\d+\s?pack\b',
        # "16 Piece" or "24 Piece"
        r'\b\d+\s?piece\b',
        # "224 Nappies" or "60 Wipes"
        r'\b\d+\s?nappies\b',
        r'\b\d+\s?wipes\b',
        # "Set of 4"
        r'\bset\s+of\s+\d+\b',
        # "12pk"
        r'\b\d+\s?pk\b',
        # "x20" or "X20" (standalone, without "pack")
        r'\bx\s?\d+\b',
        # "Dozen"
        r'\bdozen\b',
        # "Single Pack" only - not standalone "Single" (too ambiguous)
        r'\bsingle\s+pack\b',
    ]

    current_lower = current_title.lower()
    original_lower = original_title.lower()

    for pattern in patterns:
        match = re.search(pattern, current_lower, re.IGNORECASE)
        if match:
            # Get the actual matched text from current title (preserve case)
            start, end = match.start(), match.end()
            matched_value = current_title[start:end]

            # Remove from current title
            remaining = current_title[:start] + current_title[end:]
            remaining = re.sub(r'\s+', ' ', remaining).strip()

            # Find position in ORIGINAL title for correct ordering
            original_match = re.search(pattern, original_lower, re.IGNORECASE)
            original_pos = original_match.start() if original_match else start

            return matched_value, original_pos, remaining

    return None, -1, current_title


def find_size_regex(original_title: str, current_title: str) -> tuple[Optional[str], int, str]:
    """
    Find size using regex patterns.
    Matches: "500ml", "1.5L", "12oz", "500g", "1kg", "6x250ml", "6x 250mL", "Size 1 Newborn (Up to 5 kg)"
    """
    patterns = [
        # Nappy sizes: "Size 1 Newborn (Up to 5 kg)", "Size 2 Infant"
        r'\bSize\s+\d+\s+\w+\s*\([^)]+\)',
        r'\bSize\s+\d+\s+\w+',
        # Size ranges: "600-800g", "1-2kg", "500-750ml"
        r'\b\d+-\d+\s?kg\b',
        r'\b\d+-\d+\s?g\b',
        r'\b\d+-\d+\s?ml\b',
        r'\b\d+-\d+\s?lbs?\b',
        # Combined quantity + size with space: "6x 250ml", "6x 250mL", "12x 330ml"
        r'\b\d+\s?x\s+\d+\s?ml\b',
        r'\b\d+\s?x\s+\d+\s?g\b',
        r'\b\d+\s?x\s+\d+(\.\d+)?\s?L\b',
        # Combined quantity + size no space: "6x250ml", "12x330ml"
        r'\b\d+x\d+\s?ml\b',
        r'\b\d+x\d+\s?g\b',
        r'\b\d+x\d+(\.\d+)?\s?L\b',
        # Litres: "1.5L", "2 L", "1 Litre"
        r'\b\d+(\.\d+)?\s?(L|Litre|Liter)\b',
        # Millilitres: "500ml", "250 ml", "250mL"
        r'\b\d+\s?m[lL]\b',
        # Ounces: "12oz", "16 oz"
        r'\b\d+\s?oz\b',
        # Kilograms: "1.5kg", "1 kg"
        r'\b\d+(\.\d+)?\s?kg\b',
        # Grams: "500g", "250 g"
        r'\b\d+\s?g\b',
        # Pounds: "25 Pound", "5 lb", "10 lbs"
        r'\b\d+\s?pounds?\b',
        r'\b\d+\s?lbs?\b',
    ]

    for pattern in patterns:
        match = re.search(pattern, current_title, re.IGNORECASE)
        if match:
            # Get the actual matched text (preserve case)
            start, end = match.start(), match.end()
            matched_value = current_title[start:end]

            # Remove from current title
            remaining = current_title[:start] + current_title[end:]
            remaining = re.sub(r'\s+', ' ', remaining).strip()

            # Find position in ORIGINAL title for correct ordering
            original_match = re.search(pattern, original_title, re.IGNORECASE)
            original_pos = original_match.start() if original_match else start

            return matched_value, original_pos, remaining

    return None, -1, current_title


def get_remaining_label(category: str) -> str:
    """Get the appropriate label for remaining/unparsed text based on category."""
    labels = {
        "sportswear": "Model",        # Nike Pegasus 41
        "baby": "Product Type",       # Spring Water Bottles, etc.
        "groceries": "Product Type",  # The actual product name
    }
    return labels.get(category, "Product Type")


def parse_title(title: str, category: str) -> dict:
    """
    Parse a product title and extract attributes with their positions.

    Args:
        title: The product title to parse
        category: Product category (e.g., 'baby', 'sportswear', 'groceries', 'auto', 'all')

    Returns:
        Dictionary with:
        - attributes: list of {type, value, position}
        - pattern: string like "[Brand] + [Product Type] + [Size]"
        - remaining: unparsed text (could be model name, etc.)
        - detected_category: the category used (useful when 'auto' is selected)
    """
    # Auto-detect category if requested
    if category == "auto":
        category = detect_category(title)

    attributes = []
    original_title = title  # Keep original for position lookup
    remaining = title
    detected_category = category  # Track what category was used

    # 1. Extract brands (can have multiple - retailer + product brand)
    # Get category-filtered brands list
    category_brands = get_brands_for_category(detected_category)

    # Loop to find all brands in the title
    for _ in range(3):  # Max 3 brands
        brand, pos, remaining = find_attribute_in_original(original_title, remaining, category_brands)
        if brand:
            attributes.append({
                "type": "Brand",
                "value": brand,
                "position": pos
            })
        else:
            break

    # 2. Extract category-specific attributes (except size and quantity - we use regex)
    category_attrs = get_category_attributes(category)

    for attr_type, values in category_attrs.items():
        # Skip size and quantity - we'll use regex for those
        if attr_type in ['size', 'quantity']:
            continue

        # Allow multiple matches for variant and modifier (like we do for brands)
        if attr_type in ['variant', 'modifier']:
            for _ in range(3):  # Max 3 of each
                value, pos, remaining = find_attribute_in_original(original_title, remaining, values)
                if value:
                    display_type = attr_type.replace("_", " ").title()
                    attributes.append({
                        "type": display_type,
                        "value": value,
                        "position": pos
                    })
                else:
                    break
        else:
            value, pos, remaining = find_attribute_in_original(original_title, remaining, values)
            if value:
                # Convert attr_type to display name (e.g., "product_type" -> "Product Type")
                display_type = attr_type.replace("_", " ").title()
                attributes.append({
                    "type": display_type,
                    "value": value,
                    "position": pos
                })

    # 3. Extract size using regex (dynamic detection)
    size, pos, remaining = find_size_regex(original_title, remaining)
    if size:
        attributes.append({
            "type": "Size",
            "value": size,
            "position": pos
        })

    # 4. Extract quantity using regex (dynamic detection)
    quantity, pos, remaining = find_quantity_regex(original_title, remaining)
    if quantity:
        attributes.append({
            "type": "Quantity",
            "value": quantity,
            "position": pos
        })

    # 5. Sort attributes by their position in the original title
    attributes.sort(key=lambda x: x["position"])

    # 6. Generate pattern string
    pattern = " + ".join([f"[{attr['type']}]" for attr in attributes])

    # 7. Clean up remaining text (could be model, description, etc.)
    remaining = re.sub(r'\s+', ' ', remaining).strip()
    remaining = re.sub(r'^[\s\-\+,\|]+|[\s\-\+,\|]+$', '', remaining)  # Remove leading/trailing separators

    # If there's significant remaining text, label it based on category
    if remaining and len(remaining) > 2:
        remaining_label = get_remaining_label(category)

        # Check if we already have a Product Type - if so, append remaining to it
        existing_product_type = next((attr for attr in attributes if attr["type"] == "Product Type"), None)

        if existing_product_type:
            # Append remaining text to existing Product Type
            existing_product_type["value"] = f"{existing_product_type['value']} {remaining}"
            remaining = ""
        else:
            # Find position of first word of remaining text in original title
            remaining_lower = remaining.lower()
            title_lower = title.lower()
            first_word = remaining_lower.split()[0] if remaining_lower.split() else remaining_lower
            remaining_pos = title_lower.find(first_word)

            # If not found, put it after the last attribute
            if remaining_pos < 0:
                remaining_pos = max([attr["position"] for attr in attributes], default=0) + 1

            attributes.append({
                "type": remaining_label,
                "value": remaining,
                "position": remaining_pos
            })
            # Re-sort after adding
            attributes.sort(key=lambda x: x["position"])
            remaining = ""

        # Regenerate pattern
        pattern = " + ".join([f"[{attr['type']}]" for attr in attributes])

    return {
        "attributes": attributes,
        "pattern": pattern if pattern else "[Unknown]",
        "remaining": remaining,
        "detected_category": detected_category,
    }


def parse_titles_batch(titles: list[str], category: str) -> list[dict]:
    """Parse multiple titles."""
    return [parse_title(title, category) for title in titles]


# Quick test
if __name__ == "__main__":
    test_titles = [
        ("Tommee Tippee Natural Start Baby Bottles 260ml 3 Pack", "baby"),
        ("Woolworths Spring Water Bottles 600ml x 24 Pack", "baby"),
        ("Woolworths Spring Water Bottle 1.5L", "baby"),
        ("FlowFly Kids Lunch Box Insulated for Girls, Boys Blue", "baby"),
        ("Nike Men's Pegasus 41 Road Running Shoes", "sportswear"),
        ("Woolworths Lean Beef Mince 500g", "groceries"),
    ]

    for title, category in test_titles:
        result = parse_title(title, category)
        print(f"\nTitle: {title}")
        print(f"Pattern: {result['pattern']}")
        print(f"Attributes: {result['attributes']}")
        print(f"Remaining: {result['remaining']}")
