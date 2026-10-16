from src.ai_gitgen.safety import mask_secrets, limit_diff


def test_mask_secrets():
    text = (
        "API_KEY=abc123\n"
        "TOKEN=xyz789\n"
        'PASSWORD="my-password"\n'
        "DEBUG=True"
    )

    result = mask_secrets(text)

    assert "API_KEY=****" in result
    assert "TOKEN=****" in result
    assert "PASSWORD=****" in result
    assert "DEBUG=True" in result
    assert "abc123" not in result
    assert "xyz789" not in result
    assert "my-password" not in result


def test_limit_diff_max_lines():
    diff = "\n".join(f"line {i}" for i in range(1, 11))

    result = limit_diff(diff, max_lines=5)

    assert len(result.splitlines()) == 5
    assert "line 5" in result
    assert "line 6" not in result


def test_limit_diff_max_files():
    diff = (
        "diff --git a/a.py b/a.py\n"
        "+change a\n"
        "diff --git a/b.py b/b.py\n"
        "+change b\n"
        "diff --git a/c.py b/c.py\n"
        "+change c\n"
    )

    result = limit_diff(diff, max_files=2)

    assert "a/a.py" in result
    assert "b/b.py" in result
    assert "c/c.py" not in result