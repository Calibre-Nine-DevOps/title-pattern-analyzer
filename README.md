# Title Pattern Analysis Dashboard

Analyzes product title patterns from Google Shopping scrape data to identify what title structures perform best.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Or if streamlit is not in PATH:
```bash
python -m streamlit run app.py
```

## Usage

1. Upload your CSV file with columns:
   - `title` - Product title (required)
   - `position` - Search result position (required)
   - `keyword` - Search keyword (optional)
   - `merchant` - Merchant name (optional)
   - `price` - Product price (optional)

2. Select the product category (baby, sportswear, groceries)

3. View the pattern analysis

## Adding New Attributes

Edit `config/attributes.py` to add:
- New brands to `BRANDS` list
- New category-specific attributes in `ATTRIBUTES` dict

## How Pattern Detection Works

1. Parses each title to extract known attributes (brand, product type, variant, size, etc.)
2. Records the ORDER in which attributes appear
3. Groups titles by their attribute pattern
4. Calculates usage % and average position for each pattern

Example:
```
"Tommee Tippee Natural Start Baby Bottles 260ml 3 Pack"

Pattern: [Brand] + [Variant] + [Product Type] + [Size] + [Quantity]
```
