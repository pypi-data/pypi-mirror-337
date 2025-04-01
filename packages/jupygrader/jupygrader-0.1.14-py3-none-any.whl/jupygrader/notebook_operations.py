import os
from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell, new_markdown_cell
import re
import textwrap
import pandas as pd
import numpy as np
import black
import hashlib
import copy
from nbconvert import HTMLExporter
from bs4 import BeautifulSoup
from jupygrader.types import TestCaseMetadata, GradedResult
from pathlib import Path
from typing import Union, List, Optional

test_case_name_pattern = r'^\s*_test_case\s*=\s*[\'"](.*)[\'"]'
test_case_points_pattern = r"^\s*_points\s*=\s*(.*)[\s#]*.*[\r\n]"
manual_grading_pattern = r"^\s*_grade_manually\s*=\s*(True|False)"
graded_results_element_id = "_graded_results"

CWD = os.path.realpath(os.path.dirname(__file__))
CELL_SCRIPTS_PATH = os.path.join(CWD, "jupyter-cell-scripts")


def extract_test_case_metadata_from_code(code_str: str) -> Optional[TestCaseMetadata]:
    """Extract test case metadata from a code cell string.

    Parses a code string to extract test case metadata including the test case name,
    points value, and whether it requires manual grading. The function looks for
    specific patterns in the code:

    - `_test_case = 'name'`  (required)
    - `_points = value`      (optional, defaults to 0)
    - `_grade_manually = True/False`  (optional, defaults to `False`)

    Args:
        code_str: The source code string to parse for test case metadata

    Returns:
        A TestCaseMetadata object with extracted values if a test case is found,
        None if a test case is not found
    """
    tc_result = re.search(test_case_name_pattern, code_str, flags=re.MULTILINE)

    if not tc_result or len(tc_result.groups()) == 0:
        return None

    metadata = TestCaseMetadata(
        test_case_name=tc_result.groups()[0],
        points=0,
        grade_manually=False,
    )

    points_result = re.search(test_case_points_pattern, code_str, flags=re.MULTILINE)

    # if the test case code cell does not include _points
    # no points will be assigned (default of zero)
    if points_result and len(tc_result.groups()) > 0:
        metadata.points = float(points_result.groups()[0])

    manual_grading_result = re.search(
        manual_grading_pattern, code_str, flags=re.MULTILINE
    )

    if manual_grading_result and len(manual_grading_result.groups()) > 0:
        metadata.grade_manually = bool(manual_grading_result.groups()[0])

    return metadata


def extract_test_cases_metadata_from_notebook(
    nb: NotebookNode,
) -> List[TestCaseMetadata]:
    """Extract metadata from all test cases in a notebook.

    Iterates through all code cells in the notebook and identifies test case cells
    by looking for specific pattern markers. For each test case found, extracts
    the metadata into a `TestCaseMetadata` object.

    Args:
        nb: The notebook to extract test case metadata from

    Returns:
        A list of TestCaseMetadata objects for all test cases found in the notebook
    """
    metadata_list: List[TestCaseMetadata] = []

    for cell in nb.cells:
        if cell.cell_type == "code":
            test_case_metadata = extract_test_case_metadata_from_code(cell.source)

            if test_case_metadata:
                metadata_list.append(test_case_metadata)

    return metadata_list


def does_cell_contain_test_case(cell: NotebookNode) -> bool:
    """Determine if a notebook cell contains a test case.

    A cell is considered a test case if it contains the pattern '_test_case = "name"'.
    This function uses a regular expression to check for this pattern.

    Args:
        cell: The notebook cell to check

    Returns:
        True if the cell contains a test case pattern, False otherwise
    """
    search_result = re.search(test_case_name_pattern, cell.source, flags=re.MULTILINE)

    return search_result and (len(search_result.groups()) > 0)


