"""
🚀 Interactive CSV Analyzer Launcher
Choose from multiple analysis modes and tools
"""
import os
import sys

def print_banner():
    """Print welcome banner"""
    print("\n" + "🚀" * 60)
    print("🎯 INTERACTIVE CSV DATA ANALYZER SUITE")
    print("🔬 Powered by E2B Code Interpreter + OpenAI GPT-4")
    print("💡 Based on E2B Cookbook Best Practices")
    print("🚀" * 60)

def print_menu():
    """Print main menu options"""
    print("\n📋 AVAILABLE TOOLS:")
    print("=" * 50)
    print("1. 🤖 Interactive Analyzer    - Chat-based analysis")
    print("2. ⚡ Quick Demo             - Demo with sample data")
    print("3. 🤖 Automated Analysis     - Comprehensive auto-analysis")
    print("4. 📁 Session Manager        - Manage saved sessions")
    print("5. 🔧 Setup Check           - Verify environment")
    print("6. 📚 View Documentation     - Show command reference")
    print("7. 🚪 Exit                  - Exit launcher")
    print("=" * 50)

def check_setup():
    """Check if environment is properly configured"""
    print("\n🔧 ENVIRONMENT SETUP CHECK:")
    print("-" * 40)
    
    issues = []
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        issues.append("Create .env file with API keys")
    else:
        print("✅ .env file found")
        
        # Check API keys
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        e2b_key = os.getenv('E2B_API_KEY')
        
        if not openai_key:
            print("❌ OPENAI_API_KEY not set")
            issues.append("Add OPENAI_API_KEY to .env file")
        else:
            print("✅ OPENAI_API_KEY configured")
            
        if not e2b_key:
            print("❌ E2B_API_KEY not set") 
            issues.append("Add E2B_API_KEY to .env file")
        else:
            print("✅ E2B_API_KEY configured")
    
    # Check dependencies
    required_packages = [
        'openai', 'e2b_code_interpreter', 
        'dotenv', 'matplotlib', 'pandas'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            issues.append(f"Install {package}")
    
    # Check sample data
    if os.path.exists('sample_cars.csv'):
        print("✅ Sample data available")
    else:
        print("⚠️ Sample data not found (optional)")
        
    if issues:
        print(f"\n🔧 SETUP ISSUES TO FIX:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n💡 Fix these issues before using the analyzer")
        return False
    else:
        print("\n🎉 Environment setup is complete!")
        return True

def show_documentation():
    """Show command documentation"""
    print("\n📚 INTERACTIVE COMMAND REFERENCE:")
    print("=" * 50)
    
    commands = [
        ("analyze [question]", "Ask specific analysis questions", "analyze price distribution"),
        ("visualize [request]", "Create visualizations", "visualize correlation heatmap"),
        ("explore [aspect]", "Explore data aspects", "explore missing values"),
        ("summary", "Generate comprehensive overview", "summary"),
        ("history", "Show session history", "history"),
        ("save [filename]", "Save current session", "save my_analysis"),
        ("load [filename]", "Load previous session", "load my_analysis"),
        ("clear", "Clear analysis context", "clear"),
        ("help", "Show command help", "help"),
        ("exit", "Exit analyzer", "exit")
    ]
    
    for cmd, desc, example in commands:
        print(f"📝 {cmd:<20} - {desc}")
        print(f"   Example: {example}")
        print()
        
    print("💡 TIPS:")
    print("- Use natural language for questions")
    print("- Sessions are automatically saved with timestamps")
    print("- All visualizations are saved as PNG files")
    print("- Context is maintained across interactions")

def run_interactive():
    """Run interactive analyzer"""
    print("\n🤖 Starting Interactive Analyzer...")
    try:
        from main import main
        main()
    except Exception as e:
        print(f"❌ Error running interactive analyzer: {e}")

def run_quick_demo():
    """Run quick demo"""
    print("\n⚡ Starting Quick Demo...")
    try:
        from quick_demo import quick_demo
        quick_demo()
    except Exception as e:
        print(f"❌ Error running quick demo: {e}")

def run_automated():
    """Run automated analysis"""
    print("\n🤖 Starting Automated Analysis...")
    try:
        from auto_analysis import main
        main()
    except Exception as e:
        print(f"❌ Error running automated analysis: {e}")

def run_session_manager():
    """Run session manager"""
    print("\n📁 Starting Session Manager...")
    try:
        from session_manager import main
        main()
    except Exception as e:
        print(f"❌ Error running session manager: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    while True:
        print_menu()
        
        try:
            choice = input("\n🎯 Select option (1-7): ").strip()
            
            if choice == '1':
                run_interactive()
            elif choice == '2':
                run_quick_demo()
            elif choice == '3':
                run_automated()
            elif choice == '4':
                run_session_manager()
            elif choice == '5':
                check_setup()
            elif choice == '6':
                show_documentation()
            elif choice == '7':
                print("\n👋 Goodbye! Thanks for using Interactive CSV Analyzer!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n\n⚡ Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            
        input("\n📱 Press Enter to continue...")

if __name__ == "__main__":
    main()
