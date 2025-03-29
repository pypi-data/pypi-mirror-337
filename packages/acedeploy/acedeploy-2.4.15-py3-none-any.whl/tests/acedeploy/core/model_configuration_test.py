import json
import os
from unittest.mock import MagicMock

import acedeploy.core.model_configuration as mc
from acedeploy.core.model_sql_entities import DbObjectType
import aceutils.file_util as file_util
import pytest
from pathlib import PurePath

from dataclasses import dataclass, field
from typing import List

@dataclass
class dc1:
    prop_str: str

@dataclass
class dc2:
    prop_list: List

@dataclass
class dc3:
    prop_dc: dc1

@pytest.mark.parametrize(
    "cls, data, expected",
    [
        (dc1, {"prop_str": "val"}, dc1(prop_str="val")),
        (dc2, {"prop_list": ["hello", "world"]}, dc2(prop_list=["hello", "world"])),
        (dc3, {"prop_dc": {"prop_str": "val"}}, dc3(prop_dc=dc1(prop_str="val"))),
    ],
)
def test_objectoption_init_from_dict(cls, data, expected):
    result = mc.ObjectOptionFactory.init_from_dict(cls, data)
    assert result == expected


@pytest.mark.parametrize(
    "cls, data",
    [
        (dc1, {"prop2": "val"}),
        (dc2, {"prop_list": 1}),
        (dc3, {"prop_dc": {}}),
    ],
)
def test_objectoption_init_from_dict_error(cls, data):
    with pytest.raises(Exception):
        __ = mc.ObjectOptionFactory.init_from_dict(cls, data)


@pytest.mark.parametrize(
    "nested_dict, keys, expected",
    [
        ({"key1": "val"}, ["key1"], "val"),
        ({"key1": {"key2": "val"}}, ["key1", "key2"], "val"),
        ({"key": {"key": "val"}}, ["key", "key"], "val"),
        ({"key": "val"}, ["some_key"], None),
        ({"key1": {"key2": "val"}}, ["key2", "key1"], None),
    ],
)
def test_get_nested_dict_value(nested_dict, keys, expected):
    result = mc.SolutionConfig._get_nested_dict_value(nested_dict, keys)
    assert result == expected


@pytest.mark.parametrize(
    "val, expected",
    [("val", "val"), ("VAL", "VAL"), ("@@VAL", "@@VAL"), ("VAL@@", "VAL@@")],
)
def test_get_env_var_returns_value(val, expected):
    result = mc.SolutionConfig._get_env_var(None, val)
    assert result == expected


@pytest.mark.parametrize(
    "val, env_vars, expected",
    [
        ("@@name@@", {"name": "val"}, "val"),
        ("@@NAME@@", {"name": "val", "NAME": "val"}, "val"),
        ("@@wierd@@name@@", {"wierd@@name": "val"}, "val"),
        ("@@@wierd@@name@@@", {"@wierd@@name@": "val"}, "val"),
    ],
)
def test_get_env_var_returns_environment_variable(val, env_vars, expected):
    class DummySolutionConfig(mc.SolutionConfig):
        def __init__(self, env_vars):
            self.key_service = DummyKeyService(env_vars)

    class DummyKeyService:
        def __init__(self, env_vars):
            self.env_vars = env_vars

        def get_secret(self, val):
            return self.env_vars[val]

    model_config = DummySolutionConfig(env_vars)
    result = model_config._get_env_var(val)
    assert result == expected


@pytest.mark.parametrize(
    "val, env_vars, expected",
    [
        ("@@name@@", {"name": "true"}, True),
        ("@@name@@", {"name": "TRUE"}, True),
        ("@@name@@", {"name": "True"}, True),
        ("@@name@@", {"name": "false"}, False),
        ("@@name@@", {"name": "False"}, False),
        ("@@name@@", {"name": "FALSE"}, False),
    ],
)
def test_get_env_var_converts_boolean(val, env_vars, expected):
    class DummySolutionConfig(mc.SolutionConfig):
        def __init__(self, env_vars):
            self.key_service = DummyKeyService(env_vars)

    class DummyKeyService:
        def __init__(self, env_vars):
            self.env_vars = env_vars

        def get_secret(self, val):
            return self.env_vars[val]

    model_config = DummySolutionConfig(env_vars)
    result = model_config._get_env_var(val)
    assert result == expected


