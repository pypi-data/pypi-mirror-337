import jinja2


def test_jinja_extension() -> None:
    env = jinja2.Environment(extensions=["jamldump.jinja2.Jaml"])
    template = env.from_string("{{ 1 | jaml }}")
    result = template.render()
    assert result == "---\n1\n...\n"
