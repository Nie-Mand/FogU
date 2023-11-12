
# Create a Virtual Environment
venv:
	@echo "[*] Creating a Virtual Environment"
	@python3 -m venv venv


# Install Dependencies
install:
	@echo "[*] Installing Dependencies"
	@venv/bin/pip install -r requirements.txt

# Run the simulation
run:
	@echo "[*] Running the Simulation"
	@venv/bin/python3 main.py

# Phony Targets
.PHONY: install run