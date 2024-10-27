import argparse
import os
import hashlib

# Parse arguments
parser = argparse.ArgumentParser(description="Its like cmake but better.")
parser.add_argument("info_file_dir", help="Directory of the CSBuildInfo file", nargs="?", default=".")
parser.add_argument("-o", "--operation", help="Define an operation for CSBuild to do")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output of the builder")
parser.add_argument("-a", "--run-args", help="Arguments for running the program", nargs="+", required=False)
args = parser.parse_args()

# Chnage into info_file_dir
os.chdir(args.info_file_dir)

# CSBuild variables
buildinfo = []
output_file = ""
libs = ""
extra_flags = ""
compiler = "gcc"
sources = []
operations = {}
up_to_date = []

# Logs message to stdout based on severity
def log(message, level):
    if level == 0:
        print(message)
    elif level == 1:
        print("[DEBUG] " + str(message))
    elif level == 2:
        print("[ERROR] " + str(message))
        os._exit(1)

if args.verbose:
    log(args, 1)

# Build function, builds the project using CSBuild variables
def build():
    for source_file in sources:
        basename = os.path.basename(source_file)
        if os.path.exists(".csbuild/" + basename + ".hash"):
            basehash = ""
            filehash = ""
            with open(".csbuild/" + basename + ".hash", "r") as f:
                basehash = f.read()
                f.close()
            with open(source_file, "r") as f:
                string = f.read()
                filehash = str(hash(str(string)))
                f.close()
            if basehash == filehash:
                up_to_date.append(source_file)
            else:
                with open(".csbuild/" + basename + ".hash", "w") as f:
                    f.truncate()
                    f.write(str(filehash))
                    f.close()
        else:
            filehash = ""
            with open(source_file, "r") as f:
                string = f.read()
                filehash = str(hash(str(string)))
                f.close()
            with open(".csbuild/" + basename + ".hash", "x") as f:
                    f.write(str(filehash))
                    f.close()
    for source_file in sources:
        print("Compiling: " + source_file)
        
        if source_file in up_to_date:
            print("File up to date")
            continue

        if args.verbose:
            log(f"{compiler} -c {source_file} -o {source_file.replace('.c', '.o')} {libs} {extra_flags}", 1)
        os.system(f"{compiler} -c {source_file} -o {source_file.replace('.c', '.o')} {libs} {extra_flags}")

    sourcesstr = ""
    for source_file in sources:
        sourcesstr += source_file.replace(".c", ".o") + " "

    print("Linking executable: " + output_file)
    if args.verbose:
        log(f"{compiler} {sourcesstr} -o {output_file} {libs}", 1)
    os.system(f"{compiler} {sourcesstr} -o {output_file} {libs}")
    print("Done building")


# Checks if CSBuildInfo exists in current dir, if not then exits with error
if not os.path.exists("CSBuildInfo"):
    log("CSBuildInfo file does not exist in directory: " + os.getcwd(), 2)

if not os.path.exists(".csbuild"):
    log(".csbuild directory does not exist, creating it...", 1)
    os.mkdir(".csbuild")

# Reads CSBuildInfo file into buildinfo
with open("CSBuildInfo", "r") as f:
    buildinfo = f.readlines()
    f.close()

# Parse CSBuildINfo
lineidx = 0
while lineidx < buildinfo.__len__():
    line = buildinfo[lineidx].strip().replace("\n", "").replace("\t", " ")
    if line == "":
        lineidx += 1
        continue
    line_segments = line.split(" ")
    if args.verbose:
        log(f"Lineidx: {lineidx}, line: {line}", 1)

    if line_segments[0] == "COMPILER":
        compiler = line_segments[1]
    elif line_segments[0] == "LIBS":
        for i in range(1, line_segments.__len__()):
            libs += "-l" + line_segments[i] + " "

    elif line_segments[0] == "EXTRA_COMPILER_FLAGS":
        for i in range(1, line_segments.__len__()):
            extra_flags += line_segments[i] + " "
    elif line_segments[0] == "OUTPUT_FILE":
        output_file = line_segments[1]
    elif line_segments[0] == "SOURCES.":
        i = 1
        while i + lineidx < buildinfo.__len__():
           line_custom = buildinfo[lineidx + i].strip().replace("\n", "").replace("\t", " ")
           if line_custom == ".SOURCES":
               break
           sources.append(line_custom)
           i += 1
    elif line_segments[0].__contains__(":"):
        operations[line_segments[0].replace(":", "")] = lineidx + 1
        i = lineidx + 1
        while i < buildinfo.__len__() and not buildinfo[i] == "end":
            if buildinfo[i] == "end\n":
                break
            i += 1
        lineidx = i
        if args.verbose:
            log("lineidx after operation: " + str(lineidx), 1)
        continue
    elif line_segments[0].startswith("//"):
        lineidx += 1
        continue
    elif line_segments[0] == "SOURCE_DIR":
        c_files = [file for file in os.listdir(line_segments[1]) if file.endswith(".c") and os.path.isfile(os.path.join(line_segments[1], file))]
        if args.verbose:
            log(f"c_files: {c_files}", 1)
        for c_file in c_files:
            sources.append(line_segments[1] + "/" + c_file)
        
    lineidx += 1

if args.verbose:
    log("Parsed things:", 1)
    log(f"-- compiler: {compiler}", 1)
    log(f"-- libs: {libs}", 1)
    log(f"-- extra_flags: {extra_flags}", 1)
    log(f"-- output_file: {output_file}", 1)
    log(f"-- sources: {sources}", 1)
    log(f"-- operations: {operations}", 1)

if args.operation:
    if args.operation in operations.keys():
        i = operations[args.operation]
        while i < buildinfo.__len__() and not buildinfo[i].strip().replace("\n", "").replace("\t", " ") == "end":
            line = buildinfo[i].strip().replace("\n", "").replace("\t", " ")
            if args.verbose:
                log(f"Line: {line}, i: {i}", 1)
            if line == "BUILD":
                build()
            elif line.__contains__("%"):
                start = line.find("%") + 1
                end = line.find("%", start)
                var = line[start:end]
                varr = ""
                if var == "OUTPUT_FILE":
                    varr = output_file
                elif var == "COMPILER":
                    varr = compiler
                elif var == "LIBS":
                    varr = libs

                command = line.replace("%" + var + "%", varr)
                if args.verbose:
                    log(command, 1)
                os.system(command)
            elif line == "RUN":
                command = "./" + output_file
                if args.run_args:
                    for arg in args.run_args:
                        command += " " + arg
                os.system(command)
            else:
                os.system(line)
            
            i += 1
else:
    build()

