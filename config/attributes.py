"""
Product attribute dictionaries for title parsing.
Sorted by length (longest first) for accurate matching.
"""

# Universal brands (add more as needed)
BRANDS = sorted([
    # Baby / Kids products
    "Tommee Tippee",
    "Baby Brezza",
    "Philips Avent",
    "Dr. Brown's",
    "Dr Browns",
    "The Aussie PAL",
    "Aussie PAL",
    "Hydro Flask",
    "B.Box",
    "b.box",
    "Bbox",
    "Sistema",
    "Thermos",
    "Smiggle",
    "Yumbox",
    "Bentgo",
    "OmieBox",
    "Omiebox",
    "LunchBots",
    "Planetbox",
    "Funtainer",
    "Skip Hop",
    "Munchkin",
    "FlowFly",
    "Nuk",
    "NUK",
    "MAM",
    "Avent",
    "Pigeon",
    "Medela",
    "Spectra",
    "Haakaa",
    "Comotomo",
    "Zojirushi",
    "Stanley",
    "Contigo",
    "CamelBak",
    "Camelbak",
    "Nalgene",
    "Klean Kanteen",
    "S'well",
    "Swell",
    "Corkcicle",
    "YETI",
    "Yeti",
    "Igloo",
    "Coleman",
    "Esky",

    # Sportswear
    "The North Face",
    "Under Armour",
    "New Balance",
    "Nike",
    "Adidas",
    "Puma",
    "Reebok",
    "Asics",
    "Brooks",
    "Saucony",
    "On Running",
    "Hoka",
    "Lululemon",
    "Gymshark",
    "Fila",
    "Converse",
    "Vans",

    # Groceries
    "(AUSTRALIA) JMW FOODS",
    "JMW FOODS",
    "Harris Farm Markets",
    "Harris Farm",
    "Black Forest Smokehouse",
    "Black Forest Estate",
    "Black & Gold",
    "Ingham's",
    "Inghams",
    "La Banderita",
    "City Beach",
    "Get It Now",
    "Mooloola",
    "Ben's Original",
    "Bens Original",
    "Uncle Ben's",
    "Uncle Bens",
    "Ceres",
    "Asian Best",
    "Marna Shupatto",
    "Marna",
    "Shupatto",
    "Woolworths",
    "Coles",
    "Aldi",
    "Arnott's",
    "Arnotts",
    "Golden Circle",
    "Anko",
    "Huggies",
    "Pampers",
    "BabyLove",
    "Babylove",
    "Bagbase",
    "BagBase",
    "Cherub Baby",
    "Daily Juice Co",
    "Juice Co",
    "Black Pepper",  # Clothing brand - auto-detect will handle groceries context
    "Black Hawk",  # Pet food brand

    # Add more brands here...
], key=lambda x: -len(x))