def is_manually_graded_test_case(cell: NotebookNode) -> bool:
    """Determine if a notebook cell contains a manually graded test case.

    A test case is considered manually graded if it contains the pattern
    '_grade_manually = True'. This function checks for this specific pattern
    in the cell's source code.

    Args:
        cell: The notebook cell to check

    Returns:
        True if the cell is a manually graded test case, False otherwise
    """
    search_result = re.search(manual_grading_pattern, cell.source, flags=re.MULTILINE)

    return search_result and (len(search_result.groups()) > 0)


def convert_test_case_using_grader_template(cell: NotebookNode) -> str:
    """Convert a test case cell to use the grader template.

    Transforms a test case cell by wrapping it with the appropriate grader template
    based on whether it's manually graded or automatically graded.

    Args:
        cell: The notebook cell containing a test case

    Returns:
        Modified source code with the test case wrapped in a grader template
    """
    if not does_cell_contain_test_case(cell):
        # do nothing if not a test case cell
        return

    source = cell.source

    if is_manually_graded_test_case(cell):
        grader_template_code = os.path.join(
            CELL_SCRIPTS_PATH, "grader_manual_template.py"
        )
        source = cell.source
    else:
        grader_template_code = os.path.join(CELL_SCRIPTS_PATH, "grader_template.py")
        source = textwrap.indent(cell.source, "    ")

    with open(grader_template_code) as f:
        grader_template_code = f.read()

    converted_source = grader_template_code.replace("# TEST_CASE_REPLACE_HERE", source)

    cell.source = converted_source


def preprocess_test_case_cells(nb: NotebookNode) -> NotebookNode:
    """Process all test case cells in a notebook to use grader templates.

    Identifies all cells containing test cases and converts each one using
    the appropriate grader template.

    Args:
        nb: The notebook to process

    Returns:
        The notebook with all test case cells converted to use grader templates
    """
    for cell in nb.cells:
        if does_cell_contain_test_case(cell):
            convert_test_case_using_grader_template(cell)

    return nb


def add_grader_scripts(nb: NotebookNode) -> NotebookNode:
    """Add grader scripts to the beginning and end of a notebook.

    Inserts a cell with setup code at the beginning of the notebook and
    a cell with grading code at the end of the notebook.

    Args:
        nb: The notebook to add grader scripts to

    Returns:
        The notebook with grader scripts added
    """
    with open(os.path.join(CELL_SCRIPTS_PATH, "prepend_to_start_of_notebook.py")) as f:
        prepend_script = f.read()
        prepend_cell = new_code_cell(prepend_script)

    with open(os.path.join(CELL_SCRIPTS_PATH, "append_to_end_of_notebook.py")) as f:
        append_script = f.read()
        append_cell = new_code_cell(append_script)

    nb.cells.insert(0, prepend_cell)
    nb.cells.append(append_cell)

    return nb


def remove_grader_scripts(nb: NotebookNode) -> NotebookNode:
    """Remove grader scripts from the beginning and end of a notebook.

    Removes the first and last cells that were added by Jupygrader.

    Args:
        nb: The notebook to remove grader scripts from

    Returns:
        The notebook with grader scripts removed
    """
    # remove prepend, append cells added by Jupygrader before storing to HTML
    nb.cells.pop(0)  # first cell (added by Jupygrader)
    nb.cells.pop()  # last cell (added by Jupygrader)

    return nb


def extract_user_code_from_notebook(nb: NotebookNode) -> str:
    """Extract user code from a notebook.

    Collects all code from non-test-case code cells in the notebook.

    Args:
        nb: The notebook to extract code from

    Returns:
        String containing all user code concatenated with newlines
    """
    full_code = ""

    for cell in nb.cells:
        if (
            (cell.cell_type == "code")
            and not does_cell_contain_test_case(cell)
            and cell.source
        ):
            full_code += cell.source + "\n\n"

    return full_code


def remove_code_cells_that_contain(
    nb: NotebookNode, search_str: Union[str, List[str]]
) -> NotebookNode:
    if isinstance(search_str, str):
        search_list = [search_str]
    else:
        search_list = search_str

    nb.cells = [
        cell
        for cell in nb.cells
        if not (cell.cell_type == "code" and any(s in cell.source for s in search_list))
    ]
    return nb


