import os
import json

DATA_FILE = "students.txt"

# ─── File Handling ───────────────────────────────────────────────

def load_students():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=4, ensure_ascii=False)

# ─── GPA Calculation ─────────────────────────────────────────────

def calculate_gpa(grades):
    """Calculate GPA on a 4.0 scale from a dict of {subject: score}."""
    if not grades:
        return 0.0
    grade_points = []
    for score in grades.values():
        if score >= 90:   grade_points.append(4.0)
        elif score >= 80: grade_points.append(3.0)
        elif score >= 70: grade_points.append(2.0)
        elif score >= 60: grade_points.append(1.0)
        else:             grade_points.append(0.0)
    return round(sum(grade_points) / len(grade_points), 2)

def gpa_to_letter(gpa):
    if gpa >= 3.5: return "A"
    if gpa >= 3.0: return "B+"
    if gpa >= 2.5: return "B"
    if gpa >= 2.0: return "C"
    if gpa >= 1.0: return "D"
    return "F"

# ─── Display Helpers ─────────────────────────────────────────────

def print_student(sid, info):
    grades = info.get("grades", {})
    gpa = calculate_gpa(grades)
    print(f"\n  ┌─ ID     : {sid}")
    print(f"  │  Name   : {info.get('name', '-')}")
    print(f"  │  Major  : {info.get('major', '-')}")
    print(f"  │  Email  : {info.get('email', '-')}")
    if grades:
        print(f"  │  Grades :")
        for subject, score in grades.items():
            print(f"  │    {subject:<20} {score}")
    print(f"  └─ GPA   : {gpa} ({gpa_to_letter(gpa)})")

def get_input(prompt, current=None):
    if current is not None:
        val = input(f"  {prompt} [{current}]: ").strip()
        return val if val else current
    return input(f"  {prompt}: ").strip()

# ─── Core Functions ──────────────────────────────────────────────

def add_student(students):
    print("\n── Add New Student ──")
    sid = input("  Student ID : ").strip()
    if not sid:
        print("  ID cannot be empty.")
        return
    if sid in students:
        print(f"  Student ID '{sid}' already exists.")
        return
    name  = input("  Name       : ").strip()
    major = input("  Major      : ").strip()
    email = input("  Email      : ").strip()
    students[sid] = {"name": name, "major": major, "email": email, "grades": {}}
    save_students(students)
    print(f"  ✓ Student '{name}' added with ID {sid}.")

def view_students(students):
    print("\n── All Students ──")
    if not students:
        print("  No students found.")
        return
    for sid, info in sorted(students.items()):
        print_student(sid, info)

def search_student(students):
    print("\n── Search Student ──")
    query = input("  Enter ID or Name: ").strip().lower()
    results = {
        sid: info for sid, info in students.items()
        if query == sid.lower() or query in info.get("name", "").lower()
    }
    if not results:
        print("  No students found.")
        return
    for sid, info in results.items():
        print_student(sid, info)

def update_student(students):
    print("\n── Update Student ──")
    sid = input("  Enter Student ID: ").strip()
    if sid not in students:
        print(f"  Student ID '{sid}' not found.")
        return
    info = students[sid]
    print(f"  Updating '{info['name']}' — press Enter to keep current value.")
    info["name"]  = get_input("Name",  info.get("name"))
    info["major"] = get_input("Major", info.get("major"))
    info["email"] = get_input("Email", info.get("email"))
    save_students(students)
    print(f"  ✓ Student '{info['name']}' updated successfully.")

def delete_student(students):
    print("\n── Delete Student ──")
    sid = input("  Enter Student ID: ").strip()
    if sid not in students:
        print(f"  Student ID '{sid}' not found.")
        return
    confirm = input(f"  Delete '{students[sid]['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        name = students.pop(sid)["name"]
        save_students(students)
        print(f"  ✓ Student '{name}' deleted.")
    else:
        print("  Cancelled.")

def manage_grades(students):
    print("\n── Add / Update Grades ──")
    sid = input("  Enter Student ID: ").strip()
    if sid not in students:
        print(f"  Student ID '{sid}' not found.")
        return
    info = students[sid]
    print(f"  Student: {info['name']}")
    print("  Enter grades (subject name + score). Empty subject to finish.")
    while True:
        subject = input("  Subject : ").strip()
        if not subject:
            break
        try:
            score = float(input("  Score   : ").strip())
            if not (0 <= score <= 100):
                print("  Score must be between 0 and 100.")
                continue
            info["grades"][subject] = score
        except ValueError:
            print("  Invalid score.")
    save_students(students)
    gpa = calculate_gpa(info["grades"])
    print(f"  ✓ Grades updated. GPA: {gpa} ({gpa_to_letter(gpa)})")

def view_report(students):
    print("\n── Student Report ──")
    sid = input("  Enter Student ID: ").strip()
    if sid not in students:
        print(f"  Student ID '{sid}' not found.")
        return
    print_student(sid, students[sid])

# ─── Main ────────────────────────────────────────────────────────

def main():
    students = load_students()

    menu = {
        "1": ("Add new student",          add_student),
        "2": ("View all students",         view_students),
        "3": ("Search student",            search_student),
        "4": ("Update student info",       update_student),
        "5": ("Delete student",            delete_student),
        "6": ("Add / Update grades",       manage_grades),
        "7": ("View student report",       view_report),
        "8": ("Exit",                      None),
    }

    while True:
        print("\n" + "=" * 40)
        print("    🎓 Student Management System")
        print("=" * 40)
        for k, (label, _) in menu.items():
            print(f"  {k}. {label}")

        choice = input("\nEnter choice (1-8): ").strip()

        if choice == "8":
            print("Goodbye!")
            break
        elif choice in menu:
            _, func = menu[choice]
            func(students)
        else:
            print("  Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
