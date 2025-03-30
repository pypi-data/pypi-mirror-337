from setuptools import setup, find_packages

setup(
    name="dynamic-cursor-rules",
    version="1.0.2",
    description="Generate and manage documentation and task tracking for Cursor IDE projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Cursor Rules Team",
    author_email="info@cursorrules.dev",
    url="https://github.com/cursor-rules/cursor-rules",
    project_urls={
        "Bug Tracker": "https://github.com/cursor-rules/cursor-rules/issues",
        "Documentation": "https://github.com/cursor-rules/cursor-rules#readme",
        "Source Code": "https://github.com/cursor-rules/cursor-rules",
    },
    packages=find_packages(),
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="cursor, ide, documentation, rules, ai, tasks, project-management",
    python_requires=">=3.9",
    install_requires=[
        "pyyaml>=6.0",
        "markdown>=3.3.0",
        "gitpython>=3.1.0",
    ],
    extras_require={
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.5.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "isort>=5.0.0",
            "flake8>=4.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ],
    },
    scripts=[
        "bin/cursor-rules",
        "bin/cursor-tasks",
    ],
    entry_points={
        "console_scripts": [
            "cursor-rules=cursor_rules.cli:main",
            "cursor-tasks=cursor_rules.cli:main",
        ],
    },
) 