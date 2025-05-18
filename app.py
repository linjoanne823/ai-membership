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
        margin: auto;
        padding: 2rem;
       
    adding: 4rem 2rem;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(to bottom, rgba(255,255,255,0.9), rgba(255,255,255,0.9)),
    background-size: contain;       
    }
   
    .content {
    position: relative;
    z-index: 1;
    padding: 1.5rem;
   
    margin: auto;
    background: rgba(255, 255, 255, 0.9); /* semi-transparent so parallax shows through */
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.05);
    border-radius: 10px;
}


    h1 {
        text-align: center;
        margin-bottom: 2rem;
        color: #333;
    }
    h2 {
        font-size: 2rem;
        color: #0c1c5c;
    }
    form {
        display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    justify-content: center;
    align-items: center;
    margin-bottom: 3rem;
    background: linear-gradient(to right, #f0f4ff, #ffffff);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.06);
    }
    input, select {
        padding: 0.75rem 1rem;
    font-size: 1rem;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.03);
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
    }
    input[type='submit'] {
        padding: 0.75rem 1.25rem;
    font-size: 1.25rem;
    background: #116aa3;
    color: white;
    cursor: pointer;
    border: none;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    transition: background 0.3s ease;
    }
input[type="submit"]:hover {
    background-color: white;
    color: #116aa3;
    border-color: #116aa3;
    transform: scale(1.05);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }

  input[type="submit"]:active {
    transform: scale(0.95);
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  }
.carousel {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1rem;
  padding: 2rem 1rem;
  scroll-behavior: smooth;
}
.carousel-wrapper {
  max-width: 1060px; /* 3 cards x 300px + gaps */
  margin: 0 auto;
  position: relative;
}

.carousel-track {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  gap: 1rem;
  padding: 1rem 0;
}
.carousel-track::-webkit-scrollbar {
  display: none; /* hide scroll bar for clean look */
}

.carousel-btn {
  background: rgba(255,255,255,0.8);
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem 1rem;
  z-index: 1;
}

.carousel-btn.left {
  position: absolute;
  left: 0;
}

.carousel-btn.right {
  position: absolute;
  right: 0;
}
     
.card {
  flex: 0 0 250px;
  background: white;
  border-radius: 12px;
  padding: 1rem;
  box-shadow: 5px 4px 12px #116aa3;
  scroll-snap-align: start;
  transition: transform 0.3s;
}

    .card:hover {
    transform: scale(1.015);
    }
    .logo {
        width: 100px;
        height: 100px;
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
        padding: 6px 14px;
    border-radius: 999px;
    transition: background 0.2s ease;
    }
    .select-wrapper {
  position: relative;
  display: inline-block;
  width: 250px;
}


</style>
</head>

<body>
 <div class="parallax-bg"></div>
    <div class="content">

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
<div class="carousel-wrapper">
  <h2 class="carousel-title">{{ industry }}</h2>
  <div class="carousel-track">
    {% for m in filtered if m.industry == industry %}
    <div class="card">
      <img src="{{ m.logo }}" class="logo" alt="{{ m.name }} logo">
      <h3>{{ m.name }}</h3>
      <p>{{ m.industry }} · {{ m.location }}</p>
      <p><a href="{{ m.website }}" target="_blank">Visit Website</a></p>
      <div class="tags">
        {% for tag in m.tags %}
        <a href="?search={{ tag }}&industry={{ industry }}&location={{ location }}" class="tag">{{ tag }}</a>
        {% endfor %}
      </div>
    </div>
    {% endfor %}
  </div>
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

  document.addEventListener('DOMContentLoaded', () => {
    updateTagOptions();

    const urlParams = new URLSearchParams(window.location.search);
    const hasFilter = urlParams.get('industry') || urlParams.get('q');

    if (hasFilter) {
      // Convert all carousels into stacked vertical grids
      document.querySelectorAll('.carousel-track').forEach(track => {
        track.style.display = 'flex';
        track.style.flexWrap = 'wrap';
        track.style.overflowX = 'unset';
        track.style.gap = '1.5rem';
      });

      // Widen the cards a bit for the grid look
      document.querySelectorAll('.card').forEach(card => {
        card.style.flex = '0 1 calc(25% - 1rem)'; // Smaller card width
        card.style.maxWidth = '250px'; // Optional max width for smaller look
      });
    }

    document.querySelector('select[name="industry"]').addEventListener('change', updateTagOptions);
  });
