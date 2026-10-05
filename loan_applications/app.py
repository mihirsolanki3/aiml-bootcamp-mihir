"""
Loan Repayment Prediction Web Application
Standalone lightweight server with an interactive web UI.
Uses standard Python library http.server + predict.py pipeline.
Zero additional dependencies required!
"""

import http.server
import json
import socketserver
import urllib.parse
from predict import predict_loan_repayment, load_model

PORT = 5000

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Repayment AI Predictor</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0b0f19;
            --card-bg: rgba(22, 30, 49, 0.75);
            --card-border: rgba(255, 255, 255, 0.08);
            --primary: #3b82f6;
            --primary-glow: rgba(59, 130, 246, 0.35);
            --accent: #6366f1;
            --success: #10b981;
            --success-glow: rgba(16, 185, 129, 0.25);
            --danger: #ef4444;
            --danger-glow: rgba(239, 68, 68, 0.25);
            --warning: #f59e0b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --input-bg: rgba(15, 23, 42, 0.65);
            --input-border: rgba(148, 163, 184, 0.2);
            --transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.12), transparent 45%),
                        radial-gradient(circle at 85% 85%, rgba(99, 102, 241, 0.12), transparent 45%),
                        var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            padding: 32px 16px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            width: 100%;
            max-width: 1100px;
        }

        header {
            text-align: center;
            margin-bottom: 32px;
        }

        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 9999px;
            background: rgba(59, 130, 246, 0.12);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #60a5fa;
            font-size: 0.82rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            margin-bottom: 12px;
        }

        h1 {
            font-size: 2.3rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 40%, #93c5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }

        p.subtitle {
            color: var(--text-muted);
            font-size: 1.05rem;
            max-width: 620px;
            margin: 0 auto;
        }

        .grid-layout {
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            gap: 28px;
        }

        @media (max-width: 860px) {
            .grid-layout {
                grid-template-columns: 1fr;
            }
        }

        .glass-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 28px;
            box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 22px;
        }

        .card-title {
            font-size: 1.25rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .presets-row {
            display: flex;
            gap: 8px;
            margin-bottom: 22px;
            flex-wrap: wrap;
        }

        .preset-btn {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }

        .preset-btn:hover {
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.4);
            color: #93c5fd;
        }

        .form-group {
            margin-bottom: 18px;
        }

        .label-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 6px;
            font-size: 0.88rem;
            font-weight: 600;
        }

        .label-text {
            color: #e2e8f0;
        }

        .label-hint {
            color: var(--text-muted);
            font-size: 0.8rem;
        }

        .input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .input-prefix {
            position: absolute;
            left: 14px;
            color: var(--text-muted);
            font-weight: 600;
            pointer-events: none;
        }

        input[type="number"], input[type="text"] {
            width: 100%;
            background: var(--input-bg);
            border: 1px solid var(--input-border);
            border-radius: 12px;
            padding: 12px 14px;
            color: var(--text-main);
            font-family: inherit;
            font-size: 1rem;
            font-weight: 500;
            transition: var(--transition);
        }

        input.with-prefix {
            padding-left: 30px;
        }

        input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px var(--primary-glow);
            background: rgba(15, 23, 42, 0.9);
        }

        .slider-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-top: 6px;
        }

        input[type="range"] {
            flex: 1;
            accent-color: var(--primary);
            cursor: pointer;
        }

        .btn-predict {
            width: 100%;
            background: linear-gradient(135deg, #2563eb, #4f46e5);
            border: none;
            color: white;
            padding: 14px;
            border-radius: 12px;
            font-size: 1.05rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 8px 20px -4px var(--primary-glow);
            transition: var(--transition);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            margin-top: 8px;
        }

        .btn-predict:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 24px -4px var(--primary-glow);
            filter: brightness(1.1);
        }

        .btn-predict:active {
            transform: translateY(0);
        }

        /* Result Panel */
        .result-container {
            display: flex;
            flex-direction: column;
            height: 100%;
            justify-content: space-between;
        }

        .result-header {
            text-align: center;
            padding: 16px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            margin-bottom: 20px;
        }

        .outcome-badge {
            display: inline-block;
            padding: 10px 22px;
            border-radius: 9999px;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.01em;
            margin-bottom: 12px;
            transition: var(--transition);
        }

        .outcome-badge.approved {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            box-shadow: 0 0 20px var(--success-glow);
        }

        .outcome-badge.declined {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
            border: 1px solid rgba(239, 68, 68, 0.4);
            box-shadow: 0 0 20px var(--danger-glow);
        }

        .risk-pill {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
        }

        .prob-section {
            margin: 18px 0;
        }

        .prob-label-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .prob-bar-container {
            width: 100%;
            height: 14px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 9999px;
            overflow: hidden;
            display: flex;
        }

        .prob-bar-fill {
            height: 100%;
            transition: width 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .prob-bar-fill.repaid {
            background: linear-gradient(90deg, #10b981, #34d399);
        }

        .prob-bar-fill.default {
            background: linear-gradient(90deg, #f87171, #ef4444);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin: 20px 0;
        }

        .stat-box {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            padding: 14px;
            border-radius: 12px;
            text-align: center;
        }

        .stat-value {
            font-size: 1.45rem;
            font-weight: 800;
            margin-bottom: 2px;
        }

        .stat-value.repaid {
            color: #34d399;
        }

        .stat-value.default {
            color: #f87171;
        }

        .stat-label {
            font-size: 0.78rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .recommendation-box {
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.2);
            padding: 14px;
            border-radius: 12px;
            font-size: 0.88rem;
            line-height: 1.45;
            color: #bfdbfe;
            margin-bottom: 18px;
        }

        .drivers-list {
            margin-top: 10px;
        }

        .driver-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 7px 0;
            font-size: 0.83rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
        }

        .driver-name {
            color: #cbd5e1;
            font-weight: 500;
        }

        .driver-tag {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 6px;
        }

        .driver-tag.positive {
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
        }

        .driver-tag.negative {
            background: rgba(239, 68, 68, 0.15);
            color: #f87171;
        }

        footer {
            margin-top: 36px;
            color: var(--text-muted);
            font-size: 0.82rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-tag">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                Machine Learning Classifier
            </div>
            <h1>Loan Repayment Predictor</h1>
            <p class="subtitle">Predict whether an applicant will repay their loan based on financial profile and creditworthiness metrics.</p>
        </header>

        <div class="grid-layout">
            <!-- Input Form Card -->
            <div class="glass-card">
                <div class="card-header">
                    <span class="card-title">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                        Applicant Features
                    </span>
                </div>

                <div class="presets-row">
                    <span style="font-size: 0.78rem; color: var(--text-muted); align-self: center; margin-right: 4px;">Quick Presets:</span>
                    <button class="preset-btn" onclick="applyPreset('prime')">Prime Applicant</button>
                    <button class="preset-btn" onclick="applyPreset('average')">Average Applicant</button>
                    <button class="preset-btn" onclick="applyPreset('subprime')">High-Risk Applicant</button>
                </div>

                <form id="loanForm" onsubmit="event.preventDefault(); runPrediction();">
                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Annual Income</span>
                            <span class="label-hint">Dataset Avg: $56,838</span>
                        </div>
                        <div class="input-wrapper">
                            <span class="input-prefix">$</span>
                            <input class="with-prefix" type="number" id="income" value="65000" min="5000" max="500000" step="500" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Years Employed</span>
                            <span class="label-hint">Dataset Avg: 6.4 yrs</span>
                        </div>
                        <input type="number" id="years_employed" value="5.5" min="0" max="50" step="0.1" required>
                    </div>

                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Credit Score</span>
                            <span class="label-hint" id="creditScoreValue">Score: 710</span>
                        </div>
                        <input type="number" id="credit_score" value="710" min="300" max="850" step="1" oninput="syncCreditScore(this.value)" required>
                        <div class="slider-row">
                            <input type="range" id="credit_score_slider" min="300" max="850" value="710" oninput="syncCreditScore(this.value)">
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Debt-to-Income Ratio</span>
                            <span class="label-hint">e.g. 0.22 = 22%</span>
                        </div>
                        <input type="number" id="debt_ratio" value="0.22" min="0.0" max="1.0" step="0.01" required>
                    </div>

                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Loan Amount Requested</span>
                            <span class="label-hint">Dataset Avg: $56,920</span>
                        </div>
                        <div class="input-wrapper">
                            <span class="input-prefix">$</span>
                            <input class="with-prefix" type="number" id="loan_amount" value="30000" min="1000" max="500000" step="500" required>
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="label-row">
                            <span class="label-text">Decision Threshold</span>
                            <span class="label-hint" id="thresholdDisplay">Cutoff: 0.50</span>
                        </div>
                        <input type="range" id="threshold" min="0.10" max="0.90" step="0.05" value="0.50" oninput="document.getElementById('thresholdDisplay').textContent = 'Cutoff: ' + parseFloat(this.value).toFixed(2); runPrediction();">
                    </div>

                    <button type="submit" class="btn-predict" id="predictBtn">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                        Predict Repayment
                    </button>
                </form>
            </div>

            <!-- Prediction Result Card -->
            <div class="glass-card">
                <div class="card-header">
                    <span class="card-title">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
                        Prediction Analysis
                    </span>
                </div>

                <div class="result-container" id="resultContainer">
                    <div>
                        <div class="result-header">
                            <div id="outcomeBadge" class="outcome-badge approved">WILL REPAY</div>
                            <div id="riskLevel" class="risk-pill">Risk Level: Moderate Risk</div>
                        </div>

                        <div class="stats-grid">
                            <div class="stat-box">
                                <div id="repaidPct" class="stat-value repaid">59.7%</div>
                                <div class="stat-label">Repayment Likelihood</div>
                            </div>
                            <div class="stat-box">
                                <div id="defaultPct" class="stat-value default">40.3%</div>
                                <div class="stat-label">Default Risk</div>
                            </div>
                        </div>

                        <div class="prob-section">
                            <div class="prob-label-row">
                                <span>Repayment Probability</span>
                                <span id="probNumber">0.597</span>
                            </div>
                            <div class="prob-bar-container">
                                <div id="probBar" class="prob-bar-fill repaid" style="width: 59.7%;"></div>
                            </div>
                        </div>

                        <div id="recommendationText" class="recommendation-box">
                            Standard Approval - Applicant meets minimum requirements; standard monitoring recommended.
                        </div>

                        <div class="drivers-list">
                            <div style="font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; color: #94a3b8;">Feature Influence Summary</div>
                            <div id="driversList"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer>
            Trained on <code>loan_applications.csv</code> with StandardScaler &amp; LogisticRegression Pipeline.
        </footer>
    </div>

    <script>
        function syncCreditScore(val) {
            document.getElementById('credit_score').value = val;
            document.getElementById('credit_score_slider').value = val;
            document.getElementById('creditScoreValue').textContent = 'Score: ' + val;
        }

        const PRESETS = {
            prime: {
                income: 95000,
                years_employed: 8.5,
                credit_score: 770,
                debt_ratio: 0.12,
                loan_amount: 25000
            },
            average: {
                income: 57000,
                years_employed: 4.5,
                credit_score: 680,
                debt_ratio: 0.25,
                loan_amount: 45000
            },
            subprime: {
                income: 26000,
                years_employed: 1.0,
                credit_score: 540,
                debt_ratio: 0.45,
                loan_amount: 80000
            }
        };

        function applyPreset(type) {
            const p = PRESETS[type];
            if (!p) return;
            document.getElementById('income').value = p.income;
            document.getElementById('years_employed').value = p.years_employed;
            syncCreditScore(p.credit_score);
            document.getElementById('debt_ratio').value = p.debt_ratio;
            document.getElementById('loan_amount').value = p.loan_amount;
            runPrediction();
        }

        async function runPrediction() {
            const payload = {
                income: parseFloat(document.getElementById('income').value),
                years_employed: parseFloat(document.getElementById('years_employed').value),
                credit_score: parseFloat(document.getElementById('credit_score').value),
                debt_ratio: parseFloat(document.getElementById('debt_ratio').value),
                loan_amount: parseFloat(document.getElementById('loan_amount').value),
                threshold: parseFloat(document.getElementById('threshold').value)
            };

            const btn = document.getElementById('predictBtn');
            btn.style.opacity = '0.7';
            btn.innerText = 'Calculating...';

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await response.json();
                renderResult(data);
            } catch (err) {
                console.error(err);
                alert('Prediction error: ' + err.message);
            } finally {
                btn.style.opacity = '1';
                btn.innerHTML = `<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> Predict Repayment`;
            }
        }

        function renderResult(data) {
            const isRepaid = data.repaid_label === 1;
            const badge = document.getElementById('outcomeBadge');
            badge.className = 'outcome-badge ' + (isRepaid ? 'approved' : 'declined');
            badge.textContent = isRepaid ? 'WILL REPAY (APPROVED)' : 'NOT REPAID (HIGH RISK)';

            document.getElementById('riskLevel').textContent = 'Risk Rating: ' + data.risk_level;
            document.getElementById('repaidPct').textContent = data.repaid_percentage;
            document.getElementById('defaultPct').textContent = data.default_percentage;
            document.getElementById('probNumber').textContent = data.probability_repaid;

            const probBar = document.getElementById('probBar');
            probBar.className = 'prob-bar-fill ' + (isRepaid ? 'repaid' : 'default');
            probBar.style.width = data.repaid_percentage;

            document.getElementById('recommendationText').textContent = data.recommendation;

            const driversContainer = document.getElementById('driversList');
            driversContainer.innerHTML = '';
            if (data.feature_contributions) {
                data.feature_contributions.forEach(item => {
                    const isPos = item.impact.startsWith('Positive');
                    const div = document.createElement('div');
                    div.className = 'driver-item';
                    div.innerHTML = `
                        <span class="driver-name">${item.feature.replace('_', ' ').toUpperCase()}</span>
                        <span class="driver-tag ${isPos ? 'positive' : 'negative'}">${isPos ? 'Favorable' : 'Unfavorable'}</span>
                    `;
                    driversContainer.appendChild(div);
                });
            }
        }

        // Run default on page load
        window.addEventListener('DOMContentLoaded', runPrediction);
    </script>
</body>
</html>
"""


class LoanPredictionHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ("/", "/index.html"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/predict":
            # Support GET with query params
            params = urllib.parse.parse_qs(parsed.query)
            try:
                income = float(params.get("income", [60000])[0])
                years_employed = float(params.get("years_employed", [5])[0])
                credit_score = float(params.get("credit_score", [700])[0])
                debt_ratio = float(params.get("debt_ratio", [0.25])[0])
                loan_amount = float(params.get("loan_amount", [30000])[0])

                threshold = float(params.get("threshold", [0.45])[0])
                result = predict_loan_repayment(
                    income=income,
                    years_employed=years_employed,
                    credit_score=credit_score,
                    debt_ratio=debt_ratio,
                    loan_amount=loan_amount,
                    threshold=threshold,
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/predict":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                result = predict_loan_repayment(
                    income=float(data.get("income", 50000)),
                    years_employed=float(data.get("years_employed", 3)),
                    credit_score=float(data.get("credit_score", 650)),
                    debt_ratio=float(data.get("debt_ratio", 0.3)),
                    loan_amount=float(data.get("loan_amount", 25000)),
                    threshold=float(data.get("threshold", 0.45)),
                )
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(result).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Suppress verbose standard server logging
        pass


def run_server(port=PORT):
    load_model()
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), LoanPredictionHandler) as httpd:
        print(f"Loan Repayment Predictor Web UI running at http://localhost:{port}")
        print("Press Ctrl+C to stop the server.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            httpd.server_close()


if __name__ == "__main__":
    run_server()
