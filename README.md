# ProjectDoctor 🩺

**A Python library to assess codebase health, detect structural risks, and guide maintainability improvements.**

ProjectDoctor is a static analysis tool designed to help developers gain immediate insights into the health of their Python projects. It scans your codebase for common "code smells" and structural issues, generating a clear and actionable report that highlights risks and promotes better maintainability.


---

## 🎯 Core Features

*   **Maintainability Score:** Get an at-a-glance score (0-100) to quickly gauge your project's overall health.
*   **Comprehensive Detectors:** Automatically identifies common issues, including:
    *   **High Complexity:** Flags functions with high cyclomatic complexity that are difficult to test and maintain.
    *   **Circular Imports:** Detects circular dependencies between modules, which can cause runtime errors and indicate poor architecture.
    *   **Long Functions & Large Files:** Finds code that should be refactored into smaller, more manageable units.
    *   **Duplicate Code:** Identifies copy-pasted logic across your codebase.
    *   **Dead Code:** Uses `vulture` to find unused functions, classes, and variables that can be safely removed.
    *   **Structural Problems:** Checks for best practices, like the presence of a `tests/` directory.
*   **Multiple Output Formats:** Generate reports directly in your command line, or as `Markdown` or `JSON` files for documentation and integration with other tools.
*   **Customizable Thresholds:** Easily override the default analysis thresholds to fit your project's specific standards.

---

## ⚙️ Installation

ProjectDoctor requires Python 3.8 or newer.

1.  **Clone the repository (or download the source code):**
    ```bash
    git clone https://github.com/mohTalib/ProjectDoctor.git
    ```
    ```
    cd projectdoctor
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate on Windows (PowerShell)
    .\venv\Scripts\activate

    # Activate on macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the package in editable mode:**
    This command uses the pinned dependencies in `pyproject.toml` to create a stable environment.
    ```bash
    pip install -e .
    ```

---

## 🚀 Usage

The primary entry point is the `projectdoctor` command-line tool.

### Basic Analysis

To analyze a project in the current directory, simply run:

```bash
projectdoctor analyze .
