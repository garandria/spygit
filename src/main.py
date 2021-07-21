import argparse
from build import Build

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--kernel_dir", type=str, help="Linux Kernel Directory",
                        required=True)
    parser.add_argument("--data_dir", type=str, help="Data Directory",
                        required=True)
    parser.add_argument("--new", action="store_true")
    parser.add_argument("--pair", action="store_true")
    parser.add_argument("--pivot", action="store_true")
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--ccache", help="Enable ccache", action="store_true")
    args = parser.parse_args()
    sdata_dir = "../{}".format(args.data_dir)
    build = Build(kernel_dir=args.kernel_dir, data_dir=sdata_dir,
                  ccache=args.ccache, time_it=True, new=args.new)
    if args.pair:
        build.pair()
    elif args.pivot:
        build.pivot()

if __name__ == "__main__":
    main()
