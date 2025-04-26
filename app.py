from flask import Flask, request, render_template_string, jsonify
from sentence_transformers import SentenceTransformer, util

app = Flask(__name__)

model = SentenceTransformer('all-MiniLM-L6-v2')

members = [
    {"id": 1, "name": "AbCellera", "bio": "Antibody discovery and development platform.", "industry": "Biotech", "location": "British Columbia", "size": "400", "founded": 2012, "logo": "https://logo.clearbit.com/abcellera.com", "website": "https://www.abcellera.com"},
    {"id": 2, "name": "Zymeworks", "bio": "Protein therapeutics and antibody drug conjugates.", "industry": "Biotech", "location": "British Columbia", "size": "300", "founded": 2003, "logo": "https://logo.clearbit.com/zymeworks.com", "website": "https://www.zymeworks.com"},
    {"id": 3, "name": "STEMCELL Technologies", "bio": "Cell culture media and tools for life sciences research.", "industry": "Biotech", "location": "British Columbia", "size": "2000", "founded": 1993, "logo": "https://logo.clearbit.com/stemcell.com", "website": "https://www.stemcell.com"},
    {"id": 4, "name": "Medicago", "bio": "Plant-based vaccines and mRNA therapeutics.", "industry": "Biotech", "location": "Quebec", "size": "500", "founded": 1999, "logo": "https://logo.clearbit.com/medicago.com", "website": "https://www.medicago.com"},
    {"id": 5, "name": "Bausch Health", "bio": "Pharmaceutical products in various therapeutic areas.", "industry": "Pharma", "location": "Quebec", "size": "21000", "founded": 1853, "logo": "https://logo.clearbit.com/bauschhealth.com", "website": "https://www.bauschhealth.com"},
    {"id": 6, "name": "Fusion Pharmaceuticals", "bio": "Radiopharmaceuticals for cancer therapy.", "industry": "Pharma", "location": "Ontario", "size": "100", "founded": 2014, "logo": "https://logo.clearbit.com/fusionpharma.com", "website": "https://www.fusionpharma.com"},
    {"id": 7, "name": "Satellos Bioscience", "bio": "Regenerative medicine therapies.", "industry": "Biotech", "location": "Ontario", "size": "50", "founded": 2018, "logo": "https://logo.clearbit.com/satellos.com", "website": "https://www.satellos.com"},
    {"id": 8, "name": "Synaptive Medical", "bio": "Neurosurgical imaging and robotic platforms.", "industry": "Medtech", "location": "Ontario", "size": "200", "founded": 2012, "logo": "https://logo.clearbit.com/synaptivemedical.com", "website": "https://www.synaptivemedical.com"},
    {"id": 9, "name": "Baylis Medical", "bio": "Medical devices for cardiology and spine surgery.", "industry": "Medtech", "location": "Ontario", "size": "800", "founded": 1986, "logo": "https://logo.clearbit.com/baylismedical.com", "website": "https://www.baylismedical.com"},
    {"id": 10, "name": "Opsens", "bio": "Innovative optical sensor solutions.", "industry": "Medtech", "location": "Quebec", "size": "150", "founded": 2003, "logo": "https://logo.clearbit.com/opsens.com", "website": "https://www.opsens.com"}
]

for member in members:
    member['embedding'] = model.encode(member['bio'], normalize_embeddings=True).tolist()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Life Sciences Member Directory</title>
<style>
    body { font-family: Arial, sans-serif; margin: 0; background: #f5f5f5; }
header {
  background: url('https://images.pexels.com/photos/3183197/pexels-photo-3183197.jpeg') center/cover no-repeat;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-shadow: 1px 1px 4px #000;
}    header h1 { font-size: 36px; }
    .content { padding: 20px; text-align: center; }
    .intro { margin: 20px 0; font-size: 18px; color: #555; }
    .search-bar { text-align: center; margin-bottom: 20px; }
    input, select, button { padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid #ccc; }
    button { background-color: #007BFF; color: white; border: none; }
    .card { background: white; border-radius: 10px; padding: 15px; margin: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: inline-block; width: 250px; vertical-align: top; }
    .card img { width: 100px; height: 100px; object-fit: contain; margin-bottom: 10px; }
    .card h3 { margin: 0; font-size: 18px; color: #333; }
    .card p { font-size: 14px; color: #666; }
    .card a { color: #007BFF; text-decoration: none; font-size: 14px; }
    #memberList { text-align: center; }
    .no-results { font-size: 18px; color: #777; margin-top: 20px; }
</style>
<script>
async function searchMembers() {
    const query = document.getElementById('searchInput').value;
    const industry = document.getElementById('industryFilter').value;
    const location = document.getElementById('locationFilter').value;

    const response = await fetch(`/search?q=${encodeURIComponent(query)}&industry=${encodeURIComponent(industry)}&location=${encodeURIComponent(location)}`);
    const data = await response.json();

    renderMembers(data.results);
}

function renderMembers(list) {
    const container = document.getElementById('memberList');
    container.innerHTML = '';
    if (list.length === 0) {
        container.innerHTML = '<div class="no-results">No results found. Please search again.</div>';
    } else {
        list.forEach(member => {
            const div = document.createElement('div');
            div.className = 'card';
            div.innerHTML = `<img src="${member.logo}"><h3>${member.name}</h3><p>${member.bio}</p><a href="${member.website}" target="_blank">Visit Website</a>`;
            container.appendChild(div);
        });
    }
}

window.onload = () => searchMembers();
</script>
</head>
<body>
<header>
  <h1>Innovation and Collaboration in Life Sciences</h1>
</header>
<div class="content">
<div class="intro">Discover our vibrant community of leading-edge life sciences organizations, collaborating to push innovation forward.</div>
<div class="search-bar">
<input id="searchInput" placeholder="Search...">
<select id="industryFilter">
    <option value="">All Industries</option>
    <option value="Biotech">Biotech</option>
    <option value="Medtech">Medtech</option>
    <option value="Pharma">Pharma</option>
</select>
<select id="locationFilter">
    <option value="">All Locations</option>
    <option value="British Columbia">British Columbia</option>
    <option value="Ontario">Ontario</option>
    <option value="Quebec">Quebec</option>
</select>
<button onclick="searchMembers()">Search</button>
</div>
<div id="memberList"></div>
</div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    industry_filter = request.args.get('industry', '')
    location_filter = request.args.get('location', '')

    if not query:
        return jsonify(results=members)

    query_embedding = model.encode(query, normalize_embeddings=True)

    scored_members = []
    for member in members:
        score = util.cos_sim(query_embedding, member['embedding'])[0][0].item()
        if (industry_filter == '' or member['industry'] == industry_filter) and \
           (location_filter == '' or member['location'] == location_filter):
            scored_members.append((member, score))

    scored_members.sort(key=lambda x: x[1], reverse=True)
    filtered = [m for m, score in scored_members if score > 0.2]

    return jsonify(results=filtered)

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