# Category-specific attributes
ATTRIBUTES = {
    "baby": {
        "product_type": sorted([
            # Feeding - specific terms only
            "Baby Bottles",
            "Formula Dispenser",
            "Sterilizer",
            "Breast Pump",
            "Bottle Warmer",
            "Feeding Set",
            # Lunch / Food storage
            "Lunch Box",
            "Lunchbox",
            "Bento Box",
            "Reusable Food Pouches",
            "Reusable Food Pouch",
            "Food Pouches",
            "Food Pouch",
            "Food Jar",
            "Snack Box",
            "Snack Container",
            "Food Container",
            # Drinks
            "Water Bottle",
            "Drink Bottle",
            "Sippy Cup",
            "Straw Cup",
            "Tumbler",
            # Coolers & Bags
            "Recycled Eco Bag",
            "Recycled Drawstring Bag",
            "Drawstring Bag",
            "Eco Bag",
            "Cooler Bag",
            "Insulated Bag",
            "Lunch Bag",
            "Backpack",
            "Tote Bag",
            "Ice Pack",
            # Utensils
            "Cutlery Set",
            # Baby care
            "Pure Baby Cleansing Wipes",
            "Baby Cleansing Wipes",
            "Cleansing Wipes",
            "Baby Wipes",
            "Nappies",
            "Diapers",
            # Removed generic terms: Bottles, Bottle, Container, Flask, Cooler, etc.
            # These are too vague and cause duplicate Product Type issues
        ], key=lambda x: -len(x)),

        "modifier": sorted([
            # These are prefixes/modifiers, not product types
            "On The Go",
            "On the Go",
            "Grab and Go",
            "Bundle",
            "Multipack",
            "Value Pack",
            "Starter Kit",
            "Gift Set",
        ], key=lambda x: -len(x)),

        "variant": sorted([
            # Bottle variants
            "Natural Start",
            "Anti-Colic",
            "Anti Colic",
            "Advanced",
            "Classic",
            "Original",
            "Wide Neck",
            "Wide Mouth",
            "Narrow Neck",
            "Standard Mouth",
            "Glass",
            "Plastic",
            "Silicone",
            "Stainless Steel",
            "Insulated",
            "Ultimate",
            "Pro",
            "Mini Pack",
            "Mini",
            "Junior",
        ], key=lambda x: -len(x)),

        # NOTE: Size and Quantity are now detected via regex in title_parser.py
        # No need to hardcode values here - they match dynamically:
        # Size: 500ml, 1.5L, 12oz, 500g, 1kg, etc.
        # Quantity: x 24 Pack, 12 Pack, Set of 4, 6pk, etc.

        "gender": sorted([
            "for Girls",
            "for Boys",
            "Girls",
            "Boys",
            "Unisex",
            "Men's",
            "Mens",
            "Women's",
            "Womens",
            "Men",
            "Women",
            "Male",
            "Female",
        ], key=lambda x: -len(x)),

        "age": sorted([
            "for Kids",
            "for Adults",
            "Kids",
            "Kids'",
            "Adults",
            "Adult",
            "Junior",
            "Baby",
            "Toddler",
            "Infant",
            "Newborn",
        ], key=lambda x: -len(x)),

        "color": sorted([
            "Blue Moon",
            "Black",
            "White",
            "Blue",
            "Pink",
            "Green",
            "Red",
            "Purple",
            "Yellow",
            "Orange",
            "Grey",
            "Gray",
            "Navy",
            "Teal",
            "Aqua",
            # Colors are matched AFTER product types, so:
            # "Orange Juice" (product type) matches first → "Orange" won't match
            # "Pink Lady Apples" (product type) matches first → "Pink" won't match
        ], key=lambda x: -len(x)),
    },

    "sportswear": {
        "product_type": sorted([
            "Running Shoes",
            "Shoes",
            "Sneakers",
            "Shorts",
            "Jersey",
            "T-Shirt",
            "Jacket",
            "Pants",
            "Leggings",
            "Sports Bra",
            "Socks",
        ], key=lambda x: -len(x)),

        "gender": sorted([
            "Women's",
            "Womens",
            "Men's",
            "Mens",
            "Kids",
            "Kids'",
            "Unisex",
            "Boys",
            "Girls",
            "Junior",
        ], key=lambda x: -len(x)),

        "sport": sorted([
            "Running",
            "Tennis",
            "Basketball",
            "Golf",
            "Soccer",
            "Football",
            "Training",
            "Gym",
            "CrossFit",
            "Yoga",
            "Swimming",
        ], key=lambda x: -len(x)),

        "color": sorted([
            "Black",
            "White",
            "Red",
            "Blue",
            "Navy",
            "Grey",
            "Gray",
            "Green",
            "Pink",
            "Orange",
            "Yellow",
            "Purple",
        ], key=lambda x: -len(x)),
    },

    "groceries": {
        "product_type": sorted([
            # Meat - Chicken
            "Chicken Single Breast Fillet",
            "Chicken Breast Fillet",
            "Chicken Breast Fillets",
            "Chicken Breast",
            "Chicken Thigh Fillet",
            "Chicken Thigh Fillets",
            "Chicken Thigh",
            "Chicken Thighs",
            "Chicken Wings",
            "Chicken Drumsticks",
            "Chicken Tenderloins",
            "Chicken Nibbles",
            "Whole Chicken",
            "Roast Chicken",
            "Chicken Breast Nuggets",
            "Chicken Nuggets",
            "Chicken Schnitzel",
            # Meat - Beef
            "Beef Mince",
            "Beef Steak",
            "Beef Rump",
            "Beef Sirloin",
            "Beef Scotch Fillet",
            # Meat - Lamb
            "Lamb Chops",
            "Lamb Cutlets",
            "Lamb Mince",
            "Lamb Leg",
            # Meat - Pork
            "Pork Chops",
            "Pork Mince",
            "Pork Belly",
            "Bacon",
            # Seafood
            "Salmon Fillets",
            "Salmon",
            "Prawns",
            "Fish Fillets",
            # Dairy
            "Eggs",
            "Milk",
            "Cheese",
            "Yoghurt",
            "Butter",
            "Cream",
            # Fruits - specific varieties
            "Fresh Pink Lady Apples",
            "Pink Lady Apples",
            "Granny Smith Apples",
            "Royal Gala Apples",
            "Bananas",
            "Apples",
            "Oranges",
            "Strawberries",
            "Grapes",
            "Mangoes",
            "Avocados",
            "Blueberries",
            # Vegetables
            "Mixed Vegetables",
            "White Potatoes",
            "Baby White Potatoes",
            "Potatoes",
            "Tomatoes",
            "Onions",
            "Carrots",
            "Broccoli",
            "Lettuce",
            "Spinach",
            "Capsicum",
            "Vegetables",
            # Bakery
            "White Loaf",
            "Bread",
            "Loaf",
            "Tortillas",
            "Tortilla",
            "Wraps",
            # Baby products
            "Pure Baby Cleansing Wipes",
            "Baby Cleansing Wipes",
            "Cleansing Wipes",
            "Nappies",
            "Diapers",
            "Baby Wipes",
            "Wipes",
            # Ready meals
            "Green Chicken Curry",
            "Butter Chicken",
            "Chicken Curry",
            "Beef Curry",
            "Fried Rice",
            "Pasta",
            "Meat Pie",
            "Meat Pies",
            "Sausage Roll",
            "Sausage Rolls",
            # Rice products
            "Garlic Rice Pouch",
            "Rice Pouch",
            "Garlic Rice",
            "Basmati Rice",
            "Jasmine Rice",
            "Sushi Rice",
            "Brown Rice",
            "White Rice",
            "Rice",
            # Drinks
            "Apple Blackcurrant Poppers Fruit Drink Multipack Lunchbox",
            "Apple Blackcurrant Poppers Fruit Drink",
            "Poppers Fruit Drink Multipack Lunchbox",
            "Poppers Fruit Drink",
            "Black Label Chilled Orange Juice",
            "Black Label Orange Juice",
            "Chilled Orange Juice",
            "Fruit Juice",
            "Orange Juice",
            "Apple Juice",
            "Water",
            "Soft Drink",
            "Beer",
            "Wine",
            # Pet food
            "Lamb & Rice Dog Food",
            "Chicken & Rice Dog Food",
            "Dog Food",
            "Cat Food",
            "Pet Food",
            # Snacks / Biscuits
            "Scotch Finger Biscuits",
            "Scotch Finger",
            "Biscuits",
            "Chips",
            "Potato Chips",
            "Crinkle Cut Potato Chips",
            # Appliances
            "Roaster",
            "Toaster",
            "Kettle",
            "Blender",
            "Air Fryer",
        ], key=lambda x: -len(x)),

        "variant": sorted([
            "Smoked Garlic Black Pepper",
            "Garlic Black Pepper",
            "Black Pepper",
            "Grass Fed",
            "Free Range",
            "Organic",
            "Lean",
            "Regular",
            "Premium",
            "Original",
            "Ora King",
            "RSPCA Approved",
            "Hormone Free",
            "Cage Free",
            "Fresh",
            "Frozen",
            "Marinated",
            # Scents/Fragrances (cat litter, cleaning products, etc.)
            "Green Apple",
            "Lavender",
            "Fresh Linen",
            "Ocean Breeze",
            "Lemon",
            "Unscented",
            # Product lines / variants
            "Black Label",
            "Gold Label",
            "Pulp Free",
            "With Pulp",
            "Extra Pulp",
            "No Pulp",
            "Light Flavour",
            "Light Flavor",
            "Organics",
            "Organic",
        ], key=lambda x: -len(x)),

        "modifier": sorted([
            "No Added Sugar",
            "Sugar Free",
            "Low Sugar",
            "Bundle",
            "Multipack",
            "Value Pack",
            "Family Pack",
        ], key=lambda x: -len(x)),

        # NOTE: Size and Quantity are detected via regex in title_parser.py
        # NOTE: No color for groceries - "Green" in "Green Curry" is part of product name

        "origin": sorted([
            "United States",
            "Australia",
            "New Zealand",
            "USA",
            "Made in Australia",
            "Product of Australia",
            "Imported",
        ], key=lambda x: -len(x)),
    },
}