def test_solution_config_init_parse_json_full():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "$schema": "../../resources/json-schemas/deployment.schema.json",
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "cloneOptions": {
        "deployToClone": true,
        "cloneMode": "minimal",
        "dropCloneAfterDeployment": true
    },
    "deploymentOptions": {
        "resumeTasks": true,
        "reapplyExistingPolicies": false
    },
    "parallelThreads": 10,
    "actionSummaryPath": "dummy/path/actions.txt",
    "actionJsonPath": "dummy/path/actions.json",
    "keyService": "ENVIRONMENT",
    "preAndPostDeploymentFilter": [
        "dummy_entry1",
        "dummy_entry2"
    ],
    "objectOptions": {
        "TABLE": {
            "enabled": true,
            "manageRowAccessPolicyReferences": true,
            "manageMaskingPolicyReferences": true
        },
        "VIEW": {
        },
        "EXTERNAL TABLE": {
            "enabled": false
        },
        "FUNCTION": {
            "disabledLanguages": ["PYTHON"]
        }
    },
    "targetOptions": {
        "snowflakeEdition": "Enterprise",
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "targetDbRetentionTime": 1,
        "tempDbRetentionTime": 0,
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "blacklist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        },
        "preDeployment": [
            "my_project_folder/_predeployment"
        ],
        "postDeployment": [
            "my_project_folder/_postdeployment"
        ],
        "sqlVariables": {
            "my_varchar1": "this is a test",
            "my_int1": 2,
            "my_number1": 10.12,
            "my_bool1": true
        },
        "stringReplace": {
            "my_varchar1": "this is a test"
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    model_config = mc.SolutionConfig()

    assert model_config.solution_root_path == "dummy_solution_root"
    assert model_config.config_path == "dummy_config_path/test_deployment.json"

    assert model_config.deployment_mode == "develop"
    assert model_config.release_name == "my_release"
    assert model_config.git_tag_regex == "my_regex"

    assert model_config.ignore_git_information == True
    assert model_config.drop_target_objects == True
    assert model_config.abort_on_data_loss == True

    assert model_config.deploy_to_clone == True
    assert model_config.deploy_to_clone_mode == "minimal"
    assert model_config.drop_clone_after_run == True

    assert model_config.autoresume_tasks == True
    assert model_config.reapply_existing_policies == False

    assert model_config.parallel_threads == 10

    assert model_config.action_summary_path == "dummy/path/actions.txt"
    assert model_config.action_json_path == "dummy/path/actions.json"

    assert model_config.prepostdeployment_filter_list == [
        "dummy_entry1",
        "dummy_entry2",
    ]

    assert model_config.object_options == {
        DbObjectType.SCHEMA: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableObjectOption, {"enabled": True, "manageRowAccessPolicyReferences": True, "manageMaskingPolicyReferences": True}),
        DbObjectType.EXTERNALTABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": False}),
        DbObjectType.VIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
        DbObjectType.MATERIALIZEDVIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
        DbObjectType.FUNCTION: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":['PYTHON']}),
        DbObjectType.PROCEDURE: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
        DbObjectType.STAGE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.FILEFORMAT: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.STREAM: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TASK: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.PIPE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.SEQUENCE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.MASKINGPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.ROWACCESSPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.DYNAMICTABLE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.NETWORKRULE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TAG: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
    }
    assert set(model_config.enabled_object_types) == set(
        [
            DbObjectType.SCHEMA,
            DbObjectType.TABLE,
            DbObjectType.VIEW,
            DbObjectType.MATERIALIZEDVIEW,
            DbObjectType.FUNCTION,
            DbObjectType.PROCEDURE,
            DbObjectType.STAGE,
            DbObjectType.FILEFORMAT,
            DbObjectType.STREAM,
            DbObjectType.TASK,
            DbObjectType.PIPE,
            DbObjectType.SEQUENCE,
            DbObjectType.MASKINGPOLICY,
            DbObjectType.ROWACCESSPOLICY,
            DbObjectType.DYNAMICTABLE,
            DbObjectType.NETWORKRULE,
            DbObjectType.TAG,
        ]
    )
    assert set(model_config.disabled_object_types) == set([DbObjectType.EXTERNALTABLE])

    assert model_config.snow_edition == "Enterprise"
    assert model_config.snow_account == "my_account"
    assert model_config.snow_login == "my_login"
    assert model_config.snow_password == "my_pw"
    assert model_config.snow_role == "my_role"
    assert model_config.database_meta == "my_metadb"

    assert model_config.database_target == "my_target"
    assert model_config.clone_source_database == "my_sourcedb"
    assert model_config.snow_warehouse == "my_wh"

    assert model_config.target_db_retention_time == 1
    assert model_config.temp_db_retention_time == 0

    assert model_config.schema_list == {"blacklist": ["MY_SCHEMA1", "MY_SCHEMA2"]}

    assert PurePath(model_config.project_folder) == PurePath(
        "dummy_solution_root/my/project/folder"
    )
    assert [
        PurePath(pre_deployment_folder)
        for pre_deployment_folder in model_config.pre_deployment_folders
    ] == [PurePath("dummy_solution_root/my_project_folder/_predeployment")]
    assert [
        PurePath(post_deployment_folder)
        for post_deployment_folder in model_config.post_deployment_folders
    ] == [PurePath("dummy_solution_root/my_project_folder/_postdeployment")]

    assert model_config.sql_variables == {
        "my_varchar1": "this is a test",
        "my_int1": 2,
        "my_number1": 10.12,
        "my_bool1": True,
    }

    assert model_config.string_replace == {"my_varchar1": "this is a test"}


def test_solution_config_init_parse_json_small():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "parallelThreads": 10,
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    model_config = mc.SolutionConfig()

    assert model_config.solution_root_path == "dummy_solution_root"
    assert model_config.config_path == "dummy_config_path/test_deployment.json"

    assert model_config.deployment_mode == "develop"
    assert model_config.release_name == "my_release"
    assert model_config.git_tag_regex == "my_regex"

    assert model_config.ignore_git_information == True
    assert model_config.drop_target_objects == True
    assert model_config.abort_on_data_loss == True

    assert model_config.deploy_to_clone == False
    assert model_config.deploy_to_clone_mode == ""
    assert model_config.drop_clone_after_run == False

    assert model_config.autoresume_tasks == False
    assert model_config.reapply_existing_policies == False

    assert model_config.parallel_threads == 10

    assert model_config.action_summary_path == ""
    assert model_config.action_json_path == ""

    assert model_config.prepostdeployment_filter_list == []

    assert model_config.object_options == {
        DbObjectType.SCHEMA: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableObjectOption, {"enabled": True, "manageRowAccessPolicyReferences": False, "manageMaskingPolicyReferences": False}),
        DbObjectType.EXTERNALTABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
        DbObjectType.VIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
        DbObjectType.MATERIALIZEDVIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
        DbObjectType.FUNCTION: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
        DbObjectType.PROCEDURE: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
        DbObjectType.STAGE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.FILEFORMAT: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.STREAM: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TASK: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.PIPE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.SEQUENCE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.MASKINGPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.ROWACCESSPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.DYNAMICTABLE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.NETWORKRULE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
        DbObjectType.TAG: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
    }
    assert set(model_config.enabled_object_types) == set(
        [
            DbObjectType.SCHEMA,
            DbObjectType.TABLE,
            DbObjectType.EXTERNALTABLE,
            DbObjectType.VIEW,
            DbObjectType.MATERIALIZEDVIEW,
            DbObjectType.FUNCTION,
            DbObjectType.PROCEDURE,
            DbObjectType.STAGE,
            DbObjectType.FILEFORMAT,
            DbObjectType.STREAM,
            DbObjectType.TASK,
            DbObjectType.PIPE,
            DbObjectType.SEQUENCE,
            DbObjectType.MASKINGPOLICY,
            DbObjectType.ROWACCESSPOLICY,
            DbObjectType.DYNAMICTABLE,
            DbObjectType.NETWORKRULE,
            DbObjectType.TAG,
        ]
    )
    assert set(model_config.disabled_object_types) == set([])

    assert model_config.snow_edition == "Enterprise"
    assert model_config.snow_account == "my_account"
    assert model_config.snow_login == "my_login"
    assert model_config.snow_password == "my_pw"
    assert model_config.snow_role == "my_role"
    assert model_config.database_meta == "my_metadb"

    assert model_config.database_target == "my_target"
    assert model_config.clone_source_database == "my_sourcedb"
    assert model_config.snow_warehouse == "my_wh"

    assert model_config.target_db_retention_time == None
    assert model_config.temp_db_retention_time == 1

    assert model_config.schema_list == {"whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]}

    assert PurePath(model_config.project_folder) == PurePath(
        "dummy_solution_root/my/project/folder"
    )
    assert model_config.pre_deployment_folders == []
    assert model_config.post_deployment_folders == []

    assert model_config.sql_variables == {}
    assert model_config.string_replace == {}


def test_solution_config_init_parse_json_with_env_vars():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": "@@IGNORE_GIT_INFO@@",
        "dropTargetObjectsIfNotInProject": "@@DROP_IF_NOT_IN_PROJECT@@",
        "stopAtDataLoss": true
    },
    "parallelThreads": "@@PARALLEL_THREADS@@",
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "metaDatabase": "@@META_DB@@",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        },
        "sqlVariables": { "@@SQL_VAR_NAME@@": "@@SQL_VAR_VALUE@@" },
        "stringReplace": { "@@REPLACE_VAR_NAME@@": "@@REPLACE_VAR_VALUE@@" }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    os.environ["IGNORE_GIT_INFO"] = "True"
    os.environ["DROP_IF_NOT_IN_PROJECT"] = "false"
    os.environ["PARALLEL_THREADS"] = "10"
    os.environ["META_DB"] = "my_metadb"

    os.environ["SQL_VAR_NAME"] = "my_sql_var"
    os.environ["SQL_VAR_VALUE"] = "my_sql_var_value"

    os.environ["REPLACE_VAR_NAME"] = "my_reql_var"
    os.environ["REPLACE_VAR_VALUE"] = "my_repl_var_value"

    model_config = mc.SolutionConfig()

    assert model_config.ignore_git_information == True
    assert model_config.drop_target_objects == False
    assert model_config.parallel_threads == 10
    assert model_config.database_meta == "my_metadb"
    assert model_config.sql_variables == {"my_sql_var": "my_sql_var_value"}
    assert model_config.string_replace == {"my_reql_var": "my_repl_var_value"}


