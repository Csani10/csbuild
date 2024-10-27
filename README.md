### CSBuild (Csani Build)

## EN

### What is this?
This is a program like cmake made with python.
Its for building c projects.

### How to use?
#### Program
```bash
python3 csbuild.py <project directory or current directory>
```

For more usage type:
```bash
python3 csbuild.py -h
```

#### CSBuildInfo
This is the info file for csbuild
Example:
```CSBuildInfo
COMPILER gcc
EXTRA_COMPILER_FLAGS -Wextra -Wall
OUTPUT_FILE main

SOURCE_DIR src

//SOURCES.
//src/main.c
//src/mymath.c
//.SOURCES

clean:
rm src/*.o
rm %OUTPUT_FILE%
end

runbuild:
BUILD
./%OUTPUT_FILE%
end

run:
./%OUTPUT_FILE%
end
```

##### How to use CSBuildInfo
Firstly you define your c compiler with:
```CSBuildInfo
COMPILER <your complier>
```

Secondly you define your output file name with:
```CSBuildInfo
OUTPUT_FILE <your output file name>
```

You can also define libs and extra compiler flags with:
```CSBuildInfo
LIBS <lib1> <lib2>
COMPILER_EXTRA_FLAGS <flag1> <flag2>
```

Thirdly you define the source code, there are two ways.
First way, define a directory for source code
Second way, define all the source code files individually
```CSBuildInfo
//First way:
SOURCE_DIR <source code directory>

//Second way:
SOURCES.
<dir/file1>
<dir/file2>
.SOURCES
```

You can make comments with //
```CSBuildInfo
//This is a comment
```

You can also define operations to do different things:
```CSBuildInfo˙
//You can use % for variables like OUTPUT_FIlE
run:
./%OUTPUT_FILE%
end
```
