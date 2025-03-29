import acedeploy.core.model_instance_objects as mio
import pytest

from model_instance_object_fixtures import (
    metadata_fileformat,  # pylint: disable=unused-import
    metadata_function,
    metadata_maskingpolicy,
    metadata_pipe,
    metadata_procedure,
    metadata_rowaccesspolicy,
    metadata_schema,
    metadata_sequence,
    metadata_stage,
    metadata_stream,
    metadata_task,
    metadata_view,
)


def test_InstanceStage_eq_true(metadata_stage):
    obj1 = mio.InstanceStage(metadata_stage.copy())
    obj2 = mio.InstanceStage(metadata_stage.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceStage_eq_false(metadata_stage):
    for k in metadata_stage:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_stage.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceStage(metadata_stage.copy())
        obj2 = mio.InstanceStage(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceStage_eq_disregards_region(metadata_stage):
    """
    Stage property region returned by Snowflake is not always accurate.
    It is not needed for deployment and should not be compared.
    """
    metadata_stage1 = metadata_stage.copy()
    metadata_stage2 = metadata_stage.copy()
    metadata_stage1["region"] = "eastasia"
    metadata_stage2["region"] = "westeurope"
    obj1 = mio.InstanceStage(metadata_stage1.copy())
    obj2 = mio.InstanceStage(metadata_stage2.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceFileformat_eq_true(metadata_fileformat):
    obj1 = mio.InstanceFileformat(metadata_fileformat.copy())
    obj2 = mio.InstanceFileformat(metadata_fileformat.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceFileformat_eq_false(metadata_fileformat):
    for k in metadata_fileformat:
        if k in ("DATABASE_NAME", "database_name", "owner"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_fileformat.copy()
        if k == "format_options":
            updated_metadata[k] = '{"TYPE": "DUMMY"}'
        else:
            updated_metadata[k] = "new value"
        obj1 = mio.InstanceFileformat(metadata_fileformat.copy())
        obj2 = mio.InstanceFileformat(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceStream_eq_true(metadata_stream):
    obj1 = mio.InstanceStream(metadata_stream.copy())
    obj2 = mio.InstanceStream(metadata_stream.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceStream_eq_false(metadata_stream):
    for k in metadata_stream:
        if k in ("DATABASE_NAME", "database_name", "stale"):
            continue  # database name, stale are ignored in __eq__
        updated_metadata = metadata_stream.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceStream(metadata_stream.copy())
        obj2 = mio.InstanceStream(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceTask_eq_true(metadata_task):
    obj1 = mio.InstanceTask(metadata_task.copy())
    obj2 = mio.InstanceTask(metadata_task.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceTask_eq_false(metadata_task):
    for k in metadata_task:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_task.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceTask(metadata_task.copy())
        obj2 = mio.InstanceTask(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstancePipe_eq_true(metadata_pipe):
    obj1 = mio.InstancePipe(metadata_pipe.copy())
    obj2 = mio.InstancePipe(metadata_pipe.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstancePipe_eq_false(metadata_pipe):
    for k in metadata_pipe:
        if k in ("DATABASE_NAME", "database_name", "execution_state"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_pipe.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstancePipe(metadata_pipe.copy())
        obj2 = mio.InstancePipe(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceSequence_eq_true(metadata_sequence):
    obj1 = mio.InstanceSequence(metadata_sequence.copy())
    obj2 = mio.InstanceSequence(metadata_sequence.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceSequence_eq_false(metadata_sequence):
    for k in metadata_sequence:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_sequence.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceSequence(metadata_sequence.copy())
        obj2 = mio.InstanceSequence(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceMaskingPolicy_eq_true(metadata_maskingpolicy):
    obj1 = mio.InstanceMaskingPolicy(metadata_maskingpolicy.copy())
    obj2 = mio.InstanceMaskingPolicy(metadata_maskingpolicy.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceMaskingPolicy_eq_false(metadata_maskingpolicy):
    for k in metadata_maskingpolicy:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_maskingpolicy.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceMaskingPolicy(metadata_maskingpolicy.copy())
        obj2 = mio.InstanceMaskingPolicy(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceRowAccessPolicy_eq_true(metadata_rowaccesspolicy):
    obj1 = mio.InstanceRowAccessPolicy(metadata_rowaccesspolicy.copy())
    obj2 = mio.InstanceRowAccessPolicy(metadata_rowaccesspolicy.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceRowAccessPolicy_eq_false(metadata_rowaccesspolicy):
    for k in metadata_rowaccesspolicy:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_rowaccesspolicy.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceRowAccessPolicy(metadata_rowaccesspolicy.copy())
        obj2 = mio.InstanceRowAccessPolicy(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceFunction_eq_true(metadata_function):
    obj1 = mio.InstanceFunction(metadata_function.copy())
    obj2 = mio.InstanceFunction(metadata_function.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceFunction_eq_false(metadata_function):
    for k in metadata_function:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_function.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceFunction(metadata_function.copy())
        obj2 = mio.InstanceFunction(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceProcedure_eq_true(metadata_procedure):
    obj1 = mio.InstanceProcedure(metadata_procedure.copy())
    obj2 = mio.InstanceProcedure(metadata_procedure.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceProcedure_eq_false(metadata_procedure):
    for k in metadata_procedure:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_procedure.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceProcedure(metadata_procedure.copy())
        obj2 = mio.InstanceProcedure(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceSchema_eq_true(metadata_schema):
    obj1 = mio.InstanceSchema(metadata_schema.copy())
    obj2 = mio.InstanceSchema(metadata_schema.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceSchema_eq_false(metadata_schema):
    for k in metadata_schema:
        if k in ("DATABASE_NAME", "database_name"):
            continue  # database name is ignored in __eq__
        updated_metadata = metadata_schema.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceSchema(metadata_schema.copy())
        obj2 = mio.InstanceSchema(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceView_eq_true(metadata_view):
    obj1 = mio.InstanceView(metadata_view.copy())
    obj2 = mio.InstanceView(metadata_view.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceView_eq_false(metadata_view):
    for k in metadata_view:
        if k in (
            "DATABASE_NAME",  # database name is ignored in __eq__
            "VIEW_DEFINITION",  # view definition is tested seperately
            "COLUMN_DETAILS",  # columns details not tested here TODO: are column details tested somewhere?
            "COMMENT", #  comment is ignored in __eq__ -> comments on views are currently (10.04.2024) ignored by the MetadataService (view_definition in the information_schema.views does not include comments on views)
        ):
            continue
        updated_metadata = metadata_view.copy()
        updated_metadata[k] = "new value"
        obj1 = mio.InstanceView(metadata_view.copy())
        obj2 = mio.InstanceView(updated_metadata.copy())
        assert obj1 != obj2, f"property {k}"
        assert obj2 != obj1, f"property {k}"


def test_InstanceView_definition_create_or_replace_eq_true(metadata_view):
    metadata1 = metadata_view.copy()
    metadata1["VIEW_DEFINITION"] = "CREATE OR REPLACE VIEW X.Y AS SELECT 1 I;"
    metadata2 = metadata_view.copy()
    metadata2["VIEW_DEFINITION"] = "CREATE VIEW X.Y AS SELECT 1 I;"
    obj1 = mio.InstanceView(metadata1.copy())
    obj2 = mio.InstanceView(metadata2.copy())
    assert obj1 == obj2
    assert obj2 == obj1


def test_InstanceView_definition_eq_false(metadata_view):
    metadata1 = metadata_view.copy()
    metadata1["VIEW_DEFINITION"] = "CREATE OR REPLACE VIEW X.Y AS SELECT 1 I;"
    metadata2 = metadata_view.copy()
    metadata2["VIEW_DEFINITION"] = "CREATE OR REPLACE VIEW X.Y AS SELECT 2 I;"
    obj1 = mio.InstanceView(metadata1.copy())
    obj2 = mio.InstanceView(metadata2.copy())
    assert obj1 != obj2
    assert obj2 != obj1


def test_InstanceView_definition_create_or_replace_eq_false(metadata_view):
    metadata1 = metadata_view.copy()
    metadata1["VIEW_DEFINITION"] = "CREATE OR REPLACE VIEW X.Y AS SELECT 1 I;"
    metadata2 = metadata_view.copy()
    metadata2["VIEW_DEFINITION"] = "CREATE VIEW X.Y AS SELECT 2 I;"
    obj1 = mio.InstanceView(metadata1.copy())
    obj2 = mio.InstanceView(metadata2.copy())
    assert obj1 != obj2
    assert obj2 != obj1