def replace_test_case(
    nb: NotebookNode, test_case_name: str, new_test_case_code: str
) -> NotebookNode:
    """Replace a test case in a notebook with new code.

    Finds a test case with the specified name and replaces its code.

    Args:
        nb: The notebook containing the test case
        test_case_name: Name of the test case to replace
        new_test_case_code: New code to use for the test case

    Returns:
        The notebook with the specified test case replaced
    """
    for cell in nb.cells:
        if (cell.cell_type == "code") and does_cell_contain_test_case(cell):
            test_case_metadata = extract_test_case_metadata_from_code(cell.source)

            if test_case_metadata.get("test_case") == test_case_name:
                cell.source = new_test_case_code

    return nb


def remove_comments(source: str) -> str:
    """Remove comments from Python source code.

    Removes both single line comments (starting with #) and
    multi-line comments (/* ... */), while preserving strings.

    Args:
        source: Python source code as string

    Returns:
        Source code with comments removed
    """
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|#[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (# single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE | re.DOTALL)

    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return ""  # so we will return empty to remove the comment
        else:  # otherwise, we will return the 1st group
            return match.group(1)  # captured quoted-string

    return regex.sub(_replacer, source)


def get_test_cases_hash(nb: NotebookNode) -> str:
    """Generate a hash of all test cases in a notebook.

    Creates a standardized representation of all test case cells by
    removing comments and formatting with Black, then generates an MD5 hash.

    Args:
        nb: The notebook to generate a hash for

    Returns:
        MD5 hash string representing the test cases
    """
    test_cases_code = ""

    for cell in nb.cells:
        if (cell.cell_type == "code") and does_cell_contain_test_case(cell):
            # standardize code before hasing
            # by removing comments and formatting the code using the Black formatter
            standardized_code = remove_comments(cell.source)
            standardized_code = black.format_str(standardized_code, mode=black.Mode())

            # concatenate to test_cases_code
            test_cases_code += standardized_code

    # generate an MD5 hash
    hash_str = hashlib.md5(test_cases_code.encode("utf-8")).hexdigest()
    return hash_str


