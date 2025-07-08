from flask import Blueprint, render_template, request, flash
from utils.gpt_utils import generate_content

repurposer_bp = Blueprint("repurposer_bp", __name__)


@repurposer_bp.route("/", methods=["GET", "POST"])
def repurposer():
    outputs = {}
    original_content = ""
    selected_formats = []

    if request.method == "POST":
        original_content = request.form["content"]
        selected_formats = request.form.getlist("formats")

        prompt_parts = ["You are a content repurposer. Repurpose this content into the selected formats below.\n"]
        format_instructions = {
            "tweet": "---Tweet Thread---",
            "linkedin": "---LinkedIn Post---",
            "email": "---Email Snippet---",
            "instagram": "---Instagram Caption---"
        }

        for fmt in selected_formats:
            prompt_parts.append(format_instructions[fmt])

        prompt_parts.append(f"\nContent:\n\"\"\"\n{original_content}\n\"\"\"")
        prompt = "\n".join(prompt_parts)

        result = generate_content(prompt)
        print("🧠 GPT Response:\n", result)

        def extract_between(text, start, end=None):
            try:
                start_idx = text.index(start) + len(start)
                if end:
                    end_idx = text.index(end, start_idx)
                    return text[start_idx:end_idx].strip()
                return text[start_idx:].strip()
            except ValueError:
                return ""

        for i, fmt in enumerate(selected_formats):
            start_marker = format_instructions[fmt]
            end_marker = format_instructions[selected_formats[i + 1]] if i + 1 < len(selected_formats) else None
            outputs[fmt] = extract_between(result, start_marker, end_marker)

        flash("✅ Content repurposed successfully!", "success")

    return render_template("repurposer.html", outputs=outputs, original_content=original_content, selected_formats=selected_formats)