# Category detection keywords and brands
CATEGORY_INDICATORS = {
    "groceries": {
        "keywords": [
            # Meat
            "chicken", "beef", "pork", "lamb", "mince", "fillet", "steak", "bacon",
            "sausage", "roast", "drumstick", "thigh", "breast",
            # Seafood
            "salmon", "prawns", "fish", "tuna", "seafood",
            # Dairy
            "milk", "cheese", "yoghurt", "yogurt", "butter", "cream", "eggs",
            # Produce
            "apples", "oranges", "bananas", "potato", "tomato", "onion", "carrot",
            "lettuce", "spinach", "broccoli", "avocado", "mango", "grapes",
            # Drinks
            "juice", "water", "soft drink", "beer", "wine", "cordial",
            # Pantry
            "bread", "pasta", "rice", "cereal", "biscuits", "chips", "snack",
            # Pet
            "dog food", "cat food", "pet food",
            # Cleaning/Baby
            "nappies", "diapers", "wipes", "detergent",
        ],
        "brands": [
            "woolworths", "coles", "aldi", "harris farm", "golden circle",
            "daily juice", "juice co", "arnott", "black hawk",
        ],
    },
    "sportswear": {
        "keywords": [
            "shoes", "sneakers", "running", "shorts", "jersey", "jacket",
            "pants", "leggings", "sports bra", "socks", "t-shirt", "tee",
            "hoodie", "tracksuit", "trainers", "cleats", "boots",
        ],
        "brands": [
            "nike", "adidas", "puma", "reebok", "asics", "new balance",
            "under armour", "the north face", "lululemon", "gymshark",
            "hoka", "brooks", "saucony", "fila", "converse", "vans",
            "black pepper",  # Clothing brand
        ],
    },
    "baby": {
        "keywords": [
            "baby bottle", "sippy cup", "formula", "sterilizer", "breast pump",
            "bottle warmer", "pacifier", "teether", "bib", "highchair",
            "stroller", "pram", "cot", "crib", "baby monitor",
            "lunch box", "lunchbox", "drink bottle", "water bottle", "bento",
            "backpack", "cooler bag", "ice pack",
        ],
        "brands": [
            "tommee tippee", "philips avent", "dr. brown", "dr brown",
            "baby brezza", "munchkin", "skip hop", "nuk", "mam", "pigeon",
            "medela", "spectra", "haakaa", "comotomo", "b.box", "bbox",
            "sistema", "thermos", "smiggle", "yumbox", "bentgo", "omiebox",
            "flowfly", "hydro flask", "camelbak", "contigo",
        ],
    },
}


