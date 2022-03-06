import json


def load_txt(load_name):
    lines = []
    with open(load_name, "r", encoding="utf-8") as f:
        data = f.readlines()
        for line in data:
            line = line.strip()
            if line != "":
                lines.append(line)
    return lines


def save_txt(save_name, contents):
    with open(save_name, "w", encoding="utf-8") as f:
        for content in contents:
            content = content.strip()
            if content == "":
                continue
            f.write(content)
            f.write("\n")


def save_json(json_content, save_name):
    with open(save_name, "w") as f:
        json.dump(json_content, f)


def load_json(load_name):
    with open(load_name, "r") as f:
        json_content = json.load(f)
    return json_content
