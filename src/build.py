import os
from git import Git

CCACHE_SYM_LINK=\
"""cp /usr/bin/ccache /usr/local/bin/
ln -s /usr/bin/ccache /usr/local/bin/gcc
ln -s /usr/bin/ccache /usr/local/bin/g++
ln -s /usr/bin/ccache /usr/local/bin/cc
ln -s /usr/bin/ccache /usr/local/bin/c++"""

OPTIONS = ["--disable-asm", "--disable-bashcompletion", "--disable-opencl",
               "--disable-gpl", "--disable-thread", "--disable-win32thread",
               "--disable-interlaced", "--bit-depth=8"]

def get_configurations():
    configurations = []
    for f in os.listdir("sample-01"):
        path = "sample-01/{}".format(f)
        with open(path, 'r') as conf:
            configurations.append((path, " ".join(map(lambda x: x.strip('\n'), conf.readlines()))))
    return configurations

# def clean_branch_name(cfg):
#     cid = cfg.split('/')[-1]
#     return "config{}-clean".format(cid)

# def incremental_branch_name(fromb, newb):
#     next_cid = newb.split('/')[-1]
#     return "config{}-incremental-from-{}".format(next_cid, fromb)


class Build:

    def __init__(self, project_dir, ccache=False, time_it=False, new=False):
        self._project = project_dir
        os.chdir(self._project)
        self._new = new
        self._ccache = ccache
        self._time_it = time_it
        self._packages = "git"
        if self._time_it:
            self._packages += " time"
        if self._ccache:
            self._packages += " ccache"
        self.__pckg_install()
        if self._ccache:
            self.__ccache_init()
        self._git = None
        self.__git_init()

    def __pckg_install(self):
        pckg_manager = "apt-get install -y"
        cmd = "{} {}".format(pckg_manager, self._packages)
        os.system(cmd)

    def __ccache_init(self):
        print("Setting ccache...")
        os.system(CCACHE_SYM_LINK)
        print("Done.")

    def __git_init(self):
        self._git = Git(".")
        self._git.init()
        if self._new:
            self._git.add(".",  force=True)
            self._git.commit("source")

    def __ccache_clear(self):
        print("Ccache clear...")
        os.system("ccache -C")

    def __sys_refresh(self):
        cmd =\
            "swapoff -a && swapon -a && sync "\
            "&& echo 1 > /proc/sys/vm/drop_caches"
        print("Refresh system")
        os.system(cmd)

    def build(self, trace=False):
        time_cmd = ""
        redirect = ""
        if trace:
            redirect = ">> build-trace.txt"
        if self._time_it:
            time_cmd = "/usr/bin/time -pao time.txt --format=%e"
            cmd = "{} make -j$(nproc)".format(time_cmd)
        print("Build...")
        ret = os.system(cmd)
        if ret == 0:
            os.system("mv build-trace.txt build-trace-OK.txt")
        else:
            os.system("mv build-trace.txt build-trace-ERROR.txt")

    def configure(self, opt, trace=False):
        conf = "./configure {}".format(opt)
        redirect = ""
        if trace:
            redirect = ">> configure-trace.txt"
        cmd = "{} {}".format(conf, redirect)
        ret = os.system(cmd)
        if ret == 0:
            os.system("mv configure-trace.txt configure-trace-OK.txt")
        else:
            os.system("mv configure-trace.txt configure-trace-ERROR.txt")

    def simple_conf(self):
        # configurations = []
        # configurations.append(" ".join(OPTIONS))
        # for i in range(len(OPTIONS)):
        #     tmp = OPTIONS.copy()
        #     del tmp[i]
        #     configurations.append(" ".join(tmp))
        configurations = get_configurations()
        for c in configurations:
            branch_name = c[0].replace("/", "__")
            conf = c[1]
            self._git.checkout("master")
            # branch_name = c.replace("--", "__").replace(" ", "")
            self._git.create_branch(branch_name)
            self.configure(conf, trace=True)
            self.build(trace=True)
            self._git.add(".", force=True)
            self._git.commit("clean build")

    # def __scratch(self, config):
    #     curr_branch = clean_branch_name(config)
    #     if curr_branch in self._git.get_all_branches():
    #         self._git.checkout(curr_branch)
    #     else:
    #         self._git.create_branch(curr_branch)
    #         os.system("cp {} .config".format(config))
    #         self.__sys_refresh()
    #         self.build()
    #         self._git.add(".", force=True)
    #         self._git.commit("clean build")
    #     return curr_branch

    # def __incremental(self, basis, top):
    #     next_config_incr_branch =\
    #         incremental_branch_name(basis, top)
    #     if next_config_incr_branch not in self._git.get_all_branches():
    #         self._git.create_branch(next_config_incr_branch)
    #         os.system("rm .config time.txt")
    #         os.system("cp {} .config".format(top))
    #         self.__sys_refresh()
    #         self.build()
    #         self._git.add(".", force=True)
    #         self._git.commit("incremental build")
    #     return next_config_incr_branch

    # def pair(self):
    #     lorder = self._order.copy()
    #     while lorder:
    #         self.__ccache_clear()
    #         self._git.checkout("master")
    #         curre = lorder.pop(0)
    #         cb = self.__scratch(curre)
    #         if lorder:
    #             nincr = lorder[0]
    #             self.__incremental(cb, nincr)

    # def pivot(self):
    #     lorder = self._order.copy()
    #     pivot = lorder[0]
    #     while lorder:
    #         self.__ccache_clear()
    #         self._git.checkout("master")
    #         curre = lorder.pop(0)
    #         cb = self.__scratch(curre)
    #         if lorder:
    #             nincr = lorder[0]
    #             self.__incremental(cb, nincr)
