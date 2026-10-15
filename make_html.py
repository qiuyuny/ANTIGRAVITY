import re

with open('report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Make it nice HTML
html_content = ""
for line in text.split('\n'):
    if line.startswith('### '):
        html_content += f"<h3>{line[4:]}</h3>\n"
    elif line.startswith('*(Insert'):
        html_content += '''
        <div style="text-align: center; margin: 30px 0;">
            <img src="plot1_nodes.png" style="max-width: 80%; margin-bottom: 20px;"><br>
            <img src="plot2_bits.png" style="max-width: 80%; margin-bottom: 20px;"><br>
            <img src="plot3_time.png" style="max-width: 80%; margin-bottom: 20px;"><br>
        </div>
        '''
    elif line.strip() == '':
        html_content += "<br>\n"
    else:
        # replace $O(m)$ with mathjax spans or just italic
        line = re.sub(r'\$(.*?)\$', r'<i>\1</i>', line)
        html_content += f"<p>{line}</p>\n"


html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            margin: 40px auto;
            max-width: 800px;
            color: #333;
            padding: 0 20px;
        }}
        h3 {{
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        p {{
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <h1>Patricia Tree Search Performance Report</h1>
    {html_content}
</body>
</html>"""

with open('report.html', 'w', encoding='utf-8') as f:
    f.write(html)

