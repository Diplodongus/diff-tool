import logging

def generate_html_diff(diff, file, golden_file):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: monospace; white-space: pre; line-height: 1.5; }}
            .extra {{ background-color: #e6ffec; color: #24292f; }}
            .missing {{ background-color: #ffebe9; color: #24292f; }}
            .modified {{ background-color: #ffefc6; color: #24292f; }}
            .diff-line {{ padding: 2px 5px; margin: 2px 0; }}
            .diff-marker {{ display: inline-block; width: 20px; text-align: center; }}
        </style>
    </head>
    <body>
    <h1>Config Diff: {file} vs {golden_file}</h1>
    """

    logging.debug(f"Generating HTML for {len(diff)} diff entries")

    for diff_type, line in diff:
        if diff_type == 'extra':
            html += f"<div class='diff-line extra'><span class='diff-marker'>+</span>{line}</div>"
            logging.debug(f"Added extra line to HTML: + {line}")
        elif diff_type == 'missing':
            html += f"<div class='diff-line missing'><span class='diff-marker'>-</span>{line}</div>"
            logging.debug(f"Added missing line to HTML: - {line}")
        elif diff_type == 'modified':
            html += f"<div class='diff-line modified'><span class='diff-marker'>~</span>{line}</div>"
            logging.debug(f"Added modified line to HTML: ~ {line}")
        else:  # unchanged
            html += f"<div class='diff-line'><span class='diff-marker'>&nbsp;</span>{line}</div>"
            logging.debug(f"Added unchanged line to HTML: {line}")

    html += "</body></html>"
    logging.debug(f"HTML generation complete. HTML length: {len(html)}")
    return html