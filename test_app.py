#!/usr/bin/env python3
"""
Simple test script to verify the dashboard app works correctly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import load_data
import pandas as pd

def test_data_loading():
    """Test that data loads correctly"""
    print("Testing data loading...")
    df = load_data()
    
    if df.empty:
        print("ERROR: No data loaded")
        return False
    
    print(f"SUCCESS: Loaded {len(df)} records")
    print(f"   - Columns: {list(df.columns)}")
    print(f"   - Equipment types: {df['equipmentType'].nunique()}")
    print(f"   - Companies: {df['companyName'].nunique()}")
    print(f"   - Date range: {df['posted_date'].min()} to {df['posted_date'].max()}")
    
    return True

def test_data_processing():
    """Test data processing functions"""
    print("\nTesting data processing...")
    df = load_data()
    
    # Test rate conversion
    if 'rate_dollars' in df.columns:
        print("SUCCESS: Rate conversion working")
    else:
        print("ERROR: Rate conversion failed")
        return False
    
    # Test route creation
    if 'route' in df.columns:
        print("SUCCESS: Route creation working")
    else:
        print("ERROR: Route creation failed")
        return False
    
    # Test date conversion
    if 'posted_date' in df.columns:
        print("SUCCESS: Date conversion working")
    else:
        print("ERROR: Date conversion failed")
        return False
    
    return True

if __name__ == "__main__":
    print("NextLoad Dashboard Test")
    print("=" * 50)
    
    success = True
    success &= test_data_loading()
    success &= test_data_processing()
    
    print("\n" + "=" * 50)
    if success:
        print("ALL TESTS PASSED! Dashboard is ready to run.")
        print("\nTo run the dashboard:")
        print("   python -m streamlit run app.py")
        print("   or")
        print("   streamlit run app.py")
    else:
        print("SOME TESTS FAILED! Please check the errors above.")
    
    sys.exit(0 if success else 1)
