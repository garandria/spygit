import os
import git

def get_time():
    time_res = ""
    with open("time.txt", 'r') as time_file:
        for t in time_file:
            time_res = t[:-1]
    return time_res

def parse(config):
    config_dict = dict()
    with open(config, 'r') as stream:
        for line in stream:
            l = line.split()
            feat, val = l[1], l[2]
            config_dict[feat] = val
    return config_dict

def main():
    os.chdir("x264-master")
    repo = git.Git(".")
    btime = dict()
    cpp = dict()
    for b in repo.get_all_branches():
        if b != master:
            repo.checkout(b)
            btime[b] = get_time()
            cpp[b] = parse("config.h")
    print("configuration,time(s)")
    for k in btime:
        print("{},{}".format(k, btime[k]))
    with open("config_data", 'w') as data:
        data.write(cpp.__str__())

if __name__ == "__main__":
    main()