def detect_category(title: str) -> str:
    """
    Auto-detect product category based on title keywords and brands.
    Returns the most likely category or 'all' if uncertain.
    """
    title_lower = title.lower()
    scores = {"groceries": 0, "sportswear": 0, "baby": 0}

    for category, indicators in CATEGORY_INDICATORS.items():
        # Check keywords
        for keyword in indicators["keywords"]:
            if keyword in title_lower:
                scores[category] += 2  # Keywords are strong indicators

        # Check brands
        for brand in indicators["brands"]:
            if brand in title_lower:
                scores[category] += 3  # Brands are stronger indicators

    # Find category with highest score
    max_score = max(scores.values())
    if max_score >= 2:  # Minimum threshold
        return max(scores, key=scores.get)

    return "all"  # Uncertain, use combined attributes


# Brands to exclude from matching in specific categories
BRAND_EXCLUSIONS = {
    "groceries": ["Black Pepper"],  # It's a seasoning, not clothing brand
}


def get_brands_for_category(category: str) -> list:
    """Get brands list filtered for the specific category."""
    if category in BRAND_EXCLUSIONS:
        exclusions = [b.lower() for b in BRAND_EXCLUSIONS[category]]
        return [b for b in BRANDS if b.lower() not in exclusions]
    return BRANDS


def get_category_attributes(category: str) -> dict:
    """Get attributes for a specific category."""
    if category == "all":
        # Combine all categories
        combined = {}
        for cat_attrs in ATTRIBUTES.values():
            for attr_type, values in cat_attrs.items():
                if attr_type not in combined:
                    combined[attr_type] = []
                # Add values, avoiding duplicates
                for v in values:
                    if v not in combined[attr_type]:
                        combined[attr_type].append(v)
        # Re-sort each attribute list by length (longest first)
        for attr_type in combined:
            combined[attr_type] = sorted(combined[attr_type], key=lambda x: -len(x))
        return combined
    return ATTRIBUTES.get(category, {})


def get_all_attribute_types(category: str) -> list:
    """Get list of attribute types for a category."""
    return list(ATTRIBUTES.get(category, {}).keys())
