import pytest
import yaml

from mkdocs_partial.site_entry_point import IgnoreUnknownTagsLoader, SiteEntryPoint, local_docs


def test_list(capsys):
    SiteEntryPoint("0.1.0").list(None, None)
    captured = capsys.readouterr().out.splitlines()
    assert len(captured) > 0
    assert "docs-documentation" in captured


@pytest.mark.parametrize(
    "value,plugin, docs_path, docs_directory",
    [
        (r"test=d:\tmp\local-docs\docs::test/sub", "test", r"d:/tmp/local-docs/docs", r"test/sub"),
        (r"test=/tmp/local-docs/docs::test/sub", "test", r"/tmp/local-docs/docs", r"test/sub"),
        (r"test=/tmp/local-docs/docs", "test", r"/tmp/local-docs/docs", None),
        (r"test", "test", r"/docs", None),
    ],
    ids=["windows path", "linux path", "directory fallback", "path fallback"],
)
def test_local_docs(value, plugin, docs_path, docs_directory):
    actual_plugin, actual_docs_path, actual_docs_directory = local_docs(value, False)
    assert actual_plugin == plugin
    assert actual_docs_path == docs_path or (actual_docs_path is None and docs_path is None)
    assert actual_docs_directory == docs_directory


def test_load_yaml_with_unknown_tags():
    yaml_content = """
    known: value
    unknown: !unknown_tag some_value
    python_tag: !!python/name:pymdownx.superfences.fence_code_format
    """

    data = yaml.load(yaml_content, Loader=IgnoreUnknownTagsLoader)
    assert data["known"] == "value"
    assert data["unknown"] is None
    assert data["python_tag"] is None
