import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="function")
def generated_rows(request):
    def row_values(index, value):
        return mockobj.mock_calls[index][1][1][value]

    with patch(
        "snowfakery.output_streams.DebugOutputStream.write_single_row"
    ) as mockobj:
        mockobj.row_values = row_values
        yield mockobj
