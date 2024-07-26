# wiz-scenario-data-analyzer

This tool analyzes a scenario information file in the AppleII version of Wizardry.

## Usage

The usage of the tool is described in this section.

### Preparation

In this section, we describe the prerequisites for the Python runtime environment and some game data files that must be prepared before using this tool.

#### Prerequisites

This tool assumes that the following Python runtime environment and libraries are installed.

- python-3.10 or later
- svgwrite
- svglib
- rlPyCairo
- Pillow

After installing python-3.10 or later, run the `pip` command to install the necessary libraries.

```:shell
pip install -r requirements.txt
````

#### Extracting scenario information file and message information file in the game disk image

To use this tool, you need a scenario information file and a message information file of Wizardry. These files are embedded in a Wizardry master disk or master/duplicate disk image file.

You can prepare these files by extracting them from a game disk image file of Wizardry.

If you are not sure about how you should extract them, see `docs/HowToObtainScenarioData.md` (it is written in Japanese, sorry).

### How to run this tool

Execute `scenario.py` in the `src` directory with  the following command line specification ( command line options in [] is optional).

The output's format is Markdown.

```:shell
scenario.py [-h] [-v] [-d] [-o output file]
```

When the execution is completed, an image file of the scenario information file extracted image information and map information will be generated in the current directory.

The report file name can be specified by `-o` or `--outfile` options.
 When you does not specify neither `-o` or `--outfile` options, the report is written on the standard output.

#### Positional arguments

 ``scenario info file`` and ``message info file`` are positional arguments. They specifies the file paths of the following files.

|Argument|File|Meaning|
|---|---|---|
|1st position|SCENARIO.DATA|Scenario information file|
|2nd position|SCENARIO.MESGS|Message information file|

The other options are optional and they have the following meanings for each:

|Long option|Short option|Meaning|
|---|---|---|
|--help|-h|Display help message|
|--version|-v|Display version information|
|--debug|-d|Enable to run in the debug mode|
|--message file-path-string|-m file-path-string|Specify the path to the message file (Scenario one only)|
|--outfile file-path-string|-o file-path-string|Specify the path to the output file (if omitted, it will be displayed on the standard output)|
|--colormap {simple,standard}|-c {simple,standard}|color selection. "simple": output bitmaps in a file in a simple manner. "standard": output bitmaps with the standard color mapping.|

### Example

We describe an example execution procedure of the tool.
This shows operations of the tool in the situation as follows:

1. Putting Wizardry scenario information file (`SCENARIO.DATA`) and message information file (`SCENARIO.MESGS`) on the current directory before hand.
2. Creating an output directory named `output` on the current directory.
3. Executing the tool to write the report file named `output.md` (`$` denotes the command prompt).

```:shell
$ mkdir output
$ cd output/
$ ... /src/scenario.py ... /SCENARIO.DATA -m .. /SCENARIO.MESGS -o output.md
$
```

When you want to analyze a scenario file of the Wizardry scenario 2 ``The Knight of Diamonds'', this tool does not support analyzing the message file of it, so you should run this command as follows:

```:shell
$ mkdir output
$ cd output/
$ ... /src/scenario.py ... /SCENARIO.DATA -o output.md
$
```
