from utils import save_txt, load_txt
import copy

def format_aaai():
    pass

def format_acm():
    lines = load_txt("fellow/ACM fellow list_v1.txt")
    new_lines = []
    for line in lines:
        line = line.split("ACM")[0].strip()
        names = line.split(",")
        name1 = names[0].strip()
        name2 = names[1].strip()
        new_lines.append("{} {}".format(name1, name2))
        new_lines.append("{} {}".format(name2, name1))

    save_txt("fellow/ACM fellow list_v2.txt", new_lines)
        

def format_iapr():
    lines = load_txt("fellow/IAPR fellow list_v1.txt")
    new_lines = []
    for line in lines:
        ori_line = copy.copy(line)
        if not "-" in line:
            continue
        if "contri" in line:
            continue
        line = line.split("-")[:-1]
        line = "-".join(line)
        if "(" in line:
            line = line.split("(")[0].strip()
        new_lines.append(line)
    save_txt("fellow/IAPR fellow list_v2.txt", new_lines)

def format_ieee():
    lines = load_txt("fellow/IEEE fellow list_v1.txt")
    new_lines = []
    for line in lines:
        if "," in line:
            names = line.split(",")
            name1 = names[0].strip()
            name2 = names[1].strip()
            new_lines.append("{} {}".format(name1, name2))
            new_lines.append("{} {}".format(name2, name1))
        else:
            new_lines.append(line)
    save_txt("fellow/IEEE fellow list_v2.txt", new_lines)
    


if __name__ == "__main__":
    format_iapr()