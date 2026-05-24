from flask import Flask, request

app = Flask(__name__)

def determinant(matrix):
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for col in range(n):
        minor = []
        for row in range(1, n):
            minor_row = []
            for c in range(n):
                if c != col:
                    minor_row.append(matrix[row][c])
            minor.append(minor_row)

        det += ((-1) ** col) * matrix[0][col] * determinant(minor)

    return det

def html_page(content):
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Determinants Calculator</title>
    <script>
        window.MathJax = {{
            tex: {{ inlineMath: [['\\\\(', '\\\\)'], ['$', '$']] }},
            svg: {{ fontCache: 'global' }}
        }};
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
    <style>
        body {{
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            color: #222;
        }}
        .container {{
            width: 90%;
            max-width: 950px;
            margin: 30px auto;
        }}
        h1, h2 {{ text-align: center; }}
        h1 {{ color: #1f2937; }}
        h2 {{ color: #374151; font-weight: normal; }}
        .card {{
            background: white;
            padding: 25px;
            margin: 22px 0;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        p {{ line-height: 1.6; }}
        select, input {{
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #bbb;
        }}
        table {{ border-collapse: collapse; margin: 20px 0; }}
        td {{ padding: 6px; }}
        input[type=number] {{
            width: 70px;
            text-align: center;
        }}
        button, .btn {{
            background: #2563eb;
            color: white;
            padding: 11px 18px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
        }}
        .result-table td {{
            border: 1px solid #888;
            padding: 12px 18px;
            background: #f9fafb;
            text-align: center;
        }}
        .error {{ color: #b91c1c; font-weight: bold; }}
    </style>
    <script>
        function generateMatrix() {{
            const size = parseInt(document.getElementById("size").value);
            const container = document.getElementById("matrix-container");
            container.innerHTML = "";

            const table = document.createElement("table");

            for (let i = 0; i < size; i++) {{
                const row = document.createElement("tr");

                for (let j = 0; j < size; j++) {{
                    const cell = document.createElement("td");
                    const input = document.createElement("input");
                    input.type = "number";
                    input.step = "any";
                    input.name = `cell_${{i}}_${{j}}`;
                    input.required = true;
                    input.placeholder = "0";
                    cell.appendChild(input);
                    row.appendChild(cell);
                }}

                table.appendChild(row);
            }}

            container.appendChild(table);
        }}
    </script>
</head>
<body>
    <div class="container">
        {content}
    </div>
</body>
</html>"""

@app.route("/", methods=["GET"])
def home():
    return html_page("""
        <h1>Numerical Methods Online Calculator</h1>
        <h2>Topic: Determinants</h2>

        <section class="card">
            <h3>Mathematical Discussion</h3>
            <p>
                A determinant is a scalar value computed from a square matrix. It gives important information about
                the matrix, especially whether the matrix is invertible. If the determinant is zero, the matrix is
                singular and has no inverse. If the determinant is nonzero, the matrix is invertible.
            </p>

            <p>For a 2 × 2 matrix:</p>

            <p>
                \\[
                A =
                \\begin{bmatrix}
                a & b \\\\
                c & d
                \\end{bmatrix}
                \\]
            </p>

            <p>
                \\[
                \\det(A) = ad - bc
                \\]
            </p>

            <p>
                For larger matrices, the determinant may be computed using cofactor expansion.
            </p>
        </section>

        <section class="card">
            <h3>Worked Example 1: 2 × 2 Matrix</h3>

            <p>
                \\[
                A =
                \\begin{bmatrix}
                4 & 3 \\\\
                2 & 1
                \\end{bmatrix}
                \\]
            </p>

            <p>Step 1: Use the formula \\( \\det(A) = ad - bc \\).</p>
            <p>\\[ \\det(A) = (4)(1) - (3)(2) \\]</p>

            <p>Step 2: Multiply the values.</p>
            <p>\\[ \\det(A) = 4 - 6 \\]</p>

            <p>Step 3: Subtract.</p>
            <p>\\[ \\det(A) = -2 \\]</p>
        </section>

        <section class="card">
            <h3>Worked Example 2: 3 × 3 Matrix</h3>

            <p>
                \\[
                A =
                \\begin{bmatrix}
                1 & 2 & 3 \\\\
                0 & 4 & 5 \\\\
                1 & 0 & 6
                \\end{bmatrix}
                \\]
            </p>

            <p>Step 1: Expand along the first row.</p>

            <p>
                \\[
                \\det(A)
                = 1(4 \\cdot 6 - 5 \\cdot 0)
                - 2(0 \\cdot 6 - 5 \\cdot 1)
                + 3(0 \\cdot 0 - 4 \\cdot 1)
                \\]
            </p>

            <p>Step 2: Simplify each minor.</p>
            <p>\\[ \\det(A) = 1(24) - 2(-5) + 3(-4) \\]</p>

            <p>Step 3: Multiply and add.</p>
            <p>\\[ \\det(A) = 24 + 10 - 12 = 22 \\]</p>
        </section>

        <section class="card">
            <h3>Interactive Determinant Calculator</h3>

            <form method="POST" action="/calculate">
                <label for="size"><b>Select Matrix Size:</b></label>
                <select name="size" id="size" onchange="generateMatrix()">
                    <option value="2">2 × 2</option>
                    <option value="3">3 × 3</option>
                    <option value="4">4 × 4</option>
                    <option value="5">5 × 5</option>
                    <option value="6">6 × 6</option>
                </select>

                <div id="matrix-container"></div>

                <button type="submit">Calculate Determinant</button>
            </form>
        </section>

        <script>generateMatrix();</script>
    """)

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        size = int(request.form.get("size", 0))

        if size < 1 or size > 6:
            raise ValueError("Matrix size must be from 1 to 6 only.")

        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                value = request.form.get(f"cell_{i}_{j}", "").strip()
                if value == "":
                    raise ValueError("Empty entries are not allowed.")
                row.append(float(value))
            matrix.append(row)

        det = determinant(matrix)

        rows = ""
        for row in matrix:
            rows += "<tr>" + "".join(f"<td>{value:g}</td>" for value in row) + "</tr>"

        return html_page(f"""
            <h1>Determinant Result</h1>

            <section class="card">
                <h3>Input Matrix</h3>

                <table class="result-table">
                    {rows}
                </table>

                <h3>Computed Determinant</h3>

                <p style="font-size: 1.3rem; font-weight: bold;">
                    \\[
                    \\det(A) = {det:g}
                    \\]
                </p>

                <p>
                    The determinant was computed manually using recursive cofactor expansion.
                </p>

                <a href="/" class="btn">Calculate Another Matrix</a>
            </section>
        """)

    except Exception as e:
        return html_page(f"""
            <section class="card">
                <h2>Error</h2>
                <p class="error">{str(e)}</p>
                <a href="/" class="btn">Go Back</a>
            </section>
        """)

handler = app