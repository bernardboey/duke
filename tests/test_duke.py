from duke import ui

def test_prepend_tab():
    assert ui.prepend_tab("hello") == "\thello"
