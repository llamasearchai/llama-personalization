"""Basic tests for the llamapersonalization package."""

import pytest


def test_import():
    """Test that the main package can be imported."""
    try:
        import llamapersonalization
    except ImportError as e:
        pytest.fail(f"Failed to import llamapersonalization: {e}")


def test_version():
    """Test that the package has a version attribute."""
    import llamapersonalization

    assert hasattr(llamapersonalization, "__version__")
    assert isinstance(llamapersonalization.__version__, str)


# Add more core tests later, e.g.:
# - Test profile store connection/basic CRUD (mocked DB/Redis)
# - Test preference model instantiation
# - Test basic personalization logic (mocked models/data)
