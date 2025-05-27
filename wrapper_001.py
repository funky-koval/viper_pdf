"""
PDF Analysis Wrapper Module for Viper

This module allows analysts to run Didier Stevens' pdfid.py and pdf-parser.py
against the currently loaded file, from within the Viper PDF Analysis tab.

Usage examples:
  > pdfanalysis --id             # Run pdfid.py
  > pdfanalysis --id-n           # Run pdfid.py -n
  > pdfanalysis --parser         # Run pdf-parser.py
  > pdfanalysis --parser-a       # Run pdf-parser.py -a
  > pdfanalysis --parser-o6      # Run pdf-parser.py -o 6
  > pdfanalysis --parser-r6      # Run pdf-parser.py -r 6
  > pdfanalysis --custom "-O -a" # Run pdf-parser.py with custom args

NOTE: All output is shown in the Viper Web UI or CLI.
"""

import os
import subprocess
from viper.common.abstracts import Module
from viper.core.session import __sessions__

PDFID = os.path.join(os.path.dirname(__file__), 'pdfid.py')
PDFPARSER = os.path.join(os.path.dirname(__file__), 'pdf-parser.py')

class PdfAnalysis(Module):
    cmd = 'pdfanalysis'
    description = 'Run pdfid/pdf-parser tools on the loaded PDF'
    authors = ['x']
    categories = ['document']

    def __init__(self):
        super(PdfAnalysis, self).__init__()
        self.parser.add_argument('--id', action='store_true', help='Run pdfid.py')
        self.parser.add_argument('--id-n', action='store_true', help='Run pdfid.py -n')
        self.parser.add_argument('--parser', action='store_true', help='Run pdf-parser.py')
        self.parser.add_argument('--parser-a', action='store_true', help='Run pdf-parser.py -a')
        self.parser.add_argument('--parser-o6', action='store_true', help='Run pdf-parser.py -o 6')
        self.parser.add_argument('--parser-r6', action='store_true', help='Run pdf-parser.py -r 6')
        self.parser.add_argument('--custom', help='Run pdf-parser.py with custom arguments (use quotes)')

    def run(self):
        super(PdfAnalysis, self).run()

        if self.args is None:
            return

        if not __sessions__.is_set():
            self.log('error', 'No file is currently loaded. Use the "open" command first.')
            return

        file_path = __sessions__.current.file.path

        if self.args.id:
            self.execute([PDFID, file_path])
        elif self.args.id_n:
            self.execute([PDFID, '-n', file_path])
        elif self.args.parser:
            self.execute([PDFPARSER, file_path])
        elif self.args.parser_a:
            self.execute([PDFPARSER, file_path, '-a'])
        elif self.args.parser_o6:
            self.execute([PDFPARSER, file_path, '-o', '6'])
        elif self.args.parser_r6:
            self.execute([PDFPARSER, file_path, '-r', '6'])
        elif self.args.custom:
            custom_args = self.args.custom.strip().split()
            self.execute([PDFPARSER, file_path] + custom_args)
        else:
            self.log('error', 'Please specify one of the available flags.')

    def execute(self, cmd):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout.strip() + '\n' + result.stderr.strip()
            for line in output.strip().splitlines():
                self.log('info', line)
        except Exception as e:
            self.log('error', f'Execution failed: {e}')
