"""
Test for the deliberate bug: mutable default in ChatRequest.filters

This test demonstrates the bug and shows how it causes state bleed.
The bug is in src/api/models.py where ChatRequest.filters = [] as default.
"""
import pytest
from src.api.models import ChatRequest


@pytest.fixture(autouse=True)
def cleanup_model_state():
    """Clean up any modifications to the model fields after each test."""
    yield
    # Reset the filters default to empty list after each test (if it's mutable)
    default_field = ChatRequest.model_fields.get("filters")
    if default_field and isinstance(default_field.default, list):
        default_field.default.clear()


class TestMutableDefaultBug:
    """Test and document the mutable default bug."""
    
    def test_filters_not_shared_between_requests(self):
        """
        This test FAILS with the current buggy code and PASSES after fix.
        
        The bug: ChatRequest uses a mutable default (list) for filters.
        If the class-level default is mutable, mutating it affects all future instances.
        
        """
        filters_field = ChatRequest.model_fields["filters"]
        
        # Attempt to mutate the class-level default (only possible if it's a mutable list)
        if isinstance(filters_field.default, list):
            filters_field.default.append("leaked_filter")
        
        # Create a fresh instance - should always have empty filters
        fresh_request = ChatRequest(query="hello")
        
        # Test the behavior: filters should be empty for the new instance
        assert fresh_request.filters == [], (
            f"State bleed detected! Got: {fresh_request.filters}. "
            f"The mutable default [] is shared across all instances. "
        )



if __name__ == "__main__":
    pytest.main([__file__, "-v"])
