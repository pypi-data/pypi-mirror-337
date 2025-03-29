###############################################################################
# 
# Copyright (c) 2025, Anders Andersen, UiT The Arctic University of
# Norway. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# 
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
# 
# - Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
###############################################################################

# Version
version = "1.5"

# Matches for the `help2md` function (sol = start of line)
import re
_sol_lc = re.compile(r"^[a-z].*")
_sol_usage = re.compile(r"^Usage:")
_sol_ws_rest = re.compile(r"^ +.*$")
_sol_empty = re.compile(r"^$")
_sol_descr = re.compile(r"^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$")
_sol_args = re.compile(r"^[OP][a-zA-Z_0-9 ]+:$")
_py_fn = re.compile(r"[a-z]+[.]py")
_single_quoted = re.compile(r"'[^']+'")
_sol_ten_ws = re.compile(r"^          ")
_cont_line = re.compile(r"` \| ")
_sol_two_ws = re.compile(r"^  ")

def help2md(help_msg: str) -> str:
    R"""Convert a help message to markdown text

    Convert a command help message (the output from a command when the
    `-h` flag is given) to a valid and well-formated markdown text.
    This function is tailored for the help messages produced by Python
    programs using the `argparse` module.

    Arguments/return value:

    `help_msg`: The help message to convert

    `returns`: The markdown text

    """

    # Initialize help variables
    usage: bool = False
    descr: bool = False
    options: bool = False
    prev: str = ""
    nr: int = 0
    md_txt: str = ""

    # Parse each line of `help_msg`
    for line in help_msg.splitlines():

        # Count lines
        nr += 1

        # Use `match` if matching the beginning of line, and `search`
        # to match inside line

        # Uppercase first character in paragraphs
        # /^[a-z]/ 
        if _sol_lc.match(line):
            line = line[0].upper() + line[1:]

        # Initialize usage section (and optional first usage line)
        # /^Usage:/
        if _sol_usage.match(line):
            usage = True
            line = re.sub(r"^Usage: +", "\n```bash\n", line)
            line = re.sub(r"^Usage:$", "\n```bash", line)
            utxt = "\n**Usage:**\n" + line
            continue

        # Format usage code
        # usage && /^ +.*$/
        if usage and _sol_ws_rest.match(line):
            line = re.sub(r"^ +", " ", line)
            utxt += line
            continue

        # Close usage code if after usage
        # usage && /^$/
        if usage and _sol_empty.match(line):
            usage = False
            descr = True
            utxt += "\n```"
            continue

        # Close options
        # options && /^$/
        if options and _sol_empty.match(line):
            options = False

        # Description? (if so, first text after usage)
        # descr && /^[a-zA-Z_0-9][a-zA-Z_0-9 ]+.*[^:]$/
        if descr and _sol_descr.match(line):
            descr = False
            prev = "*" + line + "*"
            line = utxt

        # Initialize options/positional-arguments section
        # !usage && /^[OP][a-zA-Z_0-9 ]+:$/
        if (not usage) and _sol_args.match(line):
            if descr: descr = False
            options = True
            line = "**" + line + "**\n\nName | Description\n---- | -----------"

        # Remove .py from command
        # /[a-z]+[.]py/
        if _py_fn.search(line):
            line = re.sub(r"[.]py", "", line)

        # Substitute quote with backquote
        # /'[^']+'/
        if _single_quoted.search(line):
            line = line.replace("'", "`", 2)

        # Join continuation lines with previous line
        # /^          /
        if _sol_ten_ws.match(line):

            # options && (prev !~ /` \| /)
            if options and not _cont_line.search(prev):
                line = re.sub(r"^ *", "` | ", line)
            else:
                line = re.sub(r"^ *", " ", line)
            prev += line
            continue

        # Format arguments/options table
        # !usage && /^  /
        if not usage and _sol_two_ws.match(line):
            line = re.sub(r"^  +", "`", line)
            line = re.sub(r"  +", "` | ", line)

        # Initialize buffered line
        # NR == 1
        if nr == 1:
            prev = line

        # Print line (one line buffered)
        # NR > 1 
        else:
            md_txt += prev + "\n"
            prev = line

    # END
    md_txt += prev + "\n"
    return md_txt


# Extra appended code for pypi dist

#
# The rest of the code is to run the module as an interactive command
#
        
# Execute this module as a program
def main():

    # Create overall argument parser
    import argparse, sys
    parser = argparse.ArgumentParser(
        description=help2md.__doc__.splitlines()[0])
    parser.add_argument(
        "-V", "--version", action="version",
        version=f"%(prog)s " + version)
    parser.add_argument(
        "-o", "--outfile", default=sys.stdout, type=argparse.FileType("w"),
        help="output file (default stdout)")
    parser.add_argument(
        "-i", "--infile", default=sys.stdin, type=argparse.FileType("r"),
        help="input file (default stdin)")

    # Parse arguments
    args = parser.parse_args()
    
    # Perform the help message to markdown convertions
    try:
        print(help2md(args.infile.read()), file=args.outfile)
    except Exception as err:
        print(f"{sys.argv[0]} failed: {str(err)}", file=sys.stderr)
        sys.exit(1)

# execute this module as a program
if __name__ == '__main__':
    main()