def add_graded_result_to_notebook(
    nb: NotebookNode, graded_result: GradedResult
) -> NotebookNode:
    """Add grading results to the beginning of a notebook.

    Creates markdown cells containing a summary of grading results,
    including scores, test case outcomes, and metadata about the grading process.

    Args:
        nb: The notebook to add results to
        graded_result: Grading result data to add

    Returns:
        Notebook with grading results added at the beginning
    """
    gr_cells = []

    # add result summary
    gr_cells.append(
        new_markdown_cell(
            '<div style="text-align: center;"><img src="https://github.com/subwaymatch/jupygrader/blob/main/docs/images/logo_jupygrader_with_text_240.png?raw=true" alt="Jupygrader Logo" width="120"/></div>'
        )
    )

    learner_score_in_percentage = (
        f" ({round(graded_result.learner_autograded_score / graded_result.max_autograded_score * 100, 2)}%)"
        if graded_result.max_autograded_score != 0
        else ""
    )

    gr_dict_for_df = {
        "**Autograded Score**": f"**{graded_result.learner_autograded_score} out of {graded_result.max_autograded_score}** {learner_score_in_percentage}",
        "Autograded Test Cases": f"Passed {graded_result.num_passed_cases} out of {graded_result.num_autograded_cases} cases",
        "Pending Test Cases": f"⌛ {graded_result.num_manually_graded_cases} item{'s' if graded_result.num_manually_graded_cases > 1 else ''} worth a total of {graded_result.max_manually_graded_score} point{'s' if graded_result.max_manually_graded_score > 1 else ''} require manual grading",
        "Total Available Points": graded_result.max_total_score,
        "Filename": graded_result.filename,
        "Autograder Finished At": graded_result.grading_finished_at,
        "Autograder Duration": f"{graded_result.grading_duration_in_seconds} second{'' if graded_result.grading_duration_in_seconds == 0 else 's'}",
        "Test Cases Checksum": graded_result.test_cases_hash,
        "Submission File Checksum": graded_result.submission_notebook_hash,
        "Autograder Python Version": f"Python {graded_result.grader_python_version}",
        "Autograder Platform": graded_result.grader_platform,
        "Jupygrader Version": graded_result.jupygrader_version,
    }

    if graded_result.num_manually_graded_cases == 0:
        del gr_dict_for_df["Pending Test Cases"]

    df_metadata = pd.DataFrame(
        {"item": gr_dict_for_df.keys(), "description": gr_dict_for_df.values()}
    )
    gr_cells.append(new_markdown_cell(df_metadata.to_markdown(index=False)))

    if (
        graded_result.num_autograded_cases + graded_result.num_manually_graded_cases
        == 0
    ):
        gr_cells.append(
            new_markdown_cell(
                "Jupygrader did not detect any test cases in this notebook."
            )
        )
    else:
        gr_cells.append(
            new_markdown_cell(
                f'<h2 id="{graded_results_element_id}">Test cases result</h2>'
            )
        )

        tc_counts = {}

        test_case_links = []

        for o in graded_result.test_case_results:
            tc_name_cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", o.test_case_name)
            if tc_name_cleaned not in tc_counts:
                tc_counts[tc_name_cleaned] = 0
            tc_counts[tc_name_cleaned] += 1
            anchor_id = f"{tc_name_cleaned}_id{tc_counts[tc_name_cleaned]}"
            test_case_link = f"<a href='#{anchor_id}'>{o.test_case_name}</a>"

            test_case_links.append(test_case_link)

        df_r = pd.DataFrame(
            [result.__dict__ for result in graded_result.test_case_results]
        )

        # replace test_case_name column with linked texts
        df_r["test_case_name"] = test_case_links

        df_r.loc[df_r["grade_manually"], "points"] = np.nan
        df_r["available_points"] = df_r["available_points"].astype(str)

        # inner function to generate a human-readable result
        def get_human_readable_result(row):
            if row["grade_manually"]:
                return "⌛ Requires manual grading"
            else:
                return "✔️ Pass" if row["did_pass"] else "❌ Fail"

        df_r["did_pass"] = df_r.apply(get_human_readable_result, axis=1)
        df_r.rename(
            columns={
                "available_points": "max_score",
                "pass": "result",
                "points": "learner_score",
            },
            inplace=True,
        )
        df_r["learner_score"] = df_r["learner_score"].astype(str).fillna("")
        df_r.drop(columns=["grade_manually"], inplace=True)

        gr_cells.append(new_markdown_cell(df_r.to_markdown()))
        gr_cells.append(new_markdown_cell("\n---\n"))

    nb.cells = gr_cells + nb.cells

    return nb


