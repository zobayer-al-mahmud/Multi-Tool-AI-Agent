# Contributing

Thanks for your interest in contributing! 🎉

## Getting Started

1. Fork the repository and clone your fork.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Set up your `.env` based on `.env.example`.
5. Prepare databases:

   ```powershell
   python .\scripts\create_databases.py
   ```

6. Run the app:

   ```powershell
   python .\main.py
   ```

## Submitting Changes

1. Create a feature branch from `main`.
2. Make your changes with clear, descriptive commits.
3. Ensure the app runs without errors.
4. Open a Pull Request with:
   - A clear description of the change
   - Any relevant screenshots or logs
