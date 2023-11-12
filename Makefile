
# Create a Virtual Environment
venv:
	@echo "[*] Creating a Virtual Environment"
	@python3 -m venv venv


# Install Dependencies
install:
	@echo "[*] Installing Dependencies"
	@venv/bin/pip install -r requirements.txt

# Phony Targets
.PHONY: install