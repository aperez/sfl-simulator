import os
import uuid
import subprocess
import sys

import simulator

def call(command, timeout=1800):
    print(command)
    try:
        return subprocess.call(command.split(" "), timeout=timeout)
    except:
        return -1

def barinel_command(*args):
    command = os.path.dirname(simulator.__file__)
    if sys.platform == "darwin":
        command += "/native/Barinel.macosx.x86_64 {} {} {} {}"
    else:
        command += "/native/Barinel.linux.x86_64 {} {} {} {}"
    call(command.format(*args))

def staccato_command(*args):
    command = os.path.dirname(simulator.__file__)
    if sys.platform == "darwin":
        command += "/native/Staccato.macosx.x86_64 {} {} {}"
    else:
        command += "/native/Staccato.linux.x86_64 {} {} {}"
    call(command.format(*args))

class BarinelNative(object):

    def __init__(self, path="tmp/"):
        self.path = path
        self.matrix_template = path + "matrix.{}.txt"
        self.staccato_template = path + "staccato.{}.txt"
        self.barinel_template = path + "barinel.{}.txt"

    def diagnose(self, spectrum, mid=str(uuid.uuid4()), cleanup=True):
        matrix_path = self.matrix_template.format(mid)
        staccato_path = self.staccato_template.format(mid)
        barinel_path = self.barinel_template.format(mid)

        with open(matrix_path, "w") as m:
            spectrum.print_spectrum(m)

        staccato_command(str(spectrum.components), matrix_path, staccato_path)
        barinel_command(str(spectrum.components), matrix_path, staccato_path,
                        barinel_path)

        #process barinel file
        report = self.parse_report(barinel_path)

        if cleanup:
            if os.path.isfile(matrix_path): os.remove(matrix_path)
            if os.path.isfile(staccato_path): os.remove(staccato_path)
            if os.path.isfile(barinel_path): os.remove(barinel_path)

        return report

    def parse_report(self, barinel_path):
        report = []
        if not os.path.isfile(barinel_path):
            return report
        with open(barinel_path) as b:
            for line in b:
                candidate = []
                prob = 0
                line = line.rstrip()
                multiple = line.find('}')

                if multiple == -1:
                    line = line.split("  ")
                    candidate = [int(line[0])]
                    prob = float(line[1])
                else:
                    candidate = [int(x) for x in line[1:multiple].split(",")]
                    prob = float(line[multiple+1:])

                #components are 1-indexed
                candidate = [x-1 for x in candidate]
                report.append((candidate, prob))
        return report
