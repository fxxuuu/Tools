import os, sys, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('save_file')
    parser.add_argument('prefix', type=str)
    args = parser.parse_args()

    lines = [l.strip() for l in open(args.file, 'r').readlines()]
    with open(args.save_file, 'w') as fp:
        for line in lines:
            fp.write(args.prefix + line + '\n')

    print "All done!"
