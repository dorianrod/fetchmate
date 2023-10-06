from utils.load_template import render_template


def build_context_prompt(data):
    data["prompt"] = ". ".join(data.get("prompts", []))
    base_path = "/scripts/services/build_prompt/"
    role = render_template(f"{base_path}role.tmpl", {"engine": data["engine"]})
    messages = [
        render_template(f"{base_path}context.tmpl", data),
        render_template(f"{base_path}structure.tmpl", data),
        render_template(
            f"{base_path}question.tmpl",
            data,
        ),
    ]
    return role, messages
