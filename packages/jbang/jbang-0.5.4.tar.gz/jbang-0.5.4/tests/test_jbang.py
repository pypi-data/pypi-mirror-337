import pytest
import jbang

def test_version_command():
    """Test version command."""
    print("\nTesting version command...")
    try:
        out = jbang.exec('--version',capture_output=True)
        assert out.returncode == 0
        print("✓ Version command works")
    except Exception as e:
        pytest.fail(f"✗ Version command failed: {e}")

def test_catalog_script():
    """Test catalog script execution."""
    print("\nTesting catalog script...")
    try:
        jbang.exec('properties@jbangdev')
        print("✓ Catalog script works")
    except Exception as e:
        pytest.fail(f"✗ Catalog script failed: {e}")

def test_error_handling():
    """Test error handling."""
    print("\nTesting error handling...")
    with pytest.raises(Exception):
        jbang.exec('nonexistent-script-name')
    print("✓ Error handling works") 