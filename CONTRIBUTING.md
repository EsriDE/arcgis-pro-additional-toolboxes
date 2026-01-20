
# Contributing Guidelines

Thank you for considering a contribution to this project!

## How to Contribute

### 1. Fork the repository
Create your own fork of the project to submit changes.

### 2. Create a feature branch
Use descriptive branch names such as:
feature/new-tool
fix/copy-layer-crash
improvement/progress-handling

### 3. Follow the project structure
- Python toolboxes (`.pyt`) should remain clean and readable  
- Shared logic belongs into separate `.py` modules (e.g. `layerutils.py`)
- Avoid embedding unnecessary business logic directly inside tool classes

### 4. Code Style
- Use meaningful function and variable names
- Add docstrings for all tools and helper functions
- Follow ArcGIS Pro Python Toolbox best practices  
- Avoid breaking backward compatibility whenever possible

### 5. Submit a Pull Request
- Describe the purpose of your change
- Reference related issues if applicable
- Keep PRs focused and avoid bundling unrelated changes

### 6. Testing
Before submitting:
- Test the toolbox in ArcGIS Pro
- Validate behavior using different maps, layers, and feature classes
- Ensure no hardcoded paths remain in the code

Your contributions help the toolbox ecosystem grow and stay maintainable.  
Thank you!