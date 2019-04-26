import os, sys, argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('fin')
    parser.add_argument('start', type=int)
    parser.add_argument('end', type=int)
    parser.add_argument('fout')
    args = parser.parse_args()

    with open(args.fin, 'r') as fp:
        lines = [l.strip() for l in fp.readlines()]

    with open(args.fout, 'w') as fp:
        for i in range(start, end+1):
            fp.write(lines[i] + '\n')

    print "done!"


