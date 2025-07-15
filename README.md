# � Interactive CSV Data Analyzer

**Powered by E2B Code Interpreter + OpenAI GPT-4**

An intelligent, adaptive CSV analysis tool that uses AI to perform comprehensive data exploration with smart iteration control, automatic error recovery, and intelligent completion detection.

## 🎯 **What Makes This Special**

### 🧠 **Intelligent Iteration System**

- **No Fixed Limits**: AI determines when analysis is complete based on quality, not arbitrary iteration counts
- **Smart Stopping**: Automatically stops when comprehensive analysis is achieved
- **Topic Tracking**: Monitors 8 different analysis categories to ensure complete coverage
- **Quality-Based Completion**: Stops when 4+ core topics are thoroughly analyzed

### 🔧 **Advanced Error Recovery**

- **Sandbox Health Monitoring**: Checks E2B sandbox status before each analysis step
- **Automatic Recovery**: Handles "sandbox was not found" and timeout errors gracefully
- **Smart Reinitialization**: Automatically restarts sandbox and re-uploads data when needed
- **Error Type Detection**: Different recovery strategies for different error types

### 📊 **Comprehensive Analysis Coverage**

- **8 Analysis Categories**: Data exploration, correlations, distributions, visualizations, patterns, statistics, target analysis, feature analysis
- **Progressive Insights**: Each step builds upon previous findings
- **Adaptive Prompting**: AI generates intelligent next steps based on what's already been covered

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install openai e2b-code-interpreter python-dotenv matplotlib seaborn pandas

# Setup environment variables
cp .env.template .env
# Add your API keys to .env file
```

### 2. Run Interactive Analysis

````bash
# Main interactive mode
python main.py

# Quick demo with sample data
python quick_demo.py

# Automated comprehensive analysis
python auto_analysis.py

## 🚀 **Quick Start**

### Prerequisites
1. **Python 3.8+** with virtual environment
2. **E2B API Key** - Get from [e2b.dev](https://e2b.dev)
3. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com)

### Installation

```bash
# Clone or download the project
cd your-project-directory

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install e2b-code-interpreter openai python-dotenv pandas matplotlib seaborn numpy
````

### Setup Environment Variables

Create a `.env` file in the project directory:

```env
E2B_API_KEY=your_e2b_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### Run the Analyzer

```bash
python main.py
```

## � **Detailed Features**

### 🤖 **Intelligent Commands**

#### **Auto-Iterative Commands** (Trigger intelligent iteration automatically)

```bash
# These keywords automatically trigger intelligent iteration:
"deep complex data analysis"           # → 3-20 adaptive steps
"comprehensive heart disease study"    # → Stops when complete
"thorough statistical exploration"     # → Quality-based completion
"complete data investigation"          # → Topic coverage driven
"full analysis with visualizations"   # → Intelligent progression
```

#### **Manual Commands**

```bash
analyze [question]              # Ask specific analysis questions
analyze auto [topic]            # Force iterative analysis mode
visualize [request]             # Create specific visualizations
explore [aspect]                # Explore specific data aspects
summary                         # Comprehensive summary (5-25 steps)
autorun [prompt]                # Custom iterative analysis session
iterate [prompt]                # Force iterative mode for any analysis
history                         # Show conversation history
save [filename]                 # Save current session
load [filename]                 # Load previous session
clear                          # Clear analysis context
help                           # Show help menu
exit                           # Exit the analyzer
```

### 🧠 **How Intelligent Iteration Works**

#### **1. Smart Completion Detection**

The system intelligently determines when to stop based on:

- **Explicit AI Signals**: "analysis is complete", "comprehensive analysis", etc.
- **Topic Coverage**: Stops when 4+ core analysis areas are covered
- **Repetition Detection**: Prevents infinite loops by detecting repetitive analysis
- **Quality Assessment**: Ensures meaningful insights before stopping

#### **2. Topic Coverage Tracking**

Monitors 8 analysis categories:

- 📊 **Data Exploration**: Shape, structure, overview, basic stats
- 🔗 **Correlations**: Feature relationships, associations
- 📈 **Distributions**: Histograms, spread, density analysis
- 📉 **Visualizations**: Plots, charts, graphs
- 🎯 **Patterns**: Trends, outliers, anomalies
- 📊 **Statistics**: Summary stats, mean, median, standard deviation
- 🎯 **Target Analysis**: Prediction, classification insights
- 🔍 **Feature Analysis**: Variable analysis, column insights

#### **3. Adaptive Iteration Limits**

| Analysis Type         | Min Steps | Max Steps | Stopping Criteria           |
| --------------------- | --------- | --------- | --------------------------- |
| Auto-detected complex | 3         | 20        | Topic coverage + AI signals |
| Summary command       | 5         | 25        | Comprehensive coverage      |
| Custom autorun        | 5         | 25        | User-defined + quality      |
| Manual iterate        | 3         | 20        | Adaptive completion         |

### 🔧 **Error Recovery System**

#### **Sandbox Health Monitoring**

```python
# Before each iteration, checks:
✅ Sandbox responsiveness
✅ Connection status
✅ Error history
```

#### **Automatic Recovery Strategies**

- **Timeout Errors**: Reinitialize sandbox + re-upload data
- **Import Errors**: Continue with alternative approaches
- **Data Access**: Attempt data reload
- **Connection Issues**: Full sandbox restart

#### **Recovery Process**

1. **Detect Issue**: Health check fails or error occurs
2. **Classify Error**: Determine error type and recovery strategy
3. **Attempt Recovery**: Reinitialize sandbox if needed
4. **Re-upload Data**: Restore dataset to new sandbox
5. **Continue Analysis**: Resume from where it left off

## � **Usage Examples**

### **Example 1: Heart Disease Dataset Analysis**

```bash
📁 Enter CSV file path: heart_disease.csv

