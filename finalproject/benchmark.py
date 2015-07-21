#!/usr/bin/env python
import math, os, subprocess, sys

FPS = 30

directory  = os.path.dirname(os.path.realpath(__file__))
inputs_dir = os.path.join(directory, "inputs")
output     = "prediction.txt" # Assume cwd...

def compute_distance(p1, p2):
    return math.sqrt(pow(p2[0] - p1[0], 2) + pow(p2[1] - p1[1], 2))

def compute_error(truth, guess):
    assert len(truth) == len(guess)
    return math.sqrt(sum([pow(compute_distance(truth[i], guess[i]), 2) for i in range(len(truth))]))

def parse_data(path):
    splits = [line.strip().split(",") for line in open(path).readlines()]
    return [(int(split[0]), int(split[1])) for split in splits]

def main():
    if not os.path.isdir(inputs_dir):
        raise Exception("Didn't find inputs in {inputs_dir}".format(**vars()))

    exe = os.path.join(directory, "finalproject.py")

    if not os.path.isfile(exe):
        raise Exception("Didn't find finalproject.py at {exe}".format(**vars()))

    errors = []

    for trial in [os.path.join(inputs_dir, item) for item in os.listdir(inputs_dir) if item.startswith("test")]:
        if not os.path.isfile(trial):
            continue

        data = parse_data(trial)

        train = data[:-2*FPS]
        truth = data[-2*FPS:]

        input = os.path.splitext(os.path.basename(trial))[0] + "-benchmark.txt"

        with open(input, 'w') as f:
            for coord in train:
                f.write("%d,%d\n" % (coord[0], coord[1]))

        cmd = "python {exe} {input}".format(**vars())
        print(cmd)
        subprocess.call(cmd, shell=True)

        if not os.path.isfile(output):
            raise Exception(output + " is missing!")

        guess = parse_data(output)

        assert len(guess) == 2 * FPS

        errors.append(compute_error(truth, guess))

    if len(errors) > 2:
        errors.sort()
        errors = errors[1:-1]
        print("Average Error across %d trials (dropped best and worst): %f" % (len(errors), sum(errors) / len(errors)))
    else:
        print("Hmm, no trials...")

if __name__ == "__main__":
    main()