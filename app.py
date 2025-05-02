from flask import Flask, render_template_string, request
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)
model = SentenceTransformer('all-MiniLM-L6-v2')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Member Directory</title>
    <style>
    body {
        font-family: 'Segoe UI', sans-serif;
        max-width: 900px;
        margin: auto;
        padding: 2rem;
        background: #f9fafb;
    }
    h1 {
        text-align: center;
        margin-bottom: 2rem;
        color: #333;
    }
    form {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
    }
    input, select {
        padding: 0.5rem 1rem;
        font-size: 1rem;
        border: 1px solid #ccc;
        border-radius: 6px;
        width: auto;
        flex: unset;
    }
    input[type='submit'] {
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        width: auto;
        flex: none;
        background-color: #2563eb;
        color: white;
        cursor: pointer;
        border: none;
    }
    .carousel {
        display: flex;
        overflow-x: auto;
        gap: 1rem;
        padding-bottom: 1rem;
    }
    .carousel .card {
        min-width: 300px;
        flex: 0 0 auto;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    .logo {
        width: 60px;
        height: 60px;
        object-fit: contain;
    }
    .info {
        flex: 1;
    }
    .info h2 {
        margin: 0;
        font-size: 1.25rem;
    }
    .info p {
        margin: 0.25rem 0;
        color: #555;
    }
    .info a {
        color: #2563eb;
        text-decoration: none;
    }
    .tags {
        margin-top: 0.5rem;
    }
    .tag {
        display: inline-block;
        background: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 999px;
        margin-right: 6px;
        font-size: 0.875rem;
        text-decoration: none;
    }
</style>
</head>
<body>
    <h1>Member Directory</h1>
    <form method="get">
        <input type="text" name="search" placeholder="Search by keyword or concept..." value="{{ search }}">
        <select name="industry">
            <option value="">All Industries</option>
            <option value="Biotech" {% if industry == 'Biotech' %}selected{% endif %}>Biotech</option>
            <option value="Nonprofit" {% if industry == 'Nonprofit' %}selected{% endif %}>Nonprofit</option>
            <option value="Academic Institution" {% if industry == 'Academic Institution' %}selected{% endif %}>Academic Institution</option>
        </select>
        <select name="location">
            <option value="">All Locations</option>
            <option value="Vancouver" {% if location == 'Vancouver' %}selected{% endif %}>Vancouver</option>
            <option value="Toronto" {% if location == 'Toronto' %}selected{% endif %}>Toronto</option>
            <option value="Ottawa" {% if location == 'Ottawa' %}selected{% endif %}>Ottawa</option>
        </select>
        <select name="tag" id="advanced">
            <option value="">-- Select Tag --</option>
        </select>
        <input type="submit" value="Search">
</form>
<div style="margin-top: 2rem;"></div>
    {% if tag or search %}
    {% for m in filtered %}
    <div class="card">
    <img src="{{ m.logo }}" class="logo" alt="{{ m.name }} logo">
    <div class="info">
        <h2>{{ m.name }}</h2>
        <p>{{ m.industry }} · {{ m.location }}</p>
        <p><a href="{{ m.website }}" target="_blank">Visit Website</a></p>
        <div class="tags" style="margin-top: 0.5rem;">
            {% for tag in m.tags %}
            <a href="?search={{ tag }}&industry={{ industry }}&location={{ location }}" class="tag">{{ tag }}</a>
            {% endfor %}
                </div>
    </div>
</div>
    </div>
    {% endfor %}
{% else %}
    {% for industry in filtered | map(attribute='industry') | unique %}
    <h2>{{ industry }}</h2>
    <div class="carousel">
        {% for m in filtered if m.industry == industry %}
        <div class="card">
            <img src="{{ m.logo }}" class="logo" alt="{{ m.name }} logo">
            <div class="info">
                <h2>{{ m.name }}</h2>
                <p>{{ m.industry }} · {{ m.location }}</p>
                <p><a href="{{ m.website }}" target="_blank">Visit Website</a></p>
                <div class="tags">
                    {% for tag in m.tags %}
                    <a href="?search={{ tag }}&industry={{ industry }}&location={{ location }}" class="tag">{{ tag }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% endfor %}
{% endif %}

    <script>
    const industryTags = {
        "Biotech": ["Lab Services", "Cell Culture Tools", "Tissue Engineering", "Oncology", "Biologics", "AI", "Antibody Discovery"],
        "Nonprofit": ["Funding Agency"],
        "Academic Institution": ["Academic Research"]
    };

    function updateTagOptions() {
        const industry = document.querySelector('select[name="industry"]').value;
        const tagSelect = document.getElementById('advanced');
        tagSelect.innerHTML = '<option value="">-- Select Tag --</option>';

        if (industryTags[industry]) {
            industryTags[industry].forEach(tag => {
                const option = document.createElement('option');
                option.value = tag;
                option.textContent = tag;
                if (tag === "{{ tag }}") option.selected = true;
                tagSelect.appendChild(option);
            });
        }
    }

    document.addEventListener('DOMContentLoaded', updateTagOptions);
    document.querySelector('select[name="industry"]').addEventListener('change', updateTagOptions);
    </script>
</body>
</html>
"""

@app.route('/')
def directory():
    tag = request.args.get("tag", "").strip()
    search = request.args.get("search", "").strip()
    query = tag or search
    industry = request.args.get("industry", "")
    location = request.args.get("location", "")

    # Sample data
    members = [
        {"name": "LifeLabs", "industry": "Biotech", "location": "Toronto", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/LifeLabs_logo.png/300px-LifeLabs_logo.png", "website": "https://www.lifelabs.com", "tags": ["Lab Services"]},
        {"name": "BioTalent Canada", "industry": "Nonprofit", "location": "Ottawa", "logo": "https://www.biotalent.ca/wp-content/uploads/2022/06/BioTalent-Logo-2021.png", "website": "https://www.biotalent.ca", "tags": ["Funding Agency"]},
        {"name": "STEMCELL Technologies", "industry": "Biotech", "location": "Vancouver", "logo": "https://www.stemcell.com/content/dam/stemcell/images/logos/stemcell-logo.png", "website": "https://www.stemcell.com", "tags": ["Cell Culture Tools"]},
        {"name": "Aspect Biosystems", "industry": "Biotech", "location": "Vancouver", "logo": "https://cdn.globenewswire.com/Attachment/LogoDisplay/1077369?filename=Aspect_Biosystems_Logo.png&size=3", "website": "https://www.aspectbiosystems.com", "tags": ["Tissue Engineering"]},
        {"name": "Zymeworks", "industry": "Biotech", "location": "Vancouver", "logo": "https://upload.wikimedia.org/wikipedia/en/b/bf/Zymeworks_logo.png", "website": "https://www.zymeworks.com", "tags": ["Oncology", "Biologics"]},
        {"name": "AbCellera", "industry": "Biotech", "location": "Vancouver", "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/AbCellera_logo.svg/800px-AbCellera_logo.svg.png", "website": "https://www.abcellera.com", "tags": ["AI", "Antibody Discovery"]},
        {"name": "University of British Columbia", "industry": "Academic Institution", "location": "Vancouver", "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/University_of_British_Columbia_coat_of_arms.svg/200px-University_of_British_Columbia_coat_of_arms.svg.png", "website": "https://www.ubc.ca", "tags": ["Academic Research"]},
    ]

    # Precompute embeddings
    for m in members:
        text = m["name"] + ' ' + m["industry"] + ' ' + ' '.join(m["tags"])
        m["embedding"] = model.encode(text, convert_to_tensor=True)

    # Tag-specific filtering takes priority
    if tag:
        filtered = [m for m in members if tag in m["tags"]]
    elif search:
        query_embedding = model.encode(search, convert_to_tensor=True)
        scored = [(m, util.pytorch_cos_sim(query_embedding, m["embedding"]).item()) for m in members]
        scored.sort(key=lambda x: x[1], reverse=True)
        filtered = [m for m, score in scored if score > 0.3]
    else:
        filtered = members

    # Filter by dropdowns
    filtered = [m for m in filtered if
                (industry == "" or m["industry"] == industry) and
                (location == "" or location in m["location"])]

    return render_template_string(HTML_TEMPLATE, filtered=filtered, search=search, tag=tag, industry=industry, location=location)

if __name__ == '__main__':
    app.run(debug=True)
