import pytest

from h2o_engine_manager.clients.notebook_engine_image.image import NotebookEngineImage


@pytest.fixture(scope="function")
def notebook_engine_image_i1(notebook_engine_image_client_super_admin):
    created_image = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent="workspaces/global",
        notebook_engine_image=NotebookEngineImage(
            image="img1",
        ),
        notebook_engine_image_id="img1",
    )
    name = created_image.name

    yield created_image

    notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=name)


@pytest.fixture(scope="function")
def notebook_engine_image_i2(notebook_engine_image_client_super_admin):
    created_image = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent="workspaces/global",
        notebook_engine_image=NotebookEngineImage(
            image="img2",
        ),
        notebook_engine_image_id="img2",
    )
    name = created_image.name

    yield created_image

    notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=name)


@pytest.fixture(scope="function")
def notebook_engine_image_i3(notebook_engine_image_client_super_admin):
    created_image = notebook_engine_image_client_super_admin.create_notebook_engine_image(
        parent="workspaces/global",
        notebook_engine_image=NotebookEngineImage(
            image="img3",
        ),
        notebook_engine_image_id="img3",
    )
    name = created_image.name

    yield created_image

    notebook_engine_image_client_super_admin.delete_notebook_engine_image(name=name)