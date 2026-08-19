with open('api.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("if __name__ == '__main__':"):
        continue
    if "app.run(" in line:
        continue
    new_lines.append(line)

new_lines.append("\nif __name__ == '__main__':\n")
new_lines.append("    app.run(debug=True, port=5000, use_reloader=False)\n")

with open('api.py', 'w') as f:
    f.writelines(new_lines)
print("api.py fixed!")
