# Makefile for Zotero-MCP

.PHONY: publish-test publish

publish:
			@echo "Publishing..."
			rm -rf dist/
			uv build
			uvx twine upload \
				--password="$$(op read "op://Private/PyPi/API/token")" dist/*

publish-test:
					@echo "Publishing..."
					rm -rf dist/
					uv build
					uvx twine upload \
						--repository=testpypi \
						--password="$$(op read "op://Private/Test PyPi/API/token")" dist/*
