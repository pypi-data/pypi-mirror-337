# FlatForge Release Checklist

This document outlines the steps to follow when preparing a new release of FlatForge.

## Pre-Release Checklist

### Code Preparation

- [ ] Ensure all planned features for this release are implemented
- [ ] Check that all unit tests pass (`pytest tests/`)
- [ ] Verify test coverage is adequate for new features
- [ ] Run linting and fix any issues (`flake8 flatforge/`)
- [ ] Run static type checking if applicable (`mypy flatforge/`)
- [ ] Check for any deprecated features that should be removed
- [ ] Ensure backward compatibility with previous version, or document breaking changes

### Documentation

- [ ] Update all documentation related to new features
- [ ] Ensure user guide is complete and accurate
- [ ] Update CLI examples with new commands or features
- [ ] Update testing documentation if test procedures have changed
- [ ] Review README.md for completeness and accuracy
- [ ] Verify all links in documentation work correctly
- [ ] Update API documentation for any new or changed interfaces

### Version and Changelog

- [ ] Update version in `flatforge/__init__.py` to the new version
- [ ] Update CHANGELOG.md with all notable changes:
  - [ ] New features (Added)
  - [ ] Changes to existing functionality (Changed)
  - [ ] Fixed bugs (Fixed)
  - [ ] Deprecated features (Deprecated)
  - [ ] Removed features (Removed)
  - [ ] Security updates (Security)
- [ ] Ensure the changelog entry has the correct date (current date)

### Testing

- [ ] Run all unit tests again after changes
- [ ] Execute integration tests if available
- [ ] Test the package installation from local build
- [ ] Test all sample scripts and configurations
- [ ] Test any migration procedures from previous versions
- [ ] Verify that error handling works as expected
- [ ] Check package functions correctly on all supported platforms

## Release Process

### Package Building

- [ ] Clean previous build artifacts (`python build.py clean`)
- [ ] Build the package (`python build.py build`)
- [ ] Check the built distribution files:
  - [ ] Source distribution (.tar.gz)
  - [ ] Wheel distribution (.whl)
- [ ] Test installing the package from the built distributions

### Version Control

- [ ] Commit all changes with appropriate message
- [ ] Create a git tag for the new version (`git tag -a v0.x.y -m "Release v0.x.y"`)
- [ ] Push changes and tag to the main repository
- [ ] Create a GitHub release with release notes from the changelog

### Publication

- [ ] Upload the package to Test PyPI (`python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*`)
- [ ] Test installing from Test PyPI (`pip install --index-url https://test.pypi.org/simple/ flatforge`)
- [ ] Upload the package to PyPI (`python -m twine upload dist/*` or `python build.py publish`)
- [ ] Verify the package page on PyPI looks correct
- [ ] Test installing from PyPI (`pip install flatforge`)

## Post-Release

- [ ] Announce the release on relevant channels
- [ ] Update the documentation website if applicable
- [ ] Check GitHub issues and close any that were fixed in this release
- [ ] Create milestone for the next release
- [ ] Start planning for the next release
- [ ] Celebrate the successful release! 🎉

## Version Scheme

FlatForge follows semantic versioning (SemVer):

- **MAJOR** version for incompatible API changes
- **MINOR** version for added functionality in a backward-compatible manner
- **PATCH** version for backward-compatible bug fixes

Example: 1.2.3
- 1 = Major version
- 2 = Minor version
- 3 = Patch version

## Release Naming Convention

- Release tags: `v{MAJOR}.{MINOR}.{PATCH}` (e.g., `v0.3.0`)
- Test script naming: `test_feature_v{MAJOR}.{MINOR}.{PATCH}_{YYYYMMDD}.py` 