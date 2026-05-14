import os
import shutil
import re

# 1. Copy image
source_image = r"C:\Users\P.Navya Sarada\.gemini\antigravity\brain\90a832c5-346a-4799-abad-22b1beedf80b\premium_fashion_hero_bg_1778784255623.png"
dest_dir = r"d:\outfit_iq\outfit_iq\static\images"
dest_image = os.path.join(dest_dir, "hero_bg.png")

os.makedirs(dest_dir, exist_ok=True)
shutil.copy(source_image, dest_image)

# 2. Update CSS
css_path = r"d:\outfit_iq\outfit_iq\static\css\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

css = re.sub(
    r"background: linear-gradient.*?center/cover;",
    "background: linear-gradient(rgba(248, 246, 246, 0.70), rgba(250, 245, 247, 0.85)), url('../images/hero_bg.png') center/cover;\n    background-attachment: fixed;",
    css,
    flags=re.DOTALL
)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 3. Cache bust CSS in HTML
templates = [
    r"d:\outfit_iq\outfit_iq\templates\index.html",
    r"d:\outfit_iq\outfit_iq\templates\login.html",
    r"d:\outfit_iq\outfit_iq\templates\cart.html",
    r"d:\outfit_iq\outfit_iq\templates\product_detail.html"
]

for tmpl in templates:
    with open(tmpl, "r", encoding="utf-8") as f:
        html = f.read()
    
    # replace base case
    html = html.replace("{% static 'css/style.css' %}", "{% static 'css/style.css' %}?v=7")
    # replace if it was already modified (though usually Django static doesn't get ?v attached inside the tag, it gets attached outside)
    html = html.replace("{% static 'css/style.css' %}\"?v=6", "{% static 'css/style.css' %}?v=7\"")
    html = html.replace("?v=6\">", "?v=7\">")
    
    with open(tmpl, "w", encoding="utf-8") as f:
        f.write(html)
