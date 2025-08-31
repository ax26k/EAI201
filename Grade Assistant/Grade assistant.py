
print(" AI Grading Assistant ")
print("Type 'done' when finished.\n")

total = 0
count = 0

while True:
    subject = input("Enter subject (or 'done' to stop): ")
    if subject == "done":
        break
    
    # check if subject is numeric
    if subject.isdigit():
        print("Invalid subject! Subject name cannot be numbers.\n")
        continue
    
    marks = int(input("Enter marks: "))
    
    if marks > 100 or marks < 0:
        print("Invalid marks! Please enter between 0 and 100.\n")
        continue
    
    # grading
    if marks < 35:
        grade, remark = "W", "Needs to appear again, consider withdrawing"
    elif marks >= 95:
        grade, remark = "A+", "Excellent"
    elif marks >= 90:
        grade, remark = "A", "Good"
    elif marks >= 80:
        grade, remark = "B+", "Good, can do better"
    elif marks >= 70:
        grade, remark = "B", "Average"
    elif marks >= 60:
        grade, remark = "C+", "Needs improvement"
    elif marks >= 50:
        grade, remark = "C", "Very poor"
    else:
        grade, remark = "W", "Needs to appear again, consider withdrawing"
    
    print(subject, "->", grade, ":", remark, "\n")
    
    total += marks
    count += 1

# final grade with detailed remark
if count > 0:
    avg = total / count
    
    if avg < 35:
        final, final_remark = "W", "Needs to appear again, consider withdrawing"
    elif avg >= 95:
        final, final_remark = "A+", "Student is doing excellent, Keep going"
    elif avg >= 90:
        final, final_remark = "A", "Student is doing good, more efforts and you will be in topper's list"
    elif avg >= 80:
        final, final_remark = "B+", "Good, can do better, keep working to get in the A's"
    elif avg >= 70:
        final, final_remark = "B", "Average performance, you stand as an average student in the class"
    elif avg >= 60:
        final, final_remark = "C+", "Room for improvement, you are below average"
    elif avg >= 50:
        final, final_remark = "C", "Very poor, start working hard or you will fail"
    else:
        final, final_remark = "W", "Needs to appear again, consider withdrawing"
    
    print("Final Grade:", final, ":", final_remark)
else:
    print("No subjects entered.")