def save_graded_notebook_to_html(
    nb: NotebookNode,
    html_title: str,
    output_path: Union[str, Path],
    graded_result: GradedResult,
):
    """Save a graded notebook as HTML with enhanced navigation.

    Converts the notebook to HTML and adds a sidebar with links to test case results
    and back-to-top functionality. Also adds styling for the graded results.

    Args:
        nb: The notebook to convert
        html_title: Title for the HTML document
        output_path: Path where the HTML file will be saved
        graded_result: Grading results to use for the sidebar links
    """
    html_exporter = HTMLExporter()
    r = html_exporter.from_notebook_node(
        nb, resources={"metadata": {"name": html_title}}
    )

    # add in-page anchors for test case code cells
    soup = BeautifulSoup(r[0], "html.parser")
    elements = soup.find_all("div", class_="jp-CodeCell")

    back_to_top_link_el = soup.new_tag("a")
    back_to_top_link_el["href"] = f"#{graded_results_element_id}"
    back_to_top_link_el.string = "↑ Scroll to Graded Results Summary"

    tc_counts = {}

    for el in elements:
        cell_code = el.find("div", class_="jp-Editor").getText().strip()
        tc = extract_test_case_metadata_from_code(cell_code)
        if tc:
            tc_name_cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", tc.test_case_name)
            if tc_name_cleaned not in tc_counts:
                tc_counts[tc_name_cleaned] = 0
            tc_counts[tc_name_cleaned] += 1

            anchor_id = f"{tc_name_cleaned}_id{tc_counts[tc_name_cleaned]}"

            # set div's ID so that we can create internal anchors
            el["id"] = anchor_id

            # add "back to top" link
            el.append(copy.copy(back_to_top_link_el))

    jupygrader_sidebar_container_el = soup.new_tag("div")
    jupygrader_sidebar_container_el["class"] = "jupygrader-sidebar-container"
    soup.body.append(jupygrader_sidebar_container_el)

    back_to_top_el = BeautifulSoup(
        "<a class='graded-item-link back-to-top' data-text='Jupygrader Test Case Results' href='#_graded_results'>📑</a>",
        "html.parser",
    ).find("a")
    jupygrader_sidebar_container_el.append(back_to_top_el)

    tc_counts = {}

    for o in graded_result.test_case_results:
        tc_name_cleaned = re.sub(r"[^a-zA-Z0-9_-]", "", o.test_case_name)
        if tc_name_cleaned not in tc_counts:
            tc_counts[tc_name_cleaned] = 0
        tc_counts[tc_name_cleaned] += 1

        anchor_id = f"{tc_name_cleaned}_id{tc_counts[tc_name_cleaned]}"
        item_icon = "⌛" if o.grade_manually else "✔️" if o.did_pass else "❌"
        item_status_classname = (
            "manual-grading-required"
            if o.grade_manually
            else "pass" if o.did_pass else "fail"
        )

        item_el = soup.new_tag("a")
        item_el.string = item_icon
        item_el["class"] = f"graded-item-link {item_status_classname}"
        item_el["href"] = f"#{anchor_id}"
        item_el["data-text"] = (
            o.test_case_name
            + " "
            + (
                "(manual grading required)"
                if o.grade_manually
                else f"({o.points} out of {o.available_points})"
            )
        )
        jupygrader_sidebar_container_el.append(item_el)

    # insert css
    head = soup.head

    jupygrader_sidebar_css = """
html {
  scroll-behavior: smooth;
}
.jupygrader-sidebar-container {
  background-color: #f5f5f5;
  position: fixed;
  top: 0;
  left: 0;
  width: 36px;
  height: 100%;
  display: flex;
  flex-direction: column;
  z-index: 999;
}
.graded-item-link {
  flex: 1;
  position: relative;
  margin-bottom: 1px;
  color: #777;
  background-color: #000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  font-size: 12px;
}
.graded-item-link:hover {
  color: #fff;
  position: relative;
  z-index: 1;
}
.graded-item-link.back-to-top {
  background-color: #2196f3;
}
.graded-item-link.pass {
  border-right: 8px solid #4caf50;
}
.graded-item-link.pass:hover {
  background-color: #4caf50;
}
.graded-item-link.fail {
  border-right: 8px solid #f44336;
}
.graded-item-link.fail:hover {
  background-color: #f44336;
}
.graded-item-link.manual-grading-required {
  border-right: 8px solid #ffeb3b;
}
.graded-item-link.manual-grading-required:hover {
  background-color: #ffeb3b;
}
/* tooltip */
.graded-item-link:before {
  content: attr(data-text);
  /* here's the magic */
  position: absolute;
  font-size: 14px;
  /* vertically center */
  top: 50%;
  transform: translateY(-50%);
  /* move to right */
  left: 100%;
  /* basic styles */
  width: 300px;
  padding: 10px;
  background: #fff;
  color: #000;
  border: 4px solid #000;
  text-align: left;
  display: none;
  /* hide by default */
}
.graded-item-link.back-to-top:before {
  border-color: #2196f3;
}
.graded-item-link.pass:before {
  border-color: #4caf50;
}
.graded-item-link.fail:before {
  border-color: #f44336;
}
.graded-item-link.manual-grading-required:before {
  border-color: #ffeb3b;
}
.graded-item-link:hover:before {
  display: block;
}
"""

    new_style = soup.new_tag("style", type="text/css")
    new_style.append(jupygrader_sidebar_css)

    head.append(new_style)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())
