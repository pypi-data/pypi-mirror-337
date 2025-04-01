# Set the version bump type: major, minor, patch
BUMP = patch

# Declare phony targets
.PHONY: checks test badge bump-version release

# Check if we're on the main branch
checks:
	@git rev-parse --abbrev-ref HEAD | findstr /B /C:"main" > nul || ( \
		echo Error: You must be on the main branch to release. Current branch: "$(shell git rev-parse --abbrev-ref HEAD)" & \
		exit 1 \
	)

# Run tests with coverage
test:
	@echo "Running tests..."
	@pytest --cov=common_image_tools || (echo 'Tests failed' && exit 1)

# Generate coverage badge
badge:
	@echo "Generating coverage badge..."
	@coverage xml
	@genbadge coverage -i coverage.xml -o reports/coverage/coverage-badge.svg
	@git add reports/coverage/coverage-badge.svg

bump-version:
	@echo "Bumping version..."
	@poetry version $(BUMP)

# Release a new version
release: checks test badge bump-version
	$(eval VERSION := $(shell poetry version -s))
	@echo Building version: $(VERSION)
	@poetry build
	@git add pyproject.toml poetry.lock
	@git commit -m "Release version $(VERSION)"
	@git tag $(VERSION)
	@git push origin main --tags
