# Falliant

A terminal-based block stacking game inspired by classic block stacking games, written in Python using the curses library.

![Falliant Screenshot](falliant/images/screenshot.png)

## Features

- Classic block-stacking gameplay
- Multiple starting levels with increasing difficulty
- Hold piece functionality
- Next piece preview
- Level progression system
- High score tracking with player initials
- Clean terminal UI with color support

## Requirements

- Python 3.6+
- A terminal that supports curses and colors (most modern terminals do)

## Installation

### Option 1: Install from PyPI

```bash
pip install falliant
```

### Option 2: Install from source

1. Clone or download this repository
2. Install directly:

```bash
# Install globally
pip install .

# Or install in user directory (no admin rights needed)
pip install --user .
```

### Option 3: Development setup with virtual environment

1. Clone or download this repository
2. Set up a virtual environment and install:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .
```

## How to Play

After installation, simply run:

```bash
falliant
```

If installed in development mode with a virtual environment, make sure the environment is activated before running the command.

### Controls

- **←, ↓, →** or **A, S, D**: Move block left, down, or right
- **↑** or **W**: Rotate block
- **Space**: Drop block to bottom
- **C**: Hold current block
- **P**: Pause/resume game
- **Q**: Quit to menu

### Game Rules

- Arrange falling blocks to create complete horizontal lines
- Completed lines will disappear and award points
- The game speeds up as you level up
- Level increases every 10 lines cleared
- The game ends when blocks stack up to the top of the board
- If you achieve a high score, you can enter your three-letter initials

### Scoring System

- 1 line: 40 × level
- 2 lines: 100 × level
- 3 lines: 300 × level
- 4 lines: 1200 × level (Falliant!)
- Top 10 high scores are tracked and saved locally

## Known Issues

- Terminal resizing during gameplay may cause display issues
- Some terminals might not display colors correctly

## Troubleshooting

If you encounter display issues:

1. Try running in a different terminal
2. Make sure your terminal supports curses and colors
3. Ensure your terminal is sized appropriately (at least 80×24)

## Development

### Contributing

To contribute to Falliant:

1. Fork the repository
2. Set up a virtual environment as described in the installation section
3. Make your changes
4. Submit a pull request

### Publishing to PyPI

Falliant uses GitHub Actions for automated publishing to PyPI. When a new release is created on GitHub, the package is automatically built and published.

To create a new release manually:

1. Update the version in `pyproject.toml`
2. Build the package:

   ```bash
   python -m build
   ```

3. Upload to PyPI:

   ```bash
   python -m twine upload dist/falliant-x.y.z*
   ```

Alternatively, use the GitHub Actions workflow:

1. Create a new release on GitHub
2. The GitHub Action will automatically build and publish the package

### Automated Version Bumping

A GitHub workflow is available to bump versions automatically:

1. Go to the Actions tab in the repository
2. Select the "Bump Version" workflow
3. Click "Run workflow"
4. Choose the version type to bump (major, minor, patch)
5. A pull request will be created with the version change

## Project Structure

```bash
falliant/               # Project root
├── pyproject.toml      # Package configuration
├── README.md           # Documentation
├── LICENSE             # MIT License
├── MANIFEST.in         # Package manifest
├── .github/            # GitHub Actions workflows
├── falliant/           # Python package
│   ├── __init__.py     # Package initialization
│   ├── __main__.py     # Entry point
│   ├── block.py        # Block class
│   ├── constants.py    # Game constants
│   ├── game.py         # Game logic
│   ├── renderer.py     # Display functions
│   ├── ui.py           # User interface
│   └── images/         # Image assets
```

## License

This game is provided under the MIT License. See the LICENSE file for details.

---

Created by: [Henry Sowell](https://github.com/veteranbv)
