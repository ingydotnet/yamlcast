% YAMLCAST(1) YAMLcast User Manual
% Ingy döt Net
% 2026

# NAME

yamlcast - render a YAML screencast description as an animated GIF

# SYNOPSIS

**yamlcast** [**--dry-run**] *FILE*

# DESCRIPTION

**yamlcast** reads *FILE*, a YAML description of a terminal screencast,
translates it into a **vhs**(1) `.tape` script, and invokes **vhs** to render
the resulting animated GIF.

The translator is a YAMLScript program.
`ys-0`, Go, and **vhs** are installed on demand into the project's
`./.cache/` directory.

# OPTIONS

**--dry-run**
:   Print the generated `.tape` script to standard output and do not invoke
    **vhs**.

# INPUT FORMAT

The input file is a YAML mapping.
The recognized top-level keys are:

**output**
:   Optional.
    The name of the output GIF file.
    If omitted, defaults to the input file name with its `.yaml` or `.yml`
    extension replaced by `.gif` (so `foo.yaml` produces `foo.gif`).

**steps**
:   Optional sequence describing the actions to record.
    Each entry is one of:

    - A single-key mapping.
      Supported keys are
      **type**, **sleep**, **enter**, **image**, **tab**, **backspace**,
      **space**, **hide**, **show**, **screenshot**, **ctrl**, **source**,
      **require**, and **bg_color**.
      **enter** may be given an optional text value; in that form the text
      is typed and then **Enter** is pressed.
      **image** takes a path; the image is rendered in the cast terminal
      with `yc-image`, with the typing of the command hidden.
      **bg_color** takes a hex color (with or without a leading `#`) and
      changes the terminal background mid-cast.
    - A bare ALL-CAPS string (e.g. **CLEAR**, **ENTER**, **CTRL+L**):
      emits the matching VHS key command with no typing.
      **RESET** is a special case: it re-emits every top-level setting,
      reverting any mid-cast overrides (such as **bg_color**) back to
      the baseline.
    - A bare string that names an existing file (short form for `image:`):
      the file is rendered as an image.
    - Any other bare string (short form for `enter:`):
      the string is typed and **Enter** is pressed.
    - A bare number (short form for `sleep:`):
      sleep for that many milliseconds.

Any other top-level key is treated as a VHS `Set` directive.
Keys use `snake_case` and are converted to VHS's `PascalCase` automatically
(for example, `font_size` becomes `FontSize`).

Inside a **type** value, bracketed tokens are expanded into the matching VHS
key commands.
Recognized tokens are
`<ENTER>`, `<TAB>`, `<SPACE>`, `<BACKSPACE>`,
`<UP>`, `<DOWN>`, `<LEFT>`, `<RIGHT>`,
and `<CTRL+X>` for any single key *X*.

# ENVIRONMENT

**YAMLCAST_ROOT**
:   Absolute path to the YAMLcast project directory.
    **yamlcast** refuses to run unless this is set.
    Source the project's `.rc` file to set it.

# EXIT STATUS

**yamlcast** exits 0 on success and non-zero on any error, including a
missing or invalid input file, an unset **YAMLCAST_ROOT**, or a failed
**vhs** invocation.

# EXAMPLES

Render `example.yaml` to the GIF named by its `output` key:

    yamlcast example.yaml

Print the generated `.tape` script without rendering:

    yamlcast --dry-run example.yaml

# FILES

*$YAMLCAST_ROOT/.cache/local/bin/vhs*
:   The locally-installed **vhs** binary.

*$YAMLCAST_ROOT/.rc*
:   Shell snippet that exports **YAMLCAST_ROOT** and extends **PATH** and
    **MANPATH**.

# SEE ALSO

**vhs**(1), **make**(1)

<https://github.com/charmbracelet/vhs>, <https://yamlscript.org>

# COPYRIGHT

Copyright 2026 Ingy döt Net.
Licensed under the MIT License.
