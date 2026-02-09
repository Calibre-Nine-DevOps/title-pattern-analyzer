"""
Title Pattern Analysis Dashboard
Analyzes product title patterns from Google Shopping scrape data.
"""
import streamlit as st
import pandas as pd
from utils.title_parser import parse_title

# Page config
st.set_page_config(
    page_title="Title Pattern Analysis",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def load_data(uploaded_file) -> pd.DataFrame:
    """Load and prepare the CSV data."""
    df = pd.read_csv(uploaded_file)
    return df


@st.cache_data
def analyze_patterns(df_hash: str, titles: list, positions: list, keywords: list, category: str) -> pd.DataFrame:
    """Parse titles and analyze patterns."""
    parsed_results = []
    for i, title in enumerate(titles):
        result = parse_title(title, category)
        parsed_results.append({
            'title': title,
            'position': positions[i] if i < len(positions) else 0,
            'keyword': keywords[i] if keywords and i < len(keywords) else '',
            'pattern': result['pattern'],
            'attributes': result['attributes'],
            'attribute_types': [attr['type'] for attr in result['attributes']],
        })

    return pd.DataFrame(parsed_results)


def calculate_pattern_stats(parsed_df: pd.DataFrame, total_shopping_results: int = 40) -> pd.DataFrame:
    """
    Calculate statistics for each pattern.

    Performance % = what percentage of competitors you're outranking
    Based on typical Google Shopping showing ~40 results.
    """
    total_listings = len(parsed_df)

    pattern_stats = parsed_df.groupby('pattern').agg({
        'title': 'count',
        'position': 'mean',
    }).reset_index()

    pattern_stats.columns = ['pattern', 'count', 'avg_position']

    # Usage % = what percentage of listings use this pattern
    pattern_stats['usage_pct'] = (pattern_stats['count'] / total_listings * 100).round(1)

    # Performance % = what percentage of results are you ranking above
    # Position 1 = above 97.5%, Position 10 = above 75%
    pattern_stats['performance_pct'] = (
        (1 - pattern_stats['avg_position'] / total_shopping_results) * 100
    ).round(1)
    pattern_stats['performance_pct'] = pattern_stats['performance_pct'].clip(0, 100)

    pattern_stats = pattern_stats.sort_values('count', ascending=False)

    return pattern_stats


def get_popular_attributes(parsed_df: pd.DataFrame) -> dict:
    """Get most common attributes across all titles."""
    all_attrs = []
    for attrs in parsed_df['attribute_types']:
        all_attrs.extend(attrs)

    attr_counts = pd.Series(all_attrs).value_counts()
    return attr_counts.to_dict()


def format_attribute_tags(attributes: list) -> str:
    """Format attributes as colored tags for display."""
    colors = {
        'Brand': '#ef4444',        # red
        'Product Type': '#3b82f6', # blue
        'Variant': '#8b5cf6',      # purple
        'Size': '#10b981',         # green
        'Quantity': '#f59e0b',     # amber
        'Gender': '#ec4899',       # pink
        'Sport': '#06b6d4',        # cyan
        'Color': '#6366f1',        # indigo
        'Model': '#6b7280',        # gray
    }

    tags = []
    for attr in attributes:
        color = colors.get(attr['type'], '#6b7280')
        tags.append(f":`{color}`[**{attr['type']}:** {attr['value']}]")

    return " ".join(tags)


def render_pattern_card(pattern: str, stats: dict, examples: pd.DataFrame, total_listings: int):
    """Render a pattern analysis card using native Streamlit components."""
    with st.container():
        # Header row with badges
        col1, col2, col3, col4 = st.columns([1, 1, 2, 2])

        with col1:
            st.markdown(f"🔴 **{stats['usage_pct']:.0f}% Usage**")
        with col2:
            st.markdown(f"🟢 **{stats['performance_pct']:.0f}% Performance**")
        with col4:
            st.markdown(f"*{stats['count']} of {total_listings} listings*")

        # Formula
        st.markdown(f"**FORMULA:** {pattern}")
        st.caption(f"Avg. Position: {stats['avg_position']:.1f}")

        # Example listings with attribute breakdown
        for _, row in examples.head(3).iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{row['title']}**")
                # Show keyword tag if available
                keyword = row.get('keyword', '')
                if keyword:
                    st.caption(f"🏷️ Keyword: `{keyword}`")
                # Show attribute breakdown
                attributes = row.get('attributes', [])
                if attributes:
                    attr_display = " → ".join([f"`{attr['type']}: {attr['value']}`" for attr in attributes])
                    st.caption(attr_display)
            with col2:
                st.markdown(f"Position: **{row['position']}**")

        if len(examples) > 3:
            remaining = len(examples) - 3
            with st.expander(f"View more ({remaining} more listings)"):
                # Limit to 50 more to prevent timeout
                for _, row in examples.iloc[3:53].iterrows():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**{row['title']}**")
                        # Show keyword tag if available
                        keyword = row.get('keyword', '')
                        if keyword:
                            st.caption(f"🏷️ Keyword: `{keyword}`")
                        attributes = row.get('attributes', [])
                        if attributes:
                            attr_display = " → ".join([f"`{attr['type']}: {attr['value']}`" for attr in attributes])
                            st.caption(attr_display)
                    with col2:
                        st.markdown(f"Position: **{row['position']}**")
                if remaining > 50:
                    st.caption(f"...and {remaining - 50} more (export CSV for full list)")

        st.divider()


# Main app
def main():
    st.title("📊 Title Pattern Analysis")
    st.caption("ATTRIBUTES AND KEYWORD VALUES")

    # Sidebar for file upload and settings
    with st.sidebar:
        st.header("Settings")

        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])

        category = st.selectbox(
            "Product Category",
            options=['auto', 'all', 'baby', 'sportswear', 'groceries'],
            format_func=lambda x: "Auto-Detect" if x == "auto" else x.title()
        )

        st.divider()
        st.markdown("### How it works")
        st.markdown("""
        1. Upload your scrape data CSV
        2. Select the product category
        3. View pattern analysis

        The tool extracts attributes like brand,
        product type, size, etc. and identifies
        common patterns in successful listings.
        """)

    if uploaded_file is not None:
        # Load data
        df = load_data(uploaded_file)

        st.success(f"Loaded {len(df)} listings")

        # Show keyword filter if available
        selected_keyword = 'All'
        if 'keyword' in df.columns:
            keywords = ['All'] + list(df['keyword'].unique())
            selected_keyword = st.selectbox("Filter by Keyword", keywords)
            if selected_keyword != 'All':
                df = df[df['keyword'] == selected_keyword]

        # Deduplicate option - average position for same title
        deduplicate = st.checkbox("Deduplicate titles (average position)", value=True)
        if deduplicate:
            # Group by title, average the position
            df = df.groupby('title').agg({
                'position': 'mean',
                **{col: 'first' for col in df.columns if col not in ['title', 'position']}
            }).reset_index()
            df['position'] = df['position'].round(1)

        # Show filtered count
        if selected_keyword != 'All':
            st.info(f"Analyzing {len(df)} listings for keyword: **{selected_keyword}**")

        # Analyze patterns
        # Create cache key from filter settings
        df_hash = f"{selected_keyword}_{category}_{deduplicate}_{len(df)}"

        with st.spinner("Analyzing title patterns..."):
            # Pass lists for proper caching (underscore-prefixed params are not hashed)
            titles = df['title'].tolist()
            positions = df['position'].tolist()
            keywords = df['keyword'].tolist() if 'keyword' in df.columns else []

            parsed_df = analyze_patterns(df_hash, titles, positions, keywords, category)
            pattern_stats = calculate_pattern_stats(parsed_df)
            popular_attrs = get_popular_attributes(parsed_df)

        # Popular Attributes Section
        st.header("Popular Title Attributes")
        st.markdown("Most commonly used product category attributes in Merchant Listing Titles within the Shopping Tab results")

        # Display popular attributes as tags
        attr_list = list(popular_attrs.keys())[:6]
        attr_text = ", ".join([f"**[{attr}]**" for attr in attr_list])

        st.info(f"**ANALYSIS:** The most popular attributes in product titles are {attr_text}. "
                "Ensure your relevant products have titles that include these attributes for better visibility.")

        st.divider()

        # Title Pattern Analysis Section
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.header("Title Pattern Analysis")
            st.markdown("Most popular title attribute patterns of Merchant Listings within the Shopping Tab results")
        with col2:
            sort_by = st.selectbox(
                "Sort by",
                options=['usage', 'performance', 'count'],
                format_func=lambda x: x.title()
            )
        with col3:
            # Export button
            csv = parsed_df.to_csv(index=False)
            st.download_button(
                label="📥 Export Raw",
                data=csv,
                file_name="pattern_analysis.csv",
                mime="text/csv"
            )

        # Sort pattern stats based on selection
        if sort_by == 'usage':
            pattern_stats = pattern_stats.sort_values('usage_pct', ascending=False)
        elif sort_by == 'performance':
            pattern_stats = pattern_stats.sort_values('performance_pct', ascending=False)
        else:  # count
            pattern_stats = pattern_stats.sort_values('count', ascending=False)

        # Pagination - show limited patterns per page
        patterns_per_page = 20
        total_patterns = len(pattern_stats)
        total_pages = (total_patterns + patterns_per_page - 1) // patterns_per_page

        page = st.number_input(
            f"Page (1-{total_pages})",
            min_value=1,
            max_value=max(1, total_pages),
            value=1,
            step=1
        )

        start_idx = (page - 1) * patterns_per_page
        end_idx = start_idx + patterns_per_page
        pattern_stats_page = pattern_stats.iloc[start_idx:end_idx]

        st.caption(f"Showing patterns {start_idx + 1}-{min(end_idx, total_patterns)} of {total_patterns}")

        # Display each pattern
        total_listings = len(parsed_df)

        for _, row in pattern_stats_page.iterrows():
            pattern = row['pattern']
            examples = parsed_df[parsed_df['pattern'] == pattern]

            stats = {
                'usage_pct': row['usage_pct'],
                'performance_pct': row['performance_pct'],
                'count': int(row['count']),
                'avg_position': row['avg_position'],
            }

            render_pattern_card(pattern, stats, examples, total_listings)

        # Additional insights
        st.divider()
        st.header("Insights")

        col1, col2, col3 = st.columns(3)

        with col1:
            best_pattern = pattern_stats.iloc[0]
            st.metric(
                "Most Common Pattern",
                f"{best_pattern['usage_pct']:.0f}% Usage",
                f"Avg Position: {best_pattern['avg_position']:.1f}"
            )

        with col2:
            best_performing = pattern_stats.loc[pattern_stats['avg_position'].idxmin()]
            st.metric(
                "Best Performing Pattern",
                f"Position {best_performing['avg_position']:.1f}",
                f"{best_performing['usage_pct']:.0f}% of listings"
            )

        with col3:
            st.metric(
                "Total Patterns Found",
                len(pattern_stats),
                f"Across {total_listings} listings"
            )

    else:
        # Show demo/instructions when no file uploaded
        st.divider()
        st.markdown("### 👈 Upload a CSV file to get started")
        st.markdown("""
        Your CSV should have at least these columns:
        - `title` - Product title
        - `position` - Ranking position in search results

        Optional columns:
        - `keyword` - Search keyword
        - `merchant` - Merchant name
        - `price` - Product price
        """)

        # Show sample data format
        st.markdown("### Sample Data Format")
        sample_data = pd.DataFrame({
            'title': [
                'Tommee Tippee Natural Start Baby Bottles 260ml 3 Pack',
                'Philips Avent Anti-Colic Baby Bottles 260ml',
                'Dr Browns Options+ Wide Neck Bottles 270ml 2 Pack'
            ],
            'position': [1, 2, 3],
            'keyword': ['Bottle Feeding', 'Bottle Feeding', 'Bottle Feeding'],
            'merchant': ['Chemist Warehouse', 'Baby Bunting', 'Amazon AU'],
            'price': [20.96, 24.95, 29.99]
        })
        st.dataframe(sample_data)


if __name__ == "__main__":
    main()