🤖 You: deep comprehensive analysis

# System automatically:
✅ Detects "comprehensive" keyword → triggers intelligent iteration
✅ Runs 3-15 adaptive steps based on analysis quality
✅ Covers data exploration, correlations, distributions, patterns
✅ Creates visualizations and statistical summaries
✅ Stops when AI determines analysis is comprehensive
```

### **Example 2: Custom Visualization Request**

```bash
🤖 You: visualize correlation heatmap and distribution plots

# System:
✅ Creates correlation heatmap
✅ Generates distribution plots for key features
✅ Saves visualizations to output/ folder
✅ Provides insights about relationships
```

### **Example 3: Specific Analysis Question**

```bash
🤖 You: analyze which features most predict the target variable

# System:
✅ Calculates feature importance
✅ Runs correlation analysis
✅ Creates importance visualizations
✅ Provides ranked feature insights
```

### **Example 4: Iterative Exploration**

```bash
🤖 You: iterate explore patterns in age and cholesterol

# System:
✅ Forces iterative mode
✅ Explores age patterns step by step
✅ Analyzes cholesterol distributions
✅ Finds correlations and outliers
✅ Builds comprehensive pattern insights
```

## 🚨 **Troubleshooting**

### **Common Issues & Solutions**

#### **"Sandbox was not found" Error**

```
✅ This is automatically handled by the recovery system
✅ Sandbox will be reinitialized automatically
✅ Dataset will be re-uploaded
✅ Analysis continues seamlessly
```

#### **API Key Issues**

```bash
# Check .env file exists and contains:
E2B_API_KEY=your_actual_key_here
OPENAI_API_KEY=sk-your_actual_key_here

# Verify keys are valid:
# E2B: https://e2b.dev/dashboard
# OpenAI: https://platform.openai.com/api-keys
```

#### **Import Errors**

```bash
# Ensure virtual environment is activated:
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install missing packages:
pip install e2b-code-interpreter openai python-dotenv pandas matplotlib seaborn numpy
```

## 🎯 **Key Improvements Over Basic Systems**

| Feature                   | Basic CSV Analyzer | This Intelligent System     |
| ------------------------- | ------------------ | --------------------------- |
| **Iteration Control**     | Fixed loop count   | 🧠 AI-determined completion |
| **Error Handling**        | Crash on errors    | 🔧 Automatic recovery       |
| **Analysis Depth**        | Surface-level      | 📊 8-category comprehensive |
| **Repetition Prevention** | Manual oversight   | 🎯 Smart topic tracking     |
| **Sandbox Management**    | Manual restart     | ⚡ Auto-reinitialization    |
| **Completion Detection**  | Time/count based   | 🎉 Quality-based stopping   |

## 🔬 **Technical Architecture**

### **Core Components**

1. **InteractiveCSVAnalyzer Class**

   - Main orchestrator
   - Handles user commands
   - Manages sessions

2. **Intelligent Iteration Engine**

   - `execute_with_automation()`: Main iteration logic
   - `_check_analysis_completion()`: Smart stopping
   - `_track_analysis_topics()`: Coverage monitoring

3. **Error Recovery System**

   - `_check_sandbox_health()`: Health monitoring
   - `_reinitialize_sandbox()`: Auto-recovery
   - `_handle_execution_error()`: Error classification

4. **AI Integration**
   - `chat_with_ai()`: GPT-4 communication
   - `_parse_ai_response()`: Response parsing
   - `_generate_intelligent_prompt()`: Adaptive prompting

### **Data Flow**

```
User Input → Command Processing → AI Analysis → Code Execution → Result Analysis → Topic Tracking → Completion Check → Next Step Planning
```

## 📁 **File Structure**

```
e2b_simple/
├── main.py                 # Main analyzer with intelligent iteration
├── .env                    # API keys (create this)
├── output/                 # Generated visualizations
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── IMPROVEMENTS.md        # Technical improvement details
├── demo.py               # Demo and testing script
└── sample_cars.csv       # Sample dataset for testing
```

## 🚀 **Ready to Analyze?**

```bash
# Start your intelligent CSV analysis journey:
cd your-project-directory
python main.py

# Try these powerful commands:
"deep comprehensive data analysis"      # Full intelligent iteration
"summary"                              # Complete overview
"autorun detailed pattern exploration" # Custom deep-dive
```

**Experience the power of AI-driven, intelligent CSV analysis with automatic error recovery and smart completion detection! 🎯📊🧠**

---

_Built with ❤️ using E2B Code Interpreter, OpenAI GPT-4, and intelligent automation_
