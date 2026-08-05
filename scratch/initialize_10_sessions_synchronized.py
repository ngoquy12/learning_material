# scratch/initialize_10_sessions_synchronized.py
import os
import re
from pathlib import Path
import pandas as pd

def clean_name(text: str) -> str:
    if not isinstance(text, str):
        return ""
    # Strip illegal filename characters for Windows
    text = re.sub(r'[\\/*?:"<>|]', '', text)
    return text.strip()

def initialize_sessions():
    excel_path = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material\output\pms\Lập_trình_Python\PM_Generated_IT203.xlsx")
    target_root = Path(r"d:\Rikkei Education\Elearning_Agent\Learning-Material\output\pms\Lập_trình_Python")
    
    if not excel_path.exists():
        print(f"Error: PM Excel file not found at {excel_path}")
        return

    print(f"Reading PM Excel file: {excel_path}")
    df = pd.read_excel(excel_path, header=3)
    
    current_session_id = ""
    current_session_title = ""
    current_session_type = ""
    
    sessions_dict = {}
    
    for idx, row in df.iterrows():
        sess_col = row.iloc[0]
        type_col = row.iloc[2]
        sess_title_col = row.iloc[3]
        lesson_title_col = row.iloc[4]
        
        if pd.notna(sess_col) and "Session" in str(sess_col):
            match = re.search(r'Session\s*(\d+)', str(sess_col), re.IGNORECASE)
            if match:
                sess_id_num = int(match.group(1))
                if sess_id_num > 10:
                    break # Only process first 10 sessions
                    
                current_session_id = f"Session {sess_id_num:02d}"
                current_session_type = str(type_col).strip() if pd.notna(type_col) else "THEORY"
                current_session_title = clean_name(str(sess_title_col))
                
                if current_session_id not in sessions_dict:
                    sessions_dict[current_session_id] = {
                        "id": current_session_id,
                        "title": current_session_title,
                        "type": current_session_type,
                        "lessons": []
                    }

                
        if pd.notna(lesson_title_col) and current_session_id in sessions_dict:
            lesson_str = clean_name(str(lesson_title_col))
            if lesson_str and not lesson_str.startswith("Session"):
                # Clean "Lesson XX: " to "Lesson XX - "
                lesson_str = re.sub(r'^Lesson\s+(\d+)[:\s]+', r'Lesson \1 - ', lesson_str)
                sessions_dict[current_session_id]["lessons"].append(lesson_str)
                
    print(f"\n--- Initializing Directory Structure for {len(sessions_dict)} Sessions ---")
    
    created_folders = []
    
    for sess_id, sess_data in sessions_dict.items():
        sess_dir_name = sess_data["title"]
        sess_dir_path = target_root / sess_dir_name
        sess_dir_path.mkdir(parents=True, exist_ok=True)
        created_folders.append(str(sess_dir_path))
        print(f"\n📁 Created Session Directory: {sess_dir_name} [{sess_data['type']}]")
        
        if sess_data["lessons"]:
            for lesson_title in sess_data["lessons"]:
                lesson_dir_path = sess_dir_path / lesson_title
                lesson_dir_path.mkdir(parents=True, exist_ok=True)
                created_folders.append(str(lesson_dir_path))
                print(f"   └── 📄 Created Lesson Directory: {lesson_title}")
        else:
            print(f"   (No sub-lessons for {sess_data['type']} session)")

    print(f"\n[SUCCESS] Successfully initialized structure for 10 Sessions in {target_root}")

if __name__ == "__main__":
    initialize_sessions()
