"""
Quick Start Interactive CSV Analyzer
Run with sample data for demonstration
"""
from main import InteractiveCSVAnalyzer
import os

def quick_demo():
    """Quick demonstration with sample data"""
    print("🚀 QUICK DEMO - Interactive CSV Analyzer")
    print("=" * 50)
    
    # Check if sample data exists
    if not os.path.exists('sample_cars.csv'):
        print("❌ Sample data not found. Please run main.py first.")
        return
    
    # Create analyzer
    analyzer = InteractiveCSVAnalyzer()
    
    print("💡 DEMO COMMANDS TO TRY:")
    print("   analyze price distribution")
    print("   visualize make vs price")
    print("   explore mileage patterns")
    print("   summary")
    print("")
    
    # Start interactive session
    analyzer.interactive_session('sample_cars.csv')

if __name__ == "__main__":
    quick_demo()
