[private]
default:
	@just --list --unsorted --list-heading '' --list-prefix ''

# solve the puzzle in the current directory
[no-cd]
solve:
	@python solve.py

# add new day
[no-cd]
new:
	touch solve.py
	touch input.txt
	touch example.txt

# benchmark the solution with hyperfine
[no-cd]
benchmark:
	hyperfine "python solve.py"

# lint and format
[private]
lf: lint format

# lint with ruff
[no-cd]
lint:
	@ruff check --fix

# format with ruff
[no-cd]
format:
	@ruff format
