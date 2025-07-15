"""
Automated Analysis Runner
Runs a series of pre-defined analysis tasks
"""
from main import InteractiveCSVAnalyzer
import time
import os

class AutoAnalyzer:
    def __init__(self, csv_path):
        self.analyzer = InteractiveCSVAnalyzer()
        self.csv_path = csv_path
        
    def run_automated_analysis(self):
        """Run comprehensive automated analysis"""
        print("🤖 AUTOMATED ANALYSIS MODE")
        print("=" * 50)
        
        if not self.analyzer.create_sandbox():
            return
            
        if not self.analyzer.upload_dataset(self.csv_path):
            return
            
        # Pre-defined analysis tasks
        tasks = [
            ("📊 Dataset Overview", "summary"),
            ("🔍 Data Quality Check", "explore missing values and data quality"),
            ("📈 Distribution Analysis", "visualize distributions of all numerical columns"),
            ("🔗 Correlation Analysis", "analyze correlations between variables with heatmap"),
            ("🎯 Key Insights", "analyze key patterns and provide actionable insights"),
            ("📋 Final Report", "generate comprehensive analysis report with key findings")
        ]
        
        print(f"\n🚀 Running {len(tasks)} automated analysis tasks...")
        
        for i, (description, task) in enumerate(tasks, 1):
            print(f"\n{i}/{len(tasks)} {description}")
            print("-" * 40)
            
            if task == "summary":
                self.analyzer.handle_summary_command()
            elif task.startswith("explore"):
                self.analyzer.handle_explore_command(task[8:])
            elif task.startswith("visualize"):
                self.analyzer.handle_visualize_command(task[10:])
            elif task.startswith("analyze"):
                self.analyzer.handle_analyze_command(task[8:])
            else:
                # Generic analysis
                code = self.analyzer.chat_with_ai(task)
                if code:
                    self.analyzer.execute_code(code)
            
            time.sleep(2)  # Brief pause between tasks
            
        print("\n🎉 AUTOMATED ANALYSIS COMPLETE!")
        print("=" * 50)
        print("📁 Check generated files for visualizations")
        print("📜 Use 'history' command to see all completed tasks")
        
        # Save session automatically
        auto_filename = f"auto_analysis_{int(time.time())}"
        self.analyzer.handle_save_command(auto_filename)
        
        # Cleanup
        if self.analyzer.sandbox:
            self.analyzer.sandbox.kill()

def main():
    """Run automated analysis"""
    csv_path = input("📁 Enter CSV file path for automated analysis: ").strip().strip('"\'')
    
    if csv_path.lower() == 'demo':
        csv_path = 'sample_cars.csv'
    
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return
        
    auto_analyzer = AutoAnalyzer(csv_path)
    auto_analyzer.run_automated_analysis()

if __name__ == "__main__":
    main()
