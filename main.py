import os
import time
import json
import base64
try:
    import readline  # For enhanced input on Unix systems
except ImportError:
    pass  # readline not available on Windows, but input() still works
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
from openai import OpenAI

# Load environment variables
load_dotenv()

class InteractiveCSVAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.e2b_api_key = os.getenv("E2B_API_KEY")
        self.sandbox = None
        self.session_history = []
        self.analysis_context = ""
        self.current_dataset_info = {}
        self.conversation_log = []
        self.current_dataset_path = None  # Track current dataset for sandbox recovery
        
    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "🚀" * 50)
        print("🎯 INTERACTIVE CSV DATA ANALYZER")
        print("🔬 Powered by E2B Code Interpreter + OpenAI GPT-4")
        print("💡 Based on E2B Cookbook Best Practices")
        print("🚀" * 50)
        
    def print_help(self):
        """Print available commands"""
        print("\n📋 INTERACTIVE COMMANDS:")
        print("  📊 'analyze [question]' - Ask specific analysis questions")
        print("  🔄 'analyze auto [topic]' - ITERATIVE analysis (builds step by step)")
        print("  📈 'visualize [request]' - Create specific visualizations") 
        print("  🔍 'explore [aspect]' - Explore specific data aspects")
        print("  📋 'summary' - ITERATIVE comprehensive summary (15+ steps)")
        print("  🤖 'autorun [prompt]' - Custom iterative analysis session")
        print("  � 'iterate [prompt]' - Force iterative mode for any analysis")
        print("  �📜 'history' - Show conversation history")
        print("  💾 'save [filename]' - Save current session")
        print("  📁 'load [filename]' - Load previous session")
        print("  🗑️'clear' - Clear analysis context")
        print("  ❓ 'help' - Show this help menu")
        print("  🚪 'exit' - Exit the analyzer")
        print("  " + "-" * 50)
        print("  🔄 AUTO-ITERATIVE: Commands with 'complex', 'comprehensive',")
        print("     'complete', 'full', 'deep' automatically trigger iterations!")
        print("  📝 Examples:")
        print("     'complex data analysis' → Auto-iterates 12+ steps")
        print("     'comprehensive heart disease analysis' → Auto-iterates")
        print("     'iterate explore patterns' → Forced iterative mode")
        
    def create_sandbox(self):
        """Initialize E2B sandbox with proper error handling"""
        try:
            print("🔧 Initializing E2B Code Interpreter sandbox...")
            self.sandbox = Sandbox(api_key=self.e2b_api_key)
            print("✅ Sandbox initialized successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize sandbox: {e}")
            print("💡 Please check your E2B_API_KEY in .env file")
            return False
    
    def upload_dataset(self, file_path: str) -> bool:
        """Upload CSV dataset to E2B sandbox"""
        try:
            print(f"📁 Uploading dataset: {os.path.basename(file_path)}")
            
            with open(file_path, "rb") as f:
                file_content = f.read()
                
            if len(file_content) == 0:
                print(f"❌ File is empty: {file_path}")
                return False
                
            # Upload with standard name for consistency
            remote_path = self.sandbox.files.write("data.csv", file_content)
            print(f"✅ Dataset uploaded successfully!")
            
            # Track the dataset path for potential recovery
            self.current_dataset_path = file_path
            
            # Get initial dataset info
            self._get_dataset_info()
            return True
            
        except Exception as e:
            print(f"❌ Failed to upload dataset: {e}")
            return False
    
    def _get_dataset_info(self):
        """Get basic information about the uploaded dataset"""
        try:
            code = """
import pandas as pd
import numpy as np

# Load and inspect the dataset
df = pd.read_csv('data.csv')

# Basic info
info = {
    'shape': df.shape,
    'columns': list(df.columns),
    'dtypes': df.dtypes.to_dict(),
    'missing_values': df.isnull().sum().to_dict(),
    'memory_usage': df.memory_usage(deep=True).sum()
}

print("📊 DATASET OVERVIEW:")
print(f"   📐 Shape: {info['shape'][0]} rows × {info['shape'][1]} columns")
print(f"   📝 Columns: {', '.join(info['columns'])}")
print(f"   💾 Memory: {info['memory_usage'] / 1024:.1f} KB")

# Show data types
print("\\n🏷️ DATA TYPES:")
for col, dtype in info['dtypes'].items():
    missing = info['missing_values'][col]
    missing_pct = (missing / info['shape'][0]) * 100 if info['shape'][0] > 0 else 0
    print(f"   {col}: {dtype} (Missing: {missing}/{missing_pct:.1f}%)")

# Preview first few rows
print("\\n👀 PREVIEW (First 3 rows):")
print(df.head(3).to_string())
"""
            
            execution = self.sandbox.run_code(code)
            if execution.logs:
                print("\n" + str(execution.logs))
                
            # Store dataset info in memory
            self.current_dataset_info = {
                'uploaded_at': datetime.now().isoformat(),
                'analysis_ready': True
            }
            
        except Exception as e:
            print(f"⚠️ Could not retrieve dataset info: {e}")

    def chat_with_ai(self, user_message: str, context: str = "", is_continuation: bool = False) -> str:
        """Enhanced AI chat with better prompting"""
        try:
            full_context = f"{self.analysis_context}\n{context}" if context else self.analysis_context
            
            if is_continuation:
                system_prompt = """You are an expert data scientist conducting step-by-step analysis.

DATASET INFO: The dataset is already uploaded and available as 'data.csv' in the sandbox.

RESPONSE FORMAT - You must respond with EXACTLY this structure:

EXPLANATION: [1-2 sentences explaining what you'll do in this step and why]

CODE:
```python
[Small focused code block for this specific step]
```

ANALYSIS RULES:
- Each step should be SMALL and focused on ONE specific aspect
- Continue unless you've thoroughly analyzed the data from multiple angles
- Only respond "ANALYSIS_COMPLETE" when you've covered all major aspects
- Build upon previous findings logically
- ALWAYS use 'data.csv' as the filename - the dataset is already uploaded
- For visualizations: use plt.savefig('step_X_description.png') and plt.close()
- DO NOT create directories - they already exist
- Focus on different analysis each step: stats → correlations → distributions → patterns → insights

PREVIOUS CONTEXT: {context}""".format(context=full_context)
            else:
                system_prompt = """You are an expert data scientist conducting step-by-step analysis.

DATASET INFO: The dataset is already uploaded and available as 'data.csv' in the sandbox.

RESPONSE FORMAT - You must respond with EXACTLY this structure:

EXPLANATION: [1-2 sentences explaining what you'll do in this step and why]

CODE:
```python
[Small focused code block for this specific step]
```

ANALYSIS RULES:
- Each step should be SMALL and focused on ONE specific aspect  
- Start with basic data exploration
- ALWAYS use 'data.csv' as the filename - the dataset is already uploaded
- For visualizations: use plt.savefig('step_X_description.png') and plt.close()
- DO NOT create directories - they already exist
- Include clear print statements explaining what you're doing
- Progress through: basic stats → correlations → distributions → patterns → insights

CONTEXT: {context}""".format(context=full_context)

            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            
            code = response.choices[0].message.content.strip()
            
            # Check if analysis is complete
            if "ANALYSIS_COMPLETE" in code:
                return "ANALYSIS_COMPLETE"
            
            return code
            
        except Exception as e:
            print(f"❌ AI request failed: {e}")
            return None
    
    def execute_with_automation(self, initial_prompt: str, max_iterations: int = 15, min_iterations: int = 3):
        """Execute analysis with intelligent iteration based on quality and completion"""
        print(f"\n🤖 INTELLIGENT ITERATIVE ANALYSIS")
        print("🧠 AI will determine when analysis is complete (no fixed iteration count)")
        print(f"📊 Safety limits: minimum {min_iterations}, maximum {max_iterations} iterations")
        print("🔄 Will continue until comprehensive analysis is achieved...")
        print("=" * 70)
        
        iteration = 0
        current_prompt = initial_prompt
        consecutive_failures = 0
        analysis_topics_covered = set()
        sandbox_reset_count = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n🔄 STEP {iteration} - ADAPTIVE ANALYSIS")
            print(f"🎯 Intelligently building comprehensive insights...")
            print("-" * 50)
            
            # Check sandbox health before proceeding
            if not self._check_sandbox_health():
                print("🔧 Sandbox issue detected - attempting recovery...")
                if self._reinitialize_sandbox():
                    sandbox_reset_count += 1
                    print(f"✅ Sandbox recovered (reset #{sandbox_reset_count})")
                else:
                    print("❌ Could not recover sandbox - stopping analysis")
                    break
            
            # Get AI response with completion detection
            is_continuation = iteration > 1
            ai_response = self.chat_with_ai(current_prompt, is_continuation=is_continuation)
            
            if not ai_response:
                consecutive_failures += 1
                print(f"❌ Failed to get AI response (failure #{consecutive_failures})")
                if consecutive_failures >= 3:
                    print("🛑 Multiple AI failures - stopping analysis")
                    break
                continue
            else:
                consecutive_failures = 0  # Reset failure counter
            
            # Check for intelligent completion signals
            completion_check = self._check_analysis_completion(ai_response, iteration, min_iterations, analysis_topics_covered)
            if completion_check["should_stop"]:
                print(f"🎉 ANALYSIS COMPLETE: {completion_check['reason']}")
                print("✅ Comprehensive analysis achieved through intelligent detection")
                break
            
            # Parse AI response for explanation and code
            explanation, code = self._parse_ai_response(ai_response)
            
            if explanation:
                print(f"🤖 AI Insight: {explanation}")
                # Track analysis topics
                self._track_analysis_topics(explanation, analysis_topics_covered)
            
            if not code:
                print("⚠️ No executable code received - requesting continuation")
                current_prompt = "Please provide executable Python code for the next analysis step."
                continue
                
            print(f"💻 Executing intelligent analysis step...")
            
            # Execute the code with enhanced error handling
            success, logs = self.execute_code(code)
            
            if not success:
                # Enhanced error handling for different error types
                error_handled = self._handle_execution_error(logs, iteration)
                if not error_handled:
                    consecutive_failures += 1
                    if consecutive_failures >= 2:
                        print("🛑 Multiple execution failures - stopping analysis")
                        break
                
            # Update context with results
            result_summary = str(logs)[:500] if logs else "No output"
            self._update_context(f"Step {iteration}: {result_summary}")
            
            # Intelligent progression - only wait if we're continuing
            if iteration < max_iterations and not completion_check["should_stop"]:
                print(f"\n⏳ Brief pause for AI reflection...")
                print(f"🧠 Analyzing results and planning next intelligent step...")
                time.sleep(3)  # Reduced wait time
            
            # Prepare intelligent prompt for next iteration
            current_prompt = self._generate_intelligent_prompt(iteration, logs, analysis_topics_covered)
            
        # Final analysis summary
        self._print_completion_summary(iteration, analysis_topics_covered, sandbox_reset_count)
        
        return iteration
    
    def execute_code(self, code: str) -> tuple[bool, Any]:
        """Execute code in E2B sandbox with enhanced result handling"""
        try:
            print("\n🔄 Executing analysis...")
            
            execution = self.sandbox.run_code(
                code,
                on_stderr=lambda stderr: print(f"⚠️ Warning: {stderr}"),
                on_stdout=lambda stdout: print(f"📊 {stdout}")
            )
            
            if execution.error:
                print(f"\n❌ Execution Error: {execution.error}")
                return False, execution.error
                
            # Handle results (images, data, etc.)
            if execution.results:
                print(f"\n📈 Generated {len(execution.results)} result(s)")
                self._save_results(execution.results)
                
            # Store execution in history
            self.session_history.append({
                'timestamp': datetime.now().isoformat(),
                'code': code,
                'logs': execution.logs,
                'success': True,
                'results_count': len(execution.results) if execution.results else 0
            })
            
            return True, execution.logs
            
        except Exception as e:
            print(f"❌ Code execution failed: {e}")
            return False, str(e)
    
    def _save_results(self, results):
        """Save visualization results to output folder"""
        saved_files = []
        output_dir = "output"
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        for i, result in enumerate(results, 1):
            if hasattr(result, 'png') and result.png:
                timestamp = datetime.now().strftime("%H%M%S")
                filename = os.path.join(output_dir, f"step_{timestamp}_{i}.png")
                
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(result.png))
                    
                saved_files.append(filename)
                print(f"   💾 Saved: {filename}")
                
            elif hasattr(result, 'jpg') and result.jpg:
                timestamp = datetime.now().strftime("%H%M%S")
                filename = os.path.join(output_dir, f"step_{timestamp}_{i}.jpg")
                
                with open(filename, 'wb') as f:
                    f.write(base64.b64decode(result.jpg))
                    
                saved_files.append(filename)
                print(f"   💾 Saved: {filename}")
        
        return saved_files
    
    def process_user_command(self, user_input: str) -> tuple[str, str]:
        """Process user commands and return action and parameters"""
        user_input = user_input.strip().lower()
        
        if user_input.startswith('analyze '):
            return 'analyze', user_input[8:]
        elif user_input.startswith('visualize '):
            return 'visualize', user_input[10:]
        elif user_input.startswith('explore '):
            return 'explore', user_input[8:]
        elif user_input.startswith('autorun '):
            return 'autorun', user_input[8:]
        elif user_input.startswith('iterate '):
            return 'iterate', user_input[8:]
        elif user_input.startswith('save '):
            return 'save', user_input[5:]
        elif user_input.startswith('load '):
            return 'load', user_input[5:]
        elif user_input in ['summary', 'help', 'history', 'clear', 'exit']:
            return user_input, ''
        else:
            return 'chat', user_input
            
    def handle_analyze_command(self, question: str):
        """Handle specific analysis questions with automation"""
        print(f"\n🔍 Analyzing: {question}")
        
        # Check if user wants automated analysis
        if "auto" in question.lower() or "automated" in question.lower():
            # Remove "auto" from the question for the prompt
            clean_question = question.replace("auto", "").replace("automated", "").strip()
            prompt = f"""
            START step-by-step analysis to explore: {clean_question}
            
            DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
            
            Begin with the first small step - basic data loading and structure overview using 'data.csv'.
            Use the new format with EXPLANATION and CODE sections.
            """
            iterations = self.execute_with_automation(prompt, max_iterations=20, min_iterations=3)
            self._update_context(f"Automated iterative analysis of '{question}' completed in {iterations} steps")
        else:
            # Single iteration analysis
            prompt = f"""
            Analyze the dataset to answer this specific question: {question}
            
            DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
            
            Use the format:
            EXPLANATION: [Brief explanation of your approach]
            CODE: [Python code to analyze the question using 'data.csv']
            
            Focus on directly answering the user's question with data-driven insights.
            """
            
            ai_response = self.chat_with_ai(prompt)
            if ai_response and ai_response != "ANALYSIS_COMPLETE":
                explanation, code = self._parse_ai_response(ai_response)
                
                if explanation:
                    print(f"🤖 AI Explanation: {explanation}")
                
                if code:
                    success, result = self.execute_code(code)
                    if success:
                        self._update_context(f"User asked: {question}. Analysis completed.")
                else:
                    print("❌ No executable code found in AI response")
            
    def handle_visualize_command(self, request: str):
        """Handle visualization requests"""
        print(f"\n📈 Creating visualization: {request}")
        
        prompt = f"""
        Create visualizations based on this request: {request}
        
        DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
        
        Use the format:
        EXPLANATION: [Brief explanation of the visualization approach]
        CODE: [Python code to create the visualization using 'data.csv']
        
        Generate appropriate charts, graphs, or plots that best represent the data.
        Use matplotlib and seaborn for professional visuals.
        Save visualizations to output folder with descriptive names.
        """
        
        ai_response = self.chat_with_ai(prompt)
        if ai_response and ai_response != "ANALYSIS_COMPLETE":
            explanation, code = self._parse_ai_response(ai_response)
            
            if explanation:
                print(f"🤖 AI Explanation: {explanation}")
            
            if code:
                success, result = self.execute_code(code)
                if success:
                    self._update_context(f"Created visualization: {request}")
            else:
                print("❌ No executable code found in AI response")
                
    def handle_explore_command(self, aspect: str):
        """Handle data exploration requests"""
        print(f"\n🔬 Exploring: {aspect}")
        
        prompt = f"""
        Explore this specific aspect of the dataset: {aspect}
        
        DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
        
        Use the format:
        EXPLANATION: [Brief explanation of the exploration approach]  
        CODE: [Python code to explore the data aspect using 'data.csv']
        
        Provide deep insights, patterns, anomalies, and interesting findings.
        Include both statistical analysis and visualizations where appropriate.
        """
        
        ai_response = self.chat_with_ai(prompt)
        if ai_response and ai_response != "ANALYSIS_COMPLETE":
            explanation, code = self._parse_ai_response(ai_response)
            
            if explanation:
                print(f"🤖 AI Explanation: {explanation}")
            
            if code:
                success, result = self.execute_code(code)
                if success:
                    self._update_context(f"Explored: {aspect}")
            else:
                print("❌ No executable code found in AI response")
                
    def handle_summary_command(self):
        """Generate comprehensive dataset summary with automation"""
        print("\n📋 Generating comprehensive summary with iterative analysis...")
        print("🔄 This will build insights step by step...")
        
        prompt = """
        BEGIN step-by-step comprehensive analysis of this dataset.
        
        DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
        
        Start with the first small step - data loading and basic structure using 'data.csv'.
        Use the format with EXPLANATION and CODE sections for each step.
        """
        
        iterations = self.execute_with_automation(prompt, max_iterations=25, min_iterations=5)
        self._update_context(f"Comprehensive iterative summary completed in {iterations} steps")
                
    def handle_history_command(self):
        """Show conversation and analysis history"""
        print("\n📜 SESSION HISTORY:")
        print("=" * 60)
        
        if not self.session_history:
            print("   No analysis history yet.")
            return
            
        for i, entry in enumerate(self.session_history, 1):
            timestamp = entry['timestamp']
            success = "✅" if entry['success'] else "❌"
            results = entry.get('results_count', 0)
            
            print(f"   {i}. {timestamp} {success}")
            print(f"      Results: {results} visualization(s)")
            if len(entry['code']) > 100:
                print(f"      Code: {entry['code'][:97]}...")
            else:
                print(f"      Code: {entry['code']}")
            print()
            
    def handle_save_command(self, filename: str):
        """Save current session to file"""
        try:
            if not filename:
                filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            if not filename.endswith('.json'):
                filename += '.json'
                
            session_data = {
                'timestamp': datetime.now().isoformat(),
                'dataset_info': self.current_dataset_info,
                'analysis_context': self.analysis_context,
                'session_history': self.session_history,
                'conversation_log': self.conversation_log
            }
            
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
                
            print(f"💾 Session saved to: {filename}")
            
        except Exception as e:
            print(f"❌ Failed to save session: {e}")
            
    def handle_load_command(self, filename: str):
        """Load previous session from file"""
        try:
            if not filename.endswith('.json'):
                filename += '.json'
                
            if not os.path.exists(filename):
                print(f"❌ Session file not found: {filename}")
                return
                
            with open(filename, 'r') as f:
                session_data = json.load(f)
                
            self.current_dataset_info = session_data.get('dataset_info', {})
            self.analysis_context = session_data.get('analysis_context', '')
            self.session_history = session_data.get('session_history', [])
            self.conversation_log = session_data.get('conversation_log', [])
            
            print(f"📁 Session loaded from: {filename}")
            print(f"   History entries: {len(self.session_history)}")
            
        except Exception as e:
            print(f"❌ Failed to load session: {e}")
            
    def handle_clear_command(self):
        """Clear analysis context and history"""
        self.analysis_context = ""
        self.session_history = []
        self.conversation_log = []
        print("🗑️ Analysis context and history cleared")
        
    def _update_context(self, new_info: str):
        """Update analysis context for continuity"""
        self.analysis_context += f"\n{new_info}"
        # Keep context manageable
        if len(self.analysis_context) > 2000:
            self.analysis_context = self.analysis_context[-1500:]
    
    def interactive_session(self, csv_file_path: str):
        """Main interactive analysis session"""
        self.print_banner()
        
        # Initialize sandbox
        if not self.create_sandbox():
            return
            
        # Upload dataset
        if not self.upload_dataset(csv_file_path):
            return
            
        self.print_help()
        
        print("\n🎉 Ready for interactive analysis!")
        print("💡 Try: 'analyze correlation between columns' or 'visualize data distribution'")
        print("-" * 60)
        
        try:
            while True:
                # Get user input
                user_input = input("\n🤖 You: ").strip()
                
                if not user_input:
                    continue
                    
                # Log conversation
                self.conversation_log.append({
                    'timestamp': datetime.now().isoformat(),
                    'user_input': user_input,
                    'type': 'user'
                })
                
                # Process command
                action, params = self.process_user_command(user_input)
                
                if action == 'exit':
                    print("\n👋 Thanks for using Interactive CSV Analyzer!")
                    break
                elif action == 'help':
                    self.print_help()
                elif action == 'analyze':
                    self.handle_analyze_command(params)
                elif action == 'visualize':
                    self.handle_visualize_command(params)
                elif action == 'explore':
                    self.handle_explore_command(params)
                elif action == 'summary':
                    self.handle_summary_command()
                elif action == 'history':
                    self.handle_history_command()
                elif action == 'autorun':
                    print(f"\n🤖 Starting automated analysis session...")
                    iterations = self.execute_with_automation(params)
                    self._update_context(f"Automated analysis completed in {iterations} iterations")
                elif action == 'iterate':
                    print(f"\n🔄 Starting iterative analysis session...")
                    iterations = self.execute_with_automation(params, max_iterations=25, min_iterations=5)
                    self._update_context(f"Iterative analysis completed in {iterations} iterations")
                elif action == 'save':
                    self.handle_save_command(params)
                elif action == 'load':
                    self.handle_load_command(params)
                elif action == 'clear':
                    self.handle_clear_command()
                elif action == 'chat':
                    # Free-form chat with auto-iteration
                    print(f"\n🔍 Processing: {user_input}")
                    
                    # Check if user wants iterative analysis
                    iterative_keywords = ['complex', 'comprehensive', 'complete', 'full', 'deep', 'thorough', 'detailed']
                    should_iterate = any(keyword in user_input.lower() for keyword in iterative_keywords)
                    
                    if should_iterate:
                        print("🔄 Detected request for comprehensive analysis - starting iterative mode...")
                        prompt = f"""
                        {user_input}
                        
                        DATASET INFO: The dataset is already uploaded as 'data.csv' in the sandbox.
                        
                        Start the analysis step by step, building comprehensive insights.
                        Use the format with EXPLANATION and CODE sections for each step.
                        """
                        iterations = self.execute_with_automation(prompt, max_iterations=20, min_iterations=3)
                        self._update_context(f"Comprehensive analysis of '{user_input}' completed in {iterations} steps")
                    else:
                        # Single step analysis
                        ai_response = self.chat_with_ai(user_input)
                        if ai_response:
                            if ai_response == "ANALYSIS_COMPLETE":
                                print("🎉 Analysis complete!")
                            else:
                                # Parse response for explanation and code
                                explanation, code = self._parse_ai_response(ai_response)
                                
                                if explanation:
                                    print(f"🤖 AI Explanation: {explanation}")
                                
                                if code:
                                    success, result = self.execute_code(code)
                                    if success:
                                        self._update_context(f"User query: {user_input}")
                                else:
                                    print("❌ No executable code found in AI response")
                
        except KeyboardInterrupt:
            print("\n\n⚡ Interrupted by user")
        except Exception as e:
            print(f"\n❌ Session error: {e}")
        finally:
            if self.sandbox:
                print("\n🔒 Closing sandbox...")
                self.sandbox.kill()
                print("✅ Session ended")

    def _parse_ai_response(self, response: str) -> tuple[str, str]:
        """Parse AI response to extract explanation and code"""
        try:
            explanation = ""
            code = ""
            
            # Method 1: Look for structured format
            if 'EXPLANATION:' in response:
                lines = response.strip().split('\n')
                in_code_block = False
                
                for line in lines:
                    if line.startswith('EXPLANATION:'):
                        explanation = line.replace('EXPLANATION:', '').strip()
                    elif line.startswith('CODE:'):
                        continue  # Skip the CODE: header
                    elif line.strip().startswith('```python'):
                        in_code_block = True
                    elif line.strip() == '```' and in_code_block:
                        in_code_block = False
                    elif in_code_block:
                        code += line + '\n'
                        
                return explanation, code.strip()
            
            # Method 2: Look for markdown code blocks
            elif '```python' in response:
                # Extract explanation before code block
                code_start = response.find('```python')
                if code_start > 0:
                    explanation = response[:code_start].strip()
                    # Remove common prefixes
                    explanation = explanation.replace('EXPLANATION:', '').strip()
                
                # Extract code
                code_start_content = code_start + 9
                code_end = response.find('```', code_start_content)
                if code_end != -1:
                    code = response[code_start_content:code_end].strip()
                    
                return explanation, code
            
            # Method 3: If it looks like pure code, treat as code
            elif any(keyword in response for keyword in ['import ', 'df.', 'plt.', 'print(', 'pandas']):
                return "", response.strip()
            
            # Method 4: Default - treat as explanation
            else:
                return response.strip(), ""
                
        except Exception as e:
            print(f"⚠️ Could not parse AI response: {e}")
            # Fallback - treat entire response as code if it looks like code
            if ('import ' in response or 'df.' in response or 'plt.' in response) and not response.startswith('EXPLANATION:'):
                return "", response.strip()
            # If it has the format but parsing failed, try to extract manually
            elif 'CODE:' in response:
                try:
                    code_start = response.find('```python')
                    if code_start != -1:
                        code_start += 9
                        code_end = response.find('```', code_start)
                        if code_end != -1:
                            return "", response[code_start:code_end].strip()
                except:
                    pass
            return "", ""

    def _check_sandbox_health(self) -> bool:
        """Check if sandbox is healthy and responsive"""
        try:
            if not self.sandbox:
                return False
            # Simple health check
            test_execution = self.sandbox.run_code("print('health_check')")
            return test_execution.error is None
        except Exception as e:
            if "sandbox was not found" in str(e) or "timeout" in str(e).lower():
                return False
            return True
    
    def _reinitialize_sandbox(self) -> bool:
        """Attempt to reinitialize the sandbox"""
        try:
            print("🔄 Reinitializing sandbox...")
            if self.sandbox:
                try:
                    self.sandbox.close()
                except:
                    pass
            
            self.sandbox = Sandbox(api_key=self.e2b_api_key, timeout=60)
            
            # Re-upload dataset if available
            if hasattr(self, 'current_dataset_path') and self.current_dataset_path:
                self._upload_dataset(self.current_dataset_path)
            
            return True
        except Exception as e:
            print(f"❌ Sandbox reinitialization failed: {e}")
            return False
    
    def _check_analysis_completion(self, ai_response: str, iteration: int, min_iterations: int, topics_covered: set) -> dict:
        """Intelligently determine if analysis should be completed"""
        completion_signals = [
            "analysis is complete", "comprehensive analysis", "analysis complete",
            "sufficient insights", "thorough analysis", "complete understanding",
            "analysis finished", "all aspects covered", "comprehensive coverage"
        ]
        
        # Check for explicit completion signals
        response_lower = ai_response.lower()
        for signal in completion_signals:
            if signal in response_lower:
                return {
                    "should_stop": True,
                    "reason": f"AI indicated completion with signal: '{signal}'"
                }
        
        # Check minimum iterations first
        if iteration < min_iterations:
            return {"should_stop": False, "reason": "Still in minimum iteration phase"}
        
        # Check topic coverage (require at least 4 different analysis areas)
        core_topics = {"data_exploration", "correlations", "distributions", "visualization", "patterns"}
        covered_core = core_topics.intersection(topics_covered)
        
        if len(covered_core) >= 4 and iteration >= 5:
            return {
                "should_stop": True,
                "reason": f"Comprehensive coverage achieved: {len(covered_core)} core topics covered"
            }
        
        # Check for repetitive content
        if iteration > 8 and self._detect_repetitive_analysis():
            return {
                "should_stop": True,
                "reason": "Analysis becoming repetitive - comprehensive insights achieved"
            }
        
        return {"should_stop": False, "reason": "Analysis should continue"}
    
    def _track_analysis_topics(self, explanation: str, topics_covered: set):
        """Track what types of analysis have been covered"""
        explanation_lower = explanation.lower()
        
        # Define topic keywords
        topic_mapping = {
            "data_exploration": ["shape", "structure", "overview", "basic", "exploration"],
            "correlations": ["correlation", "relationship", "association"],
            "distributions": ["distribution", "histogram", "spread", "density"],
            "visualization": ["plot", "chart", "graph", "visualiz"],
            "patterns": ["pattern", "trend", "outlier", "anomal"],
            "statistics": ["statistical", "summary", "mean", "median", "std"],
            "target_analysis": ["target", "prediction", "classification"],
            "feature_analysis": ["feature", "variable", "column"]
        }
        
        for topic, keywords in topic_mapping.items():
            if any(keyword in explanation_lower for keyword in keywords):
                topics_covered.add(topic)
    
    def _detect_repetitive_analysis(self) -> bool:
        """Detect if recent analyses are becoming repetitive"""
        if len(self.session_history) < 4:
            return False
        
        # Check last 3 entries for similar patterns
        recent_analyses = self.session_history[-3:]
        code_similarities = []
        
        for i, analysis in enumerate(recent_analyses):
            code = analysis.get('code', '').lower()
            # Simple similarity check based on common keywords
            similar_count = 0
            for other_analysis in recent_analyses[i+1:]:
                other_code = other_analysis.get('code', '').lower()
                common_words = set(code.split()) & set(other_code.split())
                if len(common_words) > 10:  # Threshold for similarity
                    similar_count += 1
            code_similarities.append(similar_count)
        
        return max(code_similarities) >= 2
    
    def _generate_intelligent_prompt(self, iteration: int, logs: Any, topics_covered: set) -> str:
        """Generate an intelligent prompt for the next iteration"""
        
        # Determine what topics still need coverage
        all_topics = {"data_exploration", "correlations", "distributions", "visualization", "patterns", "statistics", "target_analysis"}
        remaining_topics = all_topics - topics_covered
        
        prompt = f"""
INTELLIGENT ANALYSIS CONTINUATION - Step {iteration + 1}

PREVIOUS STEP RESULTS:
{str(logs)[:400] if logs else 'No output'}

ANALYSIS CONTEXT:
{self.analysis_context[-800:] if self.analysis_context else 'Starting analysis'}

COVERAGE STATUS:
✅ Completed topics: {', '.join(topics_covered) if topics_covered else 'None yet'}
📋 Remaining areas: {', '.join(remaining_topics) if remaining_topics else 'All major areas covered'}

INTELLIGENT NEXT STEP:
Based on the coverage status, please choose the MOST VALUABLE next analysis step.
Priority order:
1. If data_exploration not covered: Basic data overview and structure
2. If correlations not covered: Feature relationships and target correlations  
3. If distributions not covered: Feature distributions and patterns
4. If visualization not covered: Key visualizations for insights
5. If patterns not covered: Advanced pattern detection and outliers

IMPORTANT: 
- Choose ONE focused analysis that adds NEW insights
- Avoid repeating previous analyses
- If all major topics covered, provide final summary or conclude
- Generate executable Python code for your chosen analysis
"""
        return prompt
    
    def _handle_execution_error(self, error_logs: Any, iteration: int) -> bool:
        """Enhanced error handling with specific error type detection"""
        error_str = str(error_logs).lower()
        
        # Sandbox timeout/not found errors
        if "sandbox was not found" in error_str or "timeout" in error_str:
            print(f"🔧 Sandbox timeout detected in step {iteration}")
            print("🔄 This is common with long-running analyses - will attempt recovery")
            return True
        
        # Import/package errors
        if "import" in error_str or "module" in error_str:
            print(f"📦 Package/import issue detected - will continue with alternative approach")
            return True
        
        # Data access errors  
        if "file not found" in error_str or "no such file" in error_str:
            print(f"📁 Data access issue - will attempt reload")
            return True
        
        # Other errors - less recoverable
        print(f"❌ Execution error in step {iteration}: {error_logs}")
        return False
    
    def _print_completion_summary(self, iteration: int, topics_covered: set, sandbox_resets: int):
        """Print intelligent completion summary"""
        print(f"\n🎯 INTELLIGENT ANALYSIS COMPLETE")
        print("=" * 50)
        print(f"📊 Total steps completed: {iteration}")
        print(f"🔬 Analysis topics covered: {len(topics_covered)}")
        print(f"   {', '.join(topics_covered) if topics_covered else 'None'}")
        print(f"📈 Visualizations created: {len([h for h in self.session_history if h.get('results_count', 0) > 0])}")
        print(f"🔧 Sandbox recoveries: {sandbox_resets}")
        print(f"✅ Analysis quality: {'Comprehensive' if len(topics_covered) >= 4 else 'Partial'}")
        
        if len(topics_covered) >= 4:
            print("🎉 Comprehensive analysis achieved through intelligent iteration!")
        else:
            print("💡 For deeper insights, try 'autorun [specific topic]' to continue")
    
    def _upload_dataset(self, file_path: str) -> bool:
        """Helper method to upload dataset during sandbox recovery"""
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            self.sandbox.files.write("data.csv", file_content)
            print("✅ Dataset re-uploaded successfully after sandbox recovery")
            return True
        except Exception as e:
            print(f"❌ Failed to re-upload dataset: {e}")
            return False

def main():
    """Main entry point for the CSV analyzer"""
    print("🔬 Interactive CSV Data Analyzer")
    print("Powered by E2B Code Interpreter + OpenAI GPT-4")
    print("=" * 60)
    
    # Get CSV file path from user
    file_path = input("📁 Enter CSV file path (or 'sample_cars.csv' for demo): ").strip().strip('"')
    
    if not file_path:
        file_path = "sample_cars.csv"
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        print("💡 Make sure the file path is correct")
        return
    
    # Create and run analyzer
    analyzer = InteractiveCSVAnalyzer()
    analyzer.interactive_session(file_path)

if __name__ == "__main__":
    main()

