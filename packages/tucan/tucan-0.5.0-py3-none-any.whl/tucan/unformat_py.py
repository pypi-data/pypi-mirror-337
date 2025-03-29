from loguru import logger
from typing import List

from tucan.unformat_common import (
    Statements,
    new_stmts,
    remove_strings,
    clean_blanks,
    clean_inline_comments,
    split_multi_statement_lines,
)
from tucan.string_utils import eat_spaces, get_indent

COMB_CHARS = {"'''": "\xaa", '"""': "\xbb"}


def remove_combined_chars(code: List[str]) -> List[str]:
    """replace combined chars with single char alternatives"""
    new_code = []
    for line in code:
        rline = line
        for cchar, rchar in COMB_CHARS.items():
            rline = rline.replace(cchar, rchar)
        new_code.append(rline)
    return new_code


def getback_combined_chars(code: List[str]) -> List[str]:
    """replace combined chars with single char alternatives, back"""
    new_code = []
    for line in code:
        rline = line
        for cchar, rchar in COMB_CHARS.items():
            rline = rline.replace(rchar, cchar)
        new_code.append(rline)
    return new_code


def align_continuation_lines(stmts: Statements) -> Statements:
    """Merge lines using \\ symbol at continuation line"""
    new_stmt = []
    new_lines = []
    last_line = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if last_line.endswith("\\"):
            new_stmt[-1] = last_line[:-1] + " " + line.strip()
            new_lines[-1][1] = lend
        else:
            new_stmt.append(line)
            new_lines.append([lstart, lend])

        last_line = new_stmt[-1]
    return Statements(new_stmt, new_lines)


def align_multiline_strings(stmts: Statements, markup: str) -> Statements:
    new_stmt = []
    new_lines = []
    buffer = ""

    in_multiline = False
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if in_multiline:
            line = " " + line.lstrip()

        if not in_multiline:
            last_start = lstart

        for char in line:
            if char == markup:
                if not in_multiline:
                    in_multiline = True
                else:
                    in_multiline = False
            buffer += char
        # end of line reached...

        if not in_multiline:
            new_stmt.append(buffer)
            new_lines.append([last_start, lend])
            buffer = ""

    return Statements(new_stmt, new_lines)


def align_context_block(stmts: Statements) -> Statements:
    """
    Join statements on [({})]

    Args:
        stmts (stmts): List of unformatted code statements along with line number ranges.
    Returns:
        Statements: List of unformatted code statements along with line number ranges. Everything in
            a parenthesis is now a one liner.
    """
    new_stmt = []
    new_lines = []
    inside_block_context = []
    buffer = ""
    for line, (lstart, lend) in zip(stmts.stmt, stmts.lines):
        if not inside_block_context:
            this_start = lstart
            indent = get_indent(line)

        for char in line.lstrip():
            buffer += char
            if char in [
                "(",
                "[",
                "{",
            ]:
                inside_block_context.append(char)
                continue
            if char in [")", "]", "}"]:
                try:
                    inside_block_context.pop(-1)
                except IndexError:
                    logger.warning(
                        f"line {lstart} , unmatched context closing symbol -{char}-"
                    )
                continue

        # EOL reached !

        if not inside_block_context:
            new_stmt.append(indent + buffer)
            new_lines.append([this_start, lend])
            buffer = ""

    return Statements(new_stmt, new_lines)


def replace_keywords(code: List[str]) -> List[str]:
    """replace some uneasy keywords for parsing"""
    new_stmt = []

    for line in code:
        new_line = line.replace("super()", "self_super")
        new_stmt.append(new_line)
    return new_stmt


def split_fstrings(code: List[str], fstring_char: str, other_char: str) -> List[str]:
    """Split f-string into multiple strings before the remove_strings()

    for example:
     'np f" lorem {ipsum} sic " hamet '
     becomes  (split_fstrings)
     'no f" lorem "{ipsum}" sic " hamet '
     then (remove_strings)
     'no f"___"{ipsum}"___" hamet '

    """
    new_stmt = []

    for line in code:
        inside_fstring_context = False
        # inside_escape_context=False
        buffer = ""
        last_char = " "
        for char in line:
            if char == fstring_char:
                if last_char == "f":
                    inside_fstring_context = True
                else:
                    inside_fstring_context = False

            if inside_fstring_context and char == other_char:
                char = "_"

            buffer += char

            if inside_fstring_context:
                if char == "{":
                    buffer = buffer[:-1] + fstring_char + "{"
                    # inside_escape_context=True
                elif char == "}":
                    # buffer+=char
                    buffer += fstring_char  # insert one quotation after }
                    # inside_escape_context=True

            last_char = char

        new_stmt.append(buffer)
    return new_stmt


def enforce_4char_indents(code: List[str]) -> List[str]:
    """for s***o***b***  using somthg else than 4char indents"""
    smallest_indent = 1000
    for line in code:
        recess = len(get_indent(line))
        if recess > 0 and recess < smallest_indent:
            smallest_indent = recess
    if smallest_indent in [4, 1000]:
        return code

    new_code = []
    for line in code:
        recess = int(len(get_indent(line)) / smallest_indent)
        new_code.append("    " * recess + line.lstrip())
    return new_code


def unformat_py(code: List[str]) -> Statements:
    """
    Unformat Python code by stripping comments and breaking multiline statements.

    Args:
        code (List[str]): List of Python code lines.

    Returns:
        Statements: List of unformatted code statements along with line number ranges.
    """
    stmts = new_stmts(code)
    stmts.stmt = eat_spaces(stmts.stmt)
    stmts.stmt = remove_combined_chars(stmts.stmt)
    stmts = align_continuation_lines(stmts)
    
    stmts = align_multiline_strings(stmts, COMB_CHARS["'''"])
    stmts = align_multiline_strings(stmts, COMB_CHARS['"""'])
    stmts.stmt = remove_strings(stmts.stmt, COMB_CHARS["'''"])  # triple quote '''
    stmts.stmt = remove_strings(stmts.stmt, COMB_CHARS['"""'])  # triple quote """
    
    # stmts.stmt = split_fstrings(stmts.stmt, "'", '"')
    stmts.stmt = split_fstrings(stmts.stmt, '"', "'")
    stmts.stmt = remove_strings(stmts.stmt, "'")
    stmts.stmt = remove_strings(stmts.stmt, '"')

    stmts = clean_inline_comments(stmts, "#")
    stmts = clean_blanks(stmts)
    stmts = split_multi_statement_lines(stmts)
    stmts = align_context_block(stmts)
    stmts.stmt = replace_keywords(stmts.stmt)
    stmts.stmt = getback_combined_chars(stmts.stmt)
    stmts.stmt = enforce_4char_indents(stmts.stmt)

    return stmts
