import sys

print("fuck this shit")

def printInput(taskName, taskType, taskTime, taskDue):
    print(f'Task Name: {taskName}, Task Type: {taskType}, Task Time: {taskTime}, Task Due: {taskDue}')


if __name__ == "__main__":
    printInput(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])