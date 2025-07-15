"""
Session Management Utilities
Load, view, and manage saved analysis sessions
"""
import json
import os
import glob
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.sessions_dir = "sessions"
        self._ensure_sessions_dir()
        
    def _ensure_sessions_dir(self):
        """Create sessions directory if it doesn't exist"""
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
            
    def list_sessions(self):
        """List all saved sessions"""
        session_files = glob.glob(os.path.join(self.sessions_dir, "*.json"))
        
        if not session_files:
            print("📭 No saved sessions found")
            return []
            
        print("\n📁 SAVED SESSIONS:")
        print("=" * 50)
        
        sessions = []
        for file_path in sorted(session_files):
            try:
                with open(file_path, 'r') as f:
                    session_data = json.load(f)
                    
                filename = os.path.basename(file_path)
                timestamp = session_data.get('timestamp', 'Unknown')
                history_count = len(session_data.get('session_history', []))
                
                sessions.append({
                    'filename': filename,
                    'filepath': file_path,
                    'timestamp': timestamp,
                    'history_count': history_count
                })
                
                print(f"📄 {filename}")
                print(f"   📅 {timestamp}")
                print(f"   📊 {history_count} analysis entries")
                print()
                
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
                
        return sessions
        
    def view_session_details(self, filename):
        """View detailed information about a session"""
        filepath = os.path.join(self.sessions_dir, filename)
        if not filename.endswith('.json'):
            filepath += '.json'
            
        if not os.path.exists(filepath):
            print(f"❌ Session not found: {filename}")
            return
            
        try:
            with open(filepath, 'r') as f:
                session_data = json.load(f)
                
            print(f"\n📄 SESSION DETAILS: {filename}")
            print("=" * 50)
            
            # Basic info
            print(f"📅 Created: {session_data.get('timestamp', 'Unknown')}")
            print(f"📊 Analysis entries: {len(session_data.get('session_history', []))}")
            print(f"💬 Conversation entries: {len(session_data.get('conversation_log', []))}")
            
            # Dataset info
            dataset_info = session_data.get('dataset_info', {})
            if dataset_info:
                print(f"📁 Dataset uploaded: {dataset_info.get('uploaded_at', 'Unknown')}")
                
            # Analysis context
            context = session_data.get('analysis_context', '')
            if context:
                print(f"\n🔍 Analysis Context:")
                print(context[:200] + "..." if len(context) > 200 else context)
                
            # Recent history
            history = session_data.get('session_history', [])
            if history:
                print(f"\n📜 Recent Analysis History:")
                for i, entry in enumerate(history[-3:], 1):  # Show last 3
                    timestamp = entry.get('timestamp', 'Unknown')
                    success = "✅" if entry.get('success') else "❌"
                    results = entry.get('results_count', 0)
                    print(f"   {i}. {timestamp} {success} ({results} results)")
                    
        except Exception as e:
            print(f"❌ Error reading session: {e}")
            
    def delete_session(self, filename):
        """Delete a saved session"""
        filepath = os.path.join(self.sessions_dir, filename)
        if not filename.endswith('.json'):
            filepath += '.json'
            
        if not os.path.exists(filepath):
            print(f"❌ Session not found: {filename}")
            return False
            
        try:
            confirm = input(f"🗑️ Are you sure you want to delete '{filename}'? (y/N): ")
            if confirm.lower() == 'y':
                os.remove(filepath)
                print(f"✅ Deleted session: {filename}")
                return True
            else:
                print("❌ Deletion cancelled")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting session: {e}")
            return False
            
    def export_session_summary(self, filename, output_format='txt'):
        """Export session summary to text file"""
        filepath = os.path.join(self.sessions_dir, filename)
        if not filename.endswith('.json'):
            filepath += '.json'
            
        if not os.path.exists(filepath):
            print(f"❌ Session not found: {filename}")
            return
            
        try:
            with open(filepath, 'r') as f:
                session_data = json.load(f)
                
            # Generate summary
            base_name = filename.replace('.json', '')
            output_file = f"{base_name}_summary.{output_format}"
            
            with open(output_file, 'w') as f:
                f.write(f"ANALYSIS SESSION SUMMARY\n")
                f.write(f"========================\n\n")
                f.write(f"Session: {filename}\n")
                f.write(f"Created: {session_data.get('timestamp', 'Unknown')}\n")
                f.write(f"Analysis Entries: {len(session_data.get('session_history', []))}\n\n")
                
                # Analysis context
                context = session_data.get('analysis_context', '')
                if context:
                    f.write(f"ANALYSIS CONTEXT:\n")
                    f.write(f"-----------------\n")
                    f.write(f"{context}\n\n")
                    
                # History
                history = session_data.get('session_history', [])
                if history:
                    f.write(f"ANALYSIS HISTORY:\n")
                    f.write(f"-----------------\n")
                    for i, entry in enumerate(history, 1):
                        f.write(f"{i}. {entry.get('timestamp', 'Unknown')}\n")
                        f.write(f"   Success: {entry.get('success', False)}\n")
                        f.write(f"   Results: {entry.get('results_count', 0)}\n")
                        f.write(f"   Code: {entry.get('code', '')[:100]}...\n\n")
                        
            print(f"📄 Summary exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error exporting summary: {e}")

def main():
    """Interactive session manager"""
    manager = SessionManager()
    
    print("📁 SESSION MANAGER")
    print("=" * 30)
    print("Commands:")
    print("  list - List all sessions")
    print("  view <filename> - View session details")
    print("  delete <filename> - Delete session")
    print("  export <filename> - Export session summary")
    print("  exit - Exit manager")
    print()
    
    while True:
        command = input("📁 Manager> ").strip().split()
        
        if not command:
            continue
            
        if command[0] == 'exit':
            break
        elif command[0] == 'list':
            manager.list_sessions()
        elif command[0] == 'view' and len(command) > 1:
            manager.view_session_details(command[1])
        elif command[0] == 'delete' and len(command) > 1:
            manager.delete_session(command[1])
        elif command[0] == 'export' and len(command) > 1:
            manager.export_session_summary(command[1])
        else:
            print("❌ Invalid command. Type 'exit' to quit.")

if __name__ == "__main__":
    main()
