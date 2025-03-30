"""Internal configuration for Documentation Generation."""

import typing as t
from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)

# Runtime folder path of {{ cookiecutter.project_slug }}
PROJ_TEMPLATE_DIR: Path = Path(__file__).parent.parent / '{{ cookiecutter.project_slug }}'

# Reminder: the Template Design (TD) is defined by the:
#   - Template Variables; ie cookiecutter.json
#   - Project Template (root dir); ie /usr/lib/python/site-packages/cookiecutter_python/{{ cookiecutter.project_slug }}

# TODO: change to Dict[str, Path]
def get_docs_gen_internal_config() -> t.Dict[str, str]:
    """Scan Template Project and map docs-builder ID to their docs template folder.
    
    Finds folders following pattern "docs-*" (ie docs-mkdocs, docs-sphinx),
    uses the substring after the dash (-) as the docs-builder ID and creates a
    mapping of docs-builder ID to their docs template folder.

    Information included:
        - the folder where we each docs builder will generate the docs.
          We locate the template folder for each docs builder, which is the
          Single Source of Truth for the docs builder's output folder.
    
    Returns:
        doc_builder_id_2_doc_folder: Mapping of doc builder ID to their docs template folder.
    """
    # find folders in PROJ_TEMPLATE_DIR with "docs-*"" glob pattern
    # and return a mapping of doc builder ID to their docs template folder
    # ie: {'mkdocs': 'docs-mkdocs', 'sphinx': 'docs-sphinx'}
    doc_builder_id_2_doc_folder: t.Dict[str, str] = dict()

    for path in (x for x in PROJ_TEMPLATE_DIR.glob('docs-*') if x.is_dir()):
        folder_name_split_on_dash: t.List[str] = path.name.split('-')
        if len(folder_name_split_on_dash) != 2:
            logger.error("Docs Tempate Folder name, does not follow proper pattern ie 'docs-mkdocs': %s", json.dumps({
                "path": str(path),
                }, indent=2, sort_keys=True))
            raise ValueError(f"Docs Tempate Folder name, does not follow proper pattern ie 'docs-mkdocs': {path}")

        docs_builder_id: str = folder_name_split_on_dash[1]
        corresponding_template_folder: str = path.name
        doc_builder_id_2_doc_folder[docs_builder_id] = corresponding_template_folder

    # doc_builder_id_2_doc_folder: t.Dict[str, str] = {
    #     path.name.split('-')[1]: path.name
    #     for path in PROJ_TEMPLATE_DIR.glob('docs-*')
    #     if path.is_dir()
    # }
    assert (
        doc_builder_id_2_doc_folder
    ), f"templated_proj_folder: {PROJ_TEMPLATE_DIR}, with files: {list(PROJ_TEMPLATE_DIR.glob('*'))}"

    # return the internal configuration (atm it's just the mapping above)
    return doc_builder_id_2_doc_folder