</script>


    </div>
</div>
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
        {"name": "LifeLabs", "industry": "Biotech", "location": "Toronto", "logo": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAaoAAAB2CAMAAACu2ickAAABj1BMVEX///8TSZ941fQDAw3l/gQAPpsAQZwMRp729/oANJf+ssxyQSMGvwAzXqoANpgwWKWMosvU3OsAO5rg5/HsnwN9kMAAAACNncYAP5sAQ50JG5fn7fXQ2utee7bAzOKGnMhNcLKvvdrqvATt/wRLzgHaAAxyNQCer9IlUqIAKJQAMJb7/+YAAJEGqihpMQDYAAAJDpbdu9dtORW1wt1qhbtHykZ0AIz/7/R1hYft5+T4/f5+foHqiIvY2NkqKi8/Zay9qZ/PwrrrlQPRjQX+4uz+x9m35/n+u9Ll9vzT8PtpIQDb0cumi31lKACZeWny7uurq65+VD1sbG/NmJq3AAD+4uPmTE/wq61CQkYdHSKZmZrfOj+X3/elnZezm44VAADvq1P++e17TzT548L669L21KHyv2vuqCnRrgUZHAzS6AX3/7Pw/ob9/+3o/jf5/83q/lvy/29v2D+r55SK2YzA6cKt56wAH5J41nfg9uByebtGT6lrcrm7pNBEAIzVzueaXKqRRqOhZrCDLJivf7sWgVDDAAAPYUlEQVR4nO2d+ZvbxBnHrd1KI7OVbI+ijYQOy21T2SbdwNpsiOlGCQ2QkINA05ZSytGLnvQmpW0KtPzhlSzrmkPSjL1r53nm+8M++9gj6dV85njnncOdjpCQkJCQkJDQbki9um0LhFro1qvPLPWqsdi2KUJ1uvVMphf29l7btjVCVKmvl0nFur1ti4TIuvoMQmpv7862bRIiScVJiXq1m0Jbv1TCudg93SKSEr7FDopMSjSBu6dbFFKiWu2cXqWQ2tvbtmVCiKikXrq2bdOEKlKppN64u23bhCq6SiP17aOb27ZNqKKrNFIHAtWO6SqN1MGRaAB3TDRSB0fCrdgxvU4hdXCwbcuEEBkUUsf3tm2ZEKIFpU7dF+3fzuk1IqnjB9u2SwjTgkTq4FhUqh3UbQKp+2JQtZO6g5ESw99d1W2knzoWpHZWi/dKXvr9B2/S0j1Uz9MqIaIWr+299MbR0dHxW/eoDsXp9f3zNEmIqmvXbt68Rnf8rr19ePj9czRHiFNvvnx4uP/oB9s2Q6hJ1xJQ+49+uG07hBqUgtp/dOVH27ZEqFanby9BxaQu0ff0qAN/lsh3nXM0Tagk9eE7Kaj9R5eufJecZhB60lSHqfSuHVz0n16fXg0H2zaBS6cv/3gFKiZ16QqxUo0iXbaBVBJQpuF5W7opjcYTd0uPno2qYiju1969fpiBWpIiVSojghVMqeSNo1JzbfrOZY3GEOjbQjWGFU2Mdpepp+++U3BKSZF6Kl+xcVBngQpMu6nOsNDPtKTYbQ2VVi3zehtUpw/fvl7mtCR1ieT+GTKhSp0Jql72IPmsuhJ/1T7sHqrFnTu38X05b9698eDwsMppReonhLuPyaSeRlT96eoJu4cqgbW3995P379xc6kb79978NbB/aPjD/ZRJaQuXSEEKkaQTOqpRGVlWbSDqGLdeemNo+OjpY5jJXF1GimSTxFRKtVTiUrZbVSdzt23jg7Kwkl975VEHxLubdAqlUDFo2a34ubBcS2pC0t9RLj3DEcF7FhAoOJRCw9QvXe/idQrvyDdO2/e88pkBaZpziNr80NggSrV3Z8d19epnxPvbSqVe0tWDsj3N/0eAtVK6oMjdlIoKsU8w/cQqHLdOKK3fhRSKCp4lu8oUBW6iwx7c1IfE/upRAiqVpEQXglUJZ2irOpbv45AtWExxABP98usDlekLvySeoFAtVGxhGsr9SojdeFX1PRro2I4G0igqur0ECd14UNqcm5Ujh+aXhBEWhQE8+GozRw/PyrH9cN+PNwbhjO3ZrKLgGoQmxlf5rd6L8cfxanN/qhdcoLYJkEerlh9UJC68DE1NR8q35QglBUbpLItCOHYbJri50NlhIES3162FEWx5ORBQ1qdQVEZQ5CYubxMGja8mj+P3wlmT5GDkAcX43zVy4dInaLElJbiQDWIOdl4kBcoEMxrGx4OVE5f02UbfZAezYipq6iMeVcB5avmNS8X9vTqO9myHrHMt6dinVq8HrM6/PU3ytocKmcuK7RgvKTAoAYWMypnbpPnPQGMSIZWUPVtJBAT5z4tVjbQSEsWAJT6jLBYUcXd1W9++7WKnqOlZUXVnxJn94vsmM6pb8eISjVrnmVPCRWrQDVQA9KUAfSIXtCoSyl8wNLZIqHME/bvHiKk2qOq9w6MiDpnkssa00CwoqLNT69MxTMxR2WFPTJlOSA8aNateQyMWDpWZlQOSoqAKkjVqxoGotXnAclCF9RXqdU9LEqgl7UBDOvLBcQek6OSAHXCdI49xqA36Il0lrA1+zKY3zWjGqfuG5bPmbp4p0NtJ9B7dMlvx9xX1VcrIKNNbR/tnQiCWGUMasufnbFdzOaaFvXrM59jxVILVA3ZjgduSaswYked5AzaRBbMqPJ5z2Q0oMeCFW8QmwbAUQFblpHFqArSxrul5g/IyWMgLNWz7iq5O57Mw3DYm8zrBv0cqNBqtQFUro7lg2xJkRdoNkTLpd0jvQ+7s54YCSwZePGodGAYhh96Vmku1EJyHUVlyWMzDENzXCZse9WL5vl3sV8Zj5Xjp4z6kbK6RB6mqfzJyl3yFa2GFc86wI2jciz0ArmXjRLdOerryqR5L3ZUMwig1q+kVk25eEq/mryKylaG2ZUDr9QiTKtPlzKrgFRqt9VRkBRAME4BOZNhx+/HcjuOjXd3uXhQ/X7TqLAWvTsslS4XvR0kGMkxBO5pPlaGi4YYBNVvKqigVzZhVDRz1aw28lpqIW/sejqAo/T/udbpDHVNk+Mxgj+hm8+D6rkqqj9gCRhRYR0V0j0bUvV+aDOTiCdaQfqwn9crpAUsoQKoLz8rKiMoX+Vmn6PcY/ljLf1HleNR3MVe8g7xe0VDqr08qDqfVFDh0QpGVKiviHXpPsJSxq3cWGQ9LxZIBL3krCuYEzrMq09WVap224Q2W129xGDiJKgWHTVB1Y+olnGhqrSAn+Dfs6HCKlUXi0kgVlp9NMHmUOXLrORR9fMclUwYLuSAKzW+QEVoBzK5k/jPRaunjafxjUNATciF6o9lVH/Cv2cbV2lNlSqmKVdvNMZSbAyVm2UvEtTLUcER4aqiuNmlcuYWZtMjNYMlKqkfLEeMYY+akAtV55sl/Rn/ehWUGCOkyNGKQRUDKVLQGSDOfBczc2OonOxRSrXq5qi6pFxXixawVAyLV7MDavTS6A6WfZWhJ0V0Tq9/fKj+8q1Cf6WmMu029w5RVFigIM4JBJWMlezNocqMti5WPq9HVYygypVxUWSAolFzthcjGsbtxHxqdNQpqc6m4kP1t68X+js1VbvIuodOGRGGuCpCEx9+bBtV3gJWTCuNQoBuUhrB2cTthHFlMoKw443pY2A+VJ+WUH1GTdUKFRbjJji2sZOI4kQT8KIy3HBozmMtZ95VblT5VoqKaRWPSZEpk8Ve3mgOJzXxWz5Un5VQ0YtBK1QOGlMCkY9LQhOhjSQXKt/s2VC2ki0PdjKVLo+9kZHdiA1VUeL08sfVEaFiBSQUqjcxY1jOTJuQZ6BT8aH6qISKnqoVKnTMlITLcKFpFPRe7KjUEOhoOBjYxaPYUBV7ySrTcjOkINo6IMXPZ9r08ePHCq2JTLU2qn/QU7VCRd3ZWCsZDfgyoxpJpHn0khhR5V1uNexloq8HLNkjVC1jsGx+68SHalGg+pSeqhUqzAFsJcyhZ0WFBYExMaLKXUAkFDPHi6INe3Q/jy4+VJ0XW3gV7VBhm7BaaU1Ui6i5gDCiGuZDZMS0PqFQADhmh7U2qppErVBd5EKFrQ9iQ+W1eCgjqrzIYaXI7RFhMa2rSLQuqpqu6kxRoYWSCRWysCLd9YpmJyOqvCEnBFtCQFjHZuPT+/VaF1VNV7WzqJxS6wcUXYo8zwuiHqgu4Nwgqo7aHxNqll4zj0jQuqhquqqz7KvWQmUWj5Sl/kBNR4aqY4xMW89pbRJVMvPb62JLYiDTPs41Ub1Yl4jTAwRys7B93yyo8klbALHZFD/gGwLT3YpcgzlAq5bO4lxwOuvfWamu/eMcAttzY9AsNL8YUBVnNOBzhHHx50SVx6Yh3QB1FOiVqgUAw0GWfKjUZ59f6nJtvrRCZaCBJYU+ZV0jBlT5lC1xmTlnDLAYAtcvIh7Mu+VcYTnAgw+Vc/nZRM//qzYVX7i2btEOXQyosiaOMEHZ4UdVBJYaHu+YpYP3gNRkbSE+VEaK6nJ9meCcBAnaW1+IAVWW1CJWX05UTm4+sQBUZESFX4NPklLFh2q2QlUftWqHCvMrLJ6DMtujyqsxceadF5VLnK+iyctzhuqE4OJDdXGJ6vI/61O1Q2VgE/Y8ATIeVMQZB05U+dftep+8uWTorPhQ/TNF9Xl9qpb7q9AFm0BrbX0hDlTkXFKbUOn1a+a7reJF+boewuIrmhBU0HWIQq7Sn292Klqj8lEfsK5aqRT/iqGvyl6ZvOIr9w9pqIBGaKDzdwA1M+4l5U2JxV2rJNglaIp2lWmlamqo2u5aRG2QyJs9Es2yhd6oWDzArN4ohFuNppkRNFSSHeHX5Y9HV8ZRSAzWr1VkoU3SYInqcdO926LCRsFAIue3H0CgkFdfMaDKzSJkU78whYpKsjW0ahfLp5HZqnASEf2G3Jfi76vaoQovN3vqHYa9wHM0DggIUWd1lE4mEDeCsKAqSga6TlYtb+qgo5Jsu+qRFJF6JKccJX6VALeoGEzye4DtUP076aomjfdujYqwMxeOy2c7qMbIg1kAjRg4y1GBwCOquEgtNm5UekU1tNtE1lMbSvmvmkVnq1cZzpOLbD2YVZtMI8ofNG0fWeJC1W3TU7HssHfxzc1AliNvGI5GYd8MerC8I45UEnNU6ewTJlga75YG3TAapVYt3OG42g7XopJsGIRG7EGo8XVFm4AsessGWzaUvNFghUv1zaJI4Kvk6OJBlXRVje5fh+kwBJ94toOtJFF0C91nCkDNThCKysuay8uq4xIhaV7QUyC6Ha8eVXJShZysSStvGEV3j2il8gNlZRx5niZZsHQnlulFHlRP/hOrYUyViOXcCl9vY0hmTw/zwVhQpe1S6XakPceNqAiSq6EqdBf/cnNz5Uk0f5YoHlRfnJycfNHi3kxHjPjYpl+67AlWGJlQOSQ02b2zf6ioqNfa1b1R6rQxb9eZryKrikqNSZ3Qf1SsENtpME6LI0ZSa0g+FROqjkutw9DL/qMOgSknjEg2Ovr1xw3roiDTfA8HqhdiUk/a3Jv14J5QbtHIAJ04UmFD1ZnRzlfqN04tQt8jlik5wpy5Rb/2jXS2c5c5UH15cvJlq3tzHIc1xfbaVw1RulrDESMUIag6LiCs6bAkvzlcqw86Q7xpA13i+U+O2aX82JBkd9dbsUTJoTIqtWXzF6PSrbLa/DaWE7vMtI4EKHBsNp6xRBGKqrMw0VPSrGVQqBlV7OW5yA+oAdijbQxQ+xrET+9JlkOzngk4npKCfnUxwCctm79OZzSsqH7xfP5qs7mE/uLfEpPeqzu/ETS8xwTvFowh0LNKnBw4mG6pcfLfLKs2T8PJ6vPHS4d8FuXX2pauhXWenGtq3RIuYMtdepmryZl2Kl3x5cl/mZ/CqEE470G52Acig2A4qwfN9Ar5Rf4wWg7dZK0oBpQrsI8HybEuMB5cBf3mbDdGw2i1EkvR5uf0y5qfn/zvfH5+1Bm4y61Vrtu0RWI9qY7DfX/VYLo2SX6Ov9361cmt83uY0BpST17YtglC7fTkq21bINRSgtTTonYDKiEhISEhISEhoV3R/wHG5cfAYTJLvQAAAABJRU5ErkJggg==", "website": "https://www.lifelabs.com", "tags": ["Lab Services"]},
        {"name": "BioTalent Canada", "industry": "Nonprofit", "location": "Ottawa", "logo": "data:image/png;base64,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", "website": "https://www.biotalent.ca", "tags": ["Funding Agency"]},
        {"name": "STEMCELL Technologies", "industry": "Biotech", "location": "Vancouver", "logo": "data:image/png;base64,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", "tags": ["Cell Culture Tools"]},
        {"name": "Aspect Biosystems", "industry": "Biotech", "location": "Vancouver", "logo": "data:image/png;base64,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", "tags": ["Tissue Engineering"]},
        {"name": "Zymeworks", "industry": "Biotech", "location": "Vancouver", "logo": "data:image/png;base64,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", "website": "https://www.zymeworks.com", "tags": ["Oncology", "Biologics"]},
        {"name": "AbCellera", "industry": "Biotech", "location": "Vancouver", "logo": "data:image/png;base64,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", "website": "https://www.abcellera.com", "tags": ["AI", "Antibody Discovery"]},
        {"name": "University of British Columbia", "industry": "Academic Institution", "location": "Vancouver", "logo": "data:image/png;base64,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", "website": "https://www.ubc.ca", "tags": ["Academic Research"]},
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
    filtered.sort(key=lambda x: (x["industry"] != "Biotech", x["name"]))


    return render_template_string(HTML_TEMPLATE, filtered=filtered, search=search, tag=tag, industry=industry, location=location)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
