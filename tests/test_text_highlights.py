#!/usr/bin/env python3
"""
Test script for Basketball Text Highlights Generator

This script demonstrates the use of the TextHighlightExtractor class
with a sample basketball game URL.
"""

from text_highlight_extractor import TextHighlightExtractor

def main():
    """
    Test the TextHighlightExtractor with a sample basketball game URL.
    
    Note: Replace the example URL with an actual basketball game page containing
    play-by-play data before running this test.
    """
    # Example URL - replace with an actual basketball game URL
    sample_url = "https://www.example.com/basketball/game/12345/play-by-play"
    
    # Test different output formats
    print("\n--- Testing Text Output ---")
    text_extractor = TextHighlightExtractor(
        url=sample_url,
        output_format="text"
    )
    text_extractor.run()
    
    print("\n--- Testing JSON Output ---")
    json_extractor = TextHighlightExtractor(
        url=sample_url,
        output_format="json",
        output_file="highlights.json"
    )
    json_extractor.run()
    
    print("\n--- Testing CSV Output ---")
    csv_extractor = TextHighlightExtractor(
        url=sample_url,
        output_format="csv",
        output_file="highlights.csv"
    )
    csv_extractor.run()
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    main() 