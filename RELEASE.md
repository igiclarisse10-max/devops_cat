# Release Guide

This document describes the release process for the To-Do List application.

## Overview

The release pipeline automates:
- **Version Management**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Git Tagging**: Automatic creation of annotated Git tags
- **Changelog Updates**: Automatic CHANGELOG.md updates
- **Docker Image Building**: Build and push Docker images to Docker Hub
- **GitHub Releases**: Create release pages on GitHub with release notes
- **Slack Notifications**: Notify team of successful/failed releases

## Prerequisites

Before running a release, ensure:

1. **Git credentials** are configured locally:
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

2. **Docker Hub credentials** (optional, for Docker image push):
   - Add to GitHub Secrets:
     - `DOCKER_HUB_USERNAME`
     - `DOCKER_HUB_PASSWORD`

3. **Slack webhook** (optional, for notifications):
   - Add to GitHub Secrets:
     - `SLACK_WEBHOOK_URL`

## How to Create a Release

### Option 1: Using GitHub UI

1. Go to your repository on GitHub
2. Navigate to **Actions** → **Release Pipeline**
3. Click **Run workflow** (button on the right)
4. Enter the version number (e.g., `1.0.1`)
5. Select the release type (major/minor/patch) - informational only
6. Click **Run workflow**

### Option 2: Using GitHub CLI

```bash
gh workflow run release.yml \
  -f version=1.0.1 \
  -f release_type=minor
```

### Option 3: Manual Release (Local)

```bash
# 1. Update VERSION file
echo "1.0.1" > VERSION

# 2. Update CHANGELOG.md manually with changes

# 3. Commit changes
git add VERSION CHANGELOG.md
git commit -m "Release v1.0.1"

# 4. Create and push tag
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin main
git push origin v1.0.1

# 5. (Optional) Build Docker image
docker build -t yourname/todo-app:1.0.1 --build-arg VERSION=1.0.1 .
docker push yourname/todo-app:1.0.1
```

## Version Numbering

Follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
  ```bash
  gh workflow run release.yml -f version=2.0.0 -f release_type=major
  ```

- **MINOR** (1.X.0): New features, backward compatible
  ```bash
  gh workflow run release.yml -f version=1.1.0 -f release_type=minor
  ```

- **PATCH** (1.0.X): Bug fixes, patches
  ```bash
  gh workflow run release.yml -f version=1.0.1 -f release_type=patch
  ```

## What Happens During Release

### 1. Version & Changelog Updates
- VERSION file is updated
- CHANGELOG.md is updated with new section for the release
- Changes are committed to main branch

### 2. Git Tag Creation
- An annotated Git tag is created (e.g., `v1.0.1`)
- Tag is pushed to remote repository

### 3. Docker Image Building (if credentials configured)
- Docker image is built with version tag
- Image is tagged as `:latest`
- Image is pushed to Docker Hub

### 4. GitHub Release Creation
- Release page is created on GitHub
- Release notes are extracted from CHANGELOG.md
- Docker image URL is included in release notes

### 5. Slack Notification (if webhook configured)
- Success message is sent to Slack with release version and workflow link
- Or failure message if any step fails

## Viewing Releases

### On GitHub
```
https://github.com/igiclarisse10-max/devops_cat/releases
```

### Using Git
```bash
# List all tags
git tag -l

# Show specific tag details
git show v1.0.0

# Show annotated tag info
git tag -l -n9
```

## Docker Image Usage

### Pull from Docker Hub
```bash
# Using latest version
docker pull yourusername/todo-app:latest

# Using specific version
docker pull yourusername/todo-app:1.0.0

# Run container
docker run -p 5000:5000 yourusername/todo-app:1.0.0
```

### Using docker-compose
```bash
# Update docker-compose.yml to reference the released image
# Then run:
docker-compose up -d
```

## Troubleshooting

### Release workflow fails with "Invalid version format"
- Ensure version follows semantic versioning: `X.Y.Z` (e.g., `1.0.0`)
- No `v` prefix in the version input field (tag is created with `v` prefix automatically)

### Docker image not pushed to Docker Hub
- Verify `DOCKER_HUB_USERNAME` and `DOCKER_HUB_PASSWORD` are set in GitHub Secrets
- Ensure Docker Hub account has push permission

### No Slack notification
- Verify `SLACK_WEBHOOK_URL` is set in GitHub Secrets
- Check that webhook URL is valid and not expired

### Git tag not created
- Verify you have write permission to the repository
- Check GitHub Actions logs for permission errors

## Release History

| Version | Date | Changes |
|---------|------|---------|
| [1.0.0](https://github.com/igiclarisse10-max/devops_cat/releases/tag/v1.0.0) | 2025-12-08 | Initial release: CRUD API, comprehensive tests, CI/CD pipeline |

See [CHANGELOG.md](CHANGELOG.md) for detailed changes.

## Next Steps

1. **Configure GitHub Secrets** (optional):
   ```bash
   # Add Docker Hub credentials
   # Add Slack webhook URL
   ```

2. **Test the release workflow**:
   - Create a test release with version `1.0.1-rc1` (release candidate)
   - Verify Git tag, Docker image, and GitHub Release are created

3. **Update deployment scripts** to pull released Docker images:
   ```bash
   docker pull yourusername/todo-app:1.0.0
   ```

## See Also

- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
