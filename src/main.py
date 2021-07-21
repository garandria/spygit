import argparse
from build import Build

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project_dir", type=str, help="Project's Directory",
                        required=True)
    parser.add_argument("--new", action="store_true")
    parser.add_argument("--configure", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--ccache", help="Enable ccache", action="store_true")
    args = parser.parse_args()
    build = Build(project_dir=args.project_dir, ccache=args.ccache, time_it=True,
                  new=args.new)
    build.simple_conf()

if __name__ == "__main__":
    main()
