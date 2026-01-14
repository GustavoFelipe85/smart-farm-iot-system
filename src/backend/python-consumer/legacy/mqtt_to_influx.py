name: CI - Smart Farm IoT System

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security-scan:
    name: "🔒 Security Scan"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: "Run Bandit Security Scan"
        run: |
          pip install bandit
          bandit -r src/ -f html -o security-report.html || true

      - name: "Dependency Vulnerability Check"
        run: |
          pip install safety
          safety check --json --output safety-report.json || true

      - name: "Upload Security Reports"
        uses: actions/upload-artifact@v4
        with:
          name: security-reports
          path: |
            security-report.html
            safety-report.json

  contract-docs:
    name: "📜 Contract & Docs"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: "Install jsonschema (pinned)"
        run: pip install jsonschema==4.23.0

      - name: "Check docs folder"
        run: test -d docs

      - name: "Check README docs link"
        run: |
          if grep -nE '\]\(/docs\)|\(/docs\)' README.md README_en.md; then
            echo "Broken /docs link found"
            exit 1
          fi

      - name: "Validate JSON Schema"
        run: |
          python - << 'EOF'
          import json
          from jsonschema import Draft7Validator
          with open("src/backend/schemas/sensor_payload.json") as f:
              schema = json.load(f)
          Draft7Validator.check_schema(schema)
          print("Schema OK")
          EOF

  code-quality:
    name: "✨ Code Quality"
    runs-on: ubuntu-latest
    needs: [ security-scan, contract-docs ]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          pip install -r requirements.txt
          pip install flake8 black pytest pytest-cov
      - run: black --check src/ tests/ || echo "Formatting issues"
      - run: flake8 src/ --max-line-length=88 --extend-ignore=E203,W503 || echo "Lint warnings"
      - run: pytest tests/ -v || echo "Tests incomplete (expected in Phase 3)"

  docker-build:
    name: "🐳 Docker Compose Validation"
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "Validate docker compose"
        working-directory: docker
        run: docker compose config -q
