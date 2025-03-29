import os
import logging
import re
import regex


def pytest_addoption(parser):
    parser.addoption(
        "--ddlfolder", action="store", help="Path at which the .sql files are located"
    )


def pytest_generate_tests(metafunc):
    """
    Executes all tests with parameters filepath and content.
    """
    project_folder = get_project_folder(metafunc.config.option.ddlfolder)
    filelist = get_filelist(project_folder)
    filenamelist = [f.replace("\\", "/").split("/")[-1] for f in filelist]
    fileinfo = read_files(filelist)
    metafunc.parametrize(
        "filepath,content,content_clean,object_type",
        [
            (
                item["filepath"],
                item["content"],
                item["content_clean"],
                item["object_type"],
            )
            for item in fileinfo
        ],
        ids=filenamelist,
    )


def pytest_itemcollected(item):
    """
    Sets the output name of a test to a fromat of '<description>: <ids>'.
    If a test has @pytest.mark.description(description='<text>') defined,
    the description will be '<text> (<functionname>)'.
    If not, the description is '<functionname>'.
    """
    description = item.originalname
    if "pytestmark" in item.keywords._markers:
        mark = list(
            filter(
                lambda x: x.name == "description", item.keywords._markers["pytestmark"]
            )
        )
        if len(mark) > 0 and mark[0].args[0] is not None:
            description = f"{mark[0].args[0]} ({item.originalname})"

    m = re.match(item.originalname + r"\[(.*)\]", item.name)
    output_id = m.group(1)
    item._nodeid = f"{description}: {output_id}"


def get_project_folder(ddlfolder):
    """
    Checks if the variable ddlfolder contains a valid folder.
    This folder contains the SQL DDLs to be tested.
    """
    if ddlfolder is None:
        raise ValueError(
            "The option --ddlfolder is mandatory. Example: 'pytest --ddlfolder=sql/my_project'"
        )
    if os.path.exists(ddlfolder):
        return ddlfolder
    else:
        raise FileNotFoundError(
            f"Failed because the path '{ddlfolder}' given by --ddlfolder does not exist."
        )


def get_filelist(project_folder):
    """
    Gets the list of all files in a folder and its subfolders.
    """
    ignorelist = get_ignorelist()

    filelist = []
    for root, __, files in os.walk(project_folder):
        for filepath in files:
            full_path = os.path.join(root, filepath)
            if not any(r.search(str(full_path)) for r in map(re.compile, ignorelist)):
                filelist.append(full_path)
    logging.debug(f"Found {len(filelist)} files in {project_folder}.")
    return filelist


def get_ignorelist():
    """
    Load a list of regular expressions to filter out files that should not be tested.
    Returns a list of the results.
    """
    ignorelist_filename = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "ignorelist"
    )
    with open(ignorelist_filename, encoding="utf-8-sig") as f:
        lines = f.readlines()
    return [l.strip() for l in lines]


def read_files(filelist):
    """
    Returns a list containing dicts (filepath, content) of a given filelist.
    """
    result = []
    for filepath in filelist:
        try:
            with open(filepath, encoding="utf-8-sig") as f:
                content = f.read()
        except Exception as e:
            raise ValueError(
                f"File {filepath} could not be loaded. Check encoding (should be UTF8). Full error message: {str(e)}"
            )
        result.append(
            {
                "filepath": filepath,
                "content": content,
                "content_clean": remove_text_in_quotes(remove_comment(content)),
                "object_type": get_object_type(filepath),
            }
        )
    return result


def remove_comment(ddl):
    """
    Remove SQL comments from a string.
    """
    if ddl is None:
        return None
    expression_blockcomment = regex.compile(
        r"('.*?'(*SKIP)(?!))|(\/\*(?:(?!\/\*).)*?\*\/)", regex.IGNORECASE | regex.DOTALL
    )
    expression_linecomment = regex.compile(
        r"('.*?'(*SKIP)(?!))|(--.*?(\n|$))|(\/\/.*?(\n|$))",
        regex.IGNORECASE | regex.DOTALL,
    )

    old_ddl = ddl
    while True:
        cleaned_ddl = expression_blockcomment.sub("", old_ddl)
        cleaned_ddl = expression_linecomment.sub("\n", cleaned_ddl)
        if cleaned_ddl == old_ddl:
            break
        old_ddl = cleaned_ddl

    return cleaned_ddl.strip()


def remove_text_in_quotes(statement):
    """
        Removes everything in single quotes ('remove') and double dollars ($$remove$$)
    Args:
        statement: str - the whole statement (multiple lines)
    Returns:
        str - the statement with any text in single quotes removed
    """
    pattern_quotes = regex.compile(
        r"'[^\\\']*(?:\\.[^\\\']*)*'", regex.IGNORECASE | regex.DOTALL
    )
    pattern_dollars = regex.compile(r"\$\$.*?\$\$", regex.IGNORECASE | regex.DOTALL)

    statement = pattern_quotes.sub("''", statement)
    statement = pattern_dollars.sub(r"$$$$", statement)

    return statement


def get_object_type(filepath):
    """
    Return the type of an object based on filepath
    """
    dirname = os.path.dirname(filepath).casefold()
    if dirname.endswith("views"):
        return r"(?:MATERIALIZED\s+)?VIEW"
    elif dirname.endswith("tables"):
        return r"(?:TRANSIENT\s+)?TABLE"
    elif dirname.endswith("functions"):
        return r"FUNCTION"
    elif dirname.endswith("procedures"):
        return r"PROCEDURE"
    elif dirname.endswith("fileformats"):
        return r"FILE\s+FORMAT"
    elif dirname.endswith("stages"):
        return r"STAGE"
    elif dirname.endswith("streams"):
        return r"STREAM"
    elif dirname.endswith("tasks"):
        return r"TASK"
    elif dirname.endswith("pipes"):
        return r"PIPE"
    elif dirname.endswith("sequences"):
        return r"SEQUENCE"
    elif dirname.endswith("policies"):
        return r"(MASKING|ROW\s+ACCESS)\s+POLICY"
    elif dirname.endswith("tags"):
        return r'TAG'
    else:
        return r"SCHEMA"