def test_solution_config_init_parse_json_invalid():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            # property deploymentMode is missing
            content = """
{
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "parallelThreads": 10,
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    with pytest.raises(EnvironmentError):
        _ = mc.SolutionConfig()


def test_standard_edition_does_not_allow_reaplly_policies():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "deploymentOptions": {
        "resumeTasks": true,
        "reapplyExistingPolicies": true
    },
    "parallelThreads": 10,
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "snowflakeEdition": "Standard",
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    with pytest.raises(ValueError):
        _ = mc.SolutionConfig()


def test_standard_edition_does_not_allow_target_retention_time_greater_1():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "deploymentOptions": {
        "resumeTasks": true,
        "reapplyExistingPolicies": false
    },
    "parallelThreads": 10,
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "snowflakeEdition": "Standard",
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDbRetentionTime": 7,
        "tempDbRetentionTime": 1,
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    with pytest.raises(ValueError):
        _ = mc.SolutionConfig()


def test_standard_edition_does_not_allow_temp_retention_time_greater_1():
    def mock_load_json(schema_file):
        if not schema_file.endswith("test_deployment.json"):
            return json.loads(file_util.load(schema_file))
        else:
            content = """
{
    "deploymentMode": "develop",
    "releaseName": "my_release",
    "solutionRepoTagRegex": "my_regex",
    "solutionOptions": {
        "ignoreGitInformation": true,
        "dropTargetObjectsIfNotInProject": true,
        "stopAtDataLoss": true
    },
    "deploymentOptions": {
        "resumeTasks": true,
        "reapplyExistingPolicies": false
    },
    "parallelThreads": 10,
    "keyService": "ENVIRONMENT",
    "targetOptions": {
        "snowflakeEdition": "Standard",
        "metaDatabase": "my_metadb",
        "account": "my_account",
        "login": "my_login",
        "password": "my_pw",
        "role": "my_role",
        "warehouse": "my_wh",
        "targetDbRetentionTime": 1,
        "tempDbRetentionTime": 7,
        "targetDatabase": "my_target",
        "cloneSourceDatabase": "my_sourcedb",
        "projectFolder": "my/project/folder",
        "projectSchemas": {
            "whitelist": ["MY_SCHEMA1", "MY_SCHEMA2"]
        }
    }
}
"""
            return json.loads(content)

    file_util.load_json = MagicMock(side_effect=mock_load_json)

    os.environ["ACEDEPLOY_CONFIG_PATH"] = "dummy_config_path/test_deployment.json"
    os.environ["ACEDEPLOY_SOLUTION_ROOT"] = "dummy_solution_root"

    with pytest.raises(ValueError):
        _ = mc.SolutionConfig()


@pytest.mark.parametrize(
    "object_options_raw, expected",
    [
        (
            {
                "TABLE": {"enabled": True},
                "VIEW": {},
                "EXTERNAL TABLE": {"enabled": False},
            },
            {
                DbObjectType.SCHEMA: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableObjectOption, {"enabled": True}),
                DbObjectType.EXTERNALTABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": False}
                ),
                DbObjectType.VIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
                DbObjectType.MATERIALIZEDVIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.FUNCTION: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.PROCEDURE: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.STAGE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.FILEFORMAT: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.STREAM: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TASK: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.PIPE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.SEQUENCE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.MASKINGPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.ROWACCESSPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.DYNAMICTABLE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.NETWORKRULE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TAG: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
            },
        ),
    ],
)
def test_parse_object_options(object_options_raw, expected):
    result = mc.SolutionConfig._parse_object_options(object_options_raw)
    assert result == expected


@pytest.mark.parametrize(
    "object_options, expected",
    [
        (
            {
                DbObjectType.SCHEMA: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
                DbObjectType.EXTERNALTABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": False}
                ),
                DbObjectType.VIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
                DbObjectType.MATERIALIZEDVIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.FUNCTION: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.PROCEDURE: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.STAGE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.FILEFORMAT: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.STREAM: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TASK: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.PIPE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.SEQUENCE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.MASKINGPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.ROWACCESSPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.DYNAMICTABLE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.NETWORKRULE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.TAG: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
            },
            [
                DbObjectType.SCHEMA,
                DbObjectType.TABLE,
                DbObjectType.VIEW,
                DbObjectType.MATERIALIZEDVIEW,
                DbObjectType.FUNCTION,
                DbObjectType.PROCEDURE,
                DbObjectType.STAGE,
                DbObjectType.FILEFORMAT,
                DbObjectType.STREAM,
                DbObjectType.TASK,
                DbObjectType.PIPE,
                DbObjectType.SEQUENCE,
                DbObjectType.MASKINGPOLICY,
                DbObjectType.ROWACCESSPOLICY,
                DbObjectType.DYNAMICTABLE,
                DbObjectType.NETWORKRULE,
                DbObjectType.TAG,
            ],
        ),
    ],
)
def test_get_enabled_object_types(object_options, expected):
    result = mc.SolutionConfig._get_enabled_object_types(object_options)
    assert set(result) == set(expected)


@pytest.mark.parametrize(
    "object_options, expected",
    [
        (
            {
                DbObjectType.SCHEMA: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
                DbObjectType.EXTERNALTABLE: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": False}
                ),
                DbObjectType.VIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, {"enabled": True}),
                DbObjectType.MATERIALIZEDVIEW: mc.ObjectOptionFactory().init_from_dict(mc.TableLikeObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.FUNCTION: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.PROCEDURE: mc.ObjectOptionFactory().init_from_dict(mc.FunctionLikeObjectOption, {"enabled": True, "disabledLanguages":[]}),
                DbObjectType.STAGE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.FILEFORMAT: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.STREAM: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.TASK: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.PIPE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.SEQUENCE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, {"enabled": True}),
                DbObjectType.MASKINGPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.ROWACCESSPOLICY: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.DYNAMICTABLE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.NETWORKRULE: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
                DbObjectType.TAG: mc.ObjectOptionFactory().init_from_dict(mc.ObjectOption, 
                    {"enabled": True}
                ),
            },
            [
                DbObjectType.EXTERNALTABLE,
            ],
        ),
    ],
)
def test__get_disabled_object_types(object_options, expected):
    result = mc.SolutionConfig._get_disabled_object_types(object_options)
    assert set(result) == set(expected)
