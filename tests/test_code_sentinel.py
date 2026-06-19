import pytest
from code_sentinel import CodeSentinel, DetectionResult

@pytest.fixture
def detector():
    """Fixture providing the CodeSentinel instance."""
    # Threshold 50 ensures 'eval' (100) and '__import__' (50) are caught.
    return CodeSentinel(threshold=50.0, entropy_limit=3.5)

def test_scan_benign_simple_math(detector):
    """Test that simple arithmetic is not flagged."""
    code = "x = 1 + 1\ny = x * 2"
    result = detector.scan(code)
    assert result.is_adversarial is False
    assert result.score == 0.0
    assert len(result.reasons) == 0

def test_scan_benign_function_def(detector):
    """Test that a benign function definition is not flagged."""
    code = "def foo():\n    pass"
    result = detector.scan(code)
    assert result.is_adversarial is False
    assert result.score == 0.0
    assert len(result.reasons) == 0

def test_scan_high_entropy_string(detector):
    """Test detection of high entropy strings (obfuscation)."""
    # A base64-like string has high entropy
    code = 's = "SGVsbG8gV29ybGQhISE="'
    result = detector.scan(code)
    # Depending on threshold, this might or might not be adversarial alone.
    # With default threshold 50 and entropy score 25, it shouldn't be adversarial alone,
    # but it should add to the score.
    assert result.score > 0
