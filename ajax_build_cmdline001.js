function buildCmdline() {
  const dropdownArg = $('select[name="args"]').val();
  const customArg = $('input[name="cmdline"]').val().trim();

  if (dropdownArg === 'custom') {
    return 'pdfanalysis --custom ' + customArg;
  } else {
    return 'pdfanalysis --' + dropdownArg;
  }
}
