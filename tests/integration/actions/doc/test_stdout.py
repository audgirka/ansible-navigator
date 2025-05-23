"""Tests for doc from CLI, stdout."""

from __future__ import annotations

import pytest

from .base import BaseClass


# ansible-doc help with EE
CLI_DOC_HELP_WITH_EE = (
    "ansible-navigator doc company_name.coll_1.mod_1 --help-doc -m stdout"
    " --execution-environment true"
)

testdata_1 = [
    pytest.param(
        0,
        CLI_DOC_HELP_WITH_EE,
        "ansible-navigator doc help with ee",
        "doc_help_with_ee",
        ["usage: ansible-doc [-h]"],
        id="1",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_1,
)
class TestDocHelpWithEE(BaseClass):
    """Run the tests for doc help from CLI, stdout, with an EE."""

    TEST_FOR_MODE = "stdout"


# ansible-doc help without EE
CLI_DOC_HELP_WITHOUT_EE = (
    "ansible-navigator doc company_name.coll_1.mod_1"
    " --help-doc -m stdout --execution-environment false"
)

testdata_2 = [
    pytest.param(
        0,
        CLI_DOC_HELP_WITHOUT_EE,
        "ansible-navigator doc help without ee",
        "doc_help_without_ee",
        ["usage: ansible-doc [-h]"],
        id="2",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_2,
)
class TestDocHelpWithoutEE(BaseClass):
    """Run the tests for doc help from CLI, stdout, without an EE."""

    TEST_FOR_MODE = "stdout"


# ansible-doc help failed check in interactive mode
CLI_DOC_HELP_WITH_EE_INTERACTIVE_MODE = (
    "ansible-navigator doc company_name.coll_1.mod_1 --help-doc -m interactive"
    " --execution-environment true"
)

testdata_3 = [
    pytest.param(
        0,
        CLI_DOC_HELP_WITH_EE_INTERACTIVE_MODE,
        "ansible-navigator doc help with ee in interactive mode",
        "doc_help_with_ee_wrong_mode",
        ["usage: ansible-doc [-h]"],
        id="3",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_3,
)
class TestDocHelpWithEEInteractiveMode(BaseClass):
    """Run the tests for doc help from CLI, stdout, with an EE, wrong mode."""

    TEST_FOR_MODE = "stdout"


# ansible-doc help failed check in interactive mode
CLI_DOC_HELP_WITHOUT_EE_INTERACTIVE_MODE = (
    "ansible-navigator doc company_name.coll_1.mod_1 --help-doc -m interactive"
    " --execution-environment false"
)

testdata_4 = [
    pytest.param(
        0,
        CLI_DOC_HELP_WITHOUT_EE_INTERACTIVE_MODE,
        "ansible-navigator doc help without ee in wrong mode",
        "doc_help_with_ee_wrong_mode",
        ["usage: ansible-doc [-h]"],
        id="4",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_4,
)
class TestDocHelpWithoutEEInteractiveMode(BaseClass):
    """Run the tests for doc help from CLI, stdout, without an EE, wrong mode."""

    TEST_FOR_MODE = "stdout"


# doc command run in stdout mode without EE
CLI_MODULE_DOC_WITHOUT_EE = (
    "ansible-navigator doc company_name.coll_1.mod_1 -m stdout -j --execution-environment false"
)

testdata_5 = [
    pytest.param(
        0,
        CLI_MODULE_DOC_WITHOUT_EE,
        "ansible-navigator doc in stdout mode without EE",
        "module_doc_without_ee",
        None,
        id="5",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_5,
)
class TestModuleDocWithoutEE(BaseClass):
    """Run the tests for doc from CLI, stdout, without an EE, module doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False


# doc command run in stdout mode with EE
CLI_MODULE_DOC_WITH_EE = (
    "ansible-navigator doc company_name.coll_1.mod_1 -m stdout -j --execution-environment true"
)

testdata_6 = [
    pytest.param(
        0,
        CLI_MODULE_DOC_WITH_EE,
        "ansible-navigator doc in stdout mode with EE",
        "module_doc_with_ee",
        None,
        id="6",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_6,
)
class TestModuleDocWithEE(BaseClass):
    """Run the tests for doc from CLI, stdout, with an EE, module doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False


# doc command run in stdout mode without EE
CLI_LOOKUP_DOC_WITHOUT_EE = (
    "ansible-navigator doc company_name.coll_1.lookup_1 -t lookup -m stdout -j"
    " --execution-environment false"
)

testdata_7 = [
    pytest.param(
        0,
        CLI_LOOKUP_DOC_WITHOUT_EE,
        "ansible-navigator lookup doc in stdout mode without EE",
        "lookup_doc_without_ee",
        None,
        id="7",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_7,
)
class TestLookUpDocWithoutEE(BaseClass):
    """Run the tests for doc from CLI, stdout, without an EE, lookup doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False


# doc command run in stdout mode with EE
CLI_LOOKUP_DOC_WITH_EE = (
    "ansible-navigator doc company_name.coll_1.lookup_1 -t lookup -m stdout -j"
    " --execution-environment true"
)

testdata_8 = [
    pytest.param(
        0,
        CLI_LOOKUP_DOC_WITH_EE,
        "ansible-navigator lookup doc in stdout mode with EE",
        "lookup_doc_with_ee",
        None,
        id="8",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_8,
)
class TestLookUpDocWithEE(BaseClass):
    """Run the tests for doc from CLI, stdout, with an EE, lookup doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False


# doc command run in stdout mode without EE
CLI_FILTER_DOC_WITHOUT_EE = (
    "ansible-navigator doc company_name.coll_1.filter_1 -t filter -m stdout -j"
    " --execution-environment false"
)

testdata_9 = [
    pytest.param(
        0,
        CLI_FILTER_DOC_WITHOUT_EE,
        "ansible-navigator filter doc in stdout mode without EE",
        "filter_doc_without_ee",
        None,
        id="9",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_9,
)
class TestFilterDocWithoutEE(BaseClass):
    """Run the tests for doc from CLI, stdout, without an EE, filter doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False


# doc command run in stdout mode with EE
CLI_FILTER_DOC_WITH_EE = (
    "ansible-navigator doc company_name.coll_1.filter_1 -t filter -m stdout -j"
    " --execution-environment true"
)

testdata_10 = [
    pytest.param(
        0,
        CLI_FILTER_DOC_WITH_EE,
        "ansible-navigator filter doc in stdout mode with EE",
        "filter_doc_with_ee",
        None,
        id="0",
    ),
]


@pytest.mark.parametrize(
    ("index", "user_input", "comment", "testname", "expected_in_output"),
    testdata_10,
)
class TestFilterDocWithEE(BaseClass):
    """Run the tests for doc from CLI, stdout, with an EE, filter doc."""

    TEST_FOR_MODE = "stdout"
    UPDATE_FIXTURES = False
