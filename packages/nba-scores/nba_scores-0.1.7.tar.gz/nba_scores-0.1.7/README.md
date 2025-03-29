# NBA

NBA is a simple Python package that provides you with a quick and easy
command-line interface to current NBA scores and standings.

See the [Installation](#installation) & [Usage](#usage) sections below
for more information.

# Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

[Back to top](#table-of-contents)

## PyPi

```shell
pipx install nba-scores
```

## Manual

To run the script locally, run the following commands:

```shell
git clone https://github.com/ccleberg/nba
cd nba
pipx install .
```

![Installation](https://github.com/ccleberg/nba/blob/main/screenshots/installation.png?raw=true)

# Usage

[Back to top](#table-of-contents)

All commands can be passed to the program with the following template:
`nba <ARGUMENT>`

| Argument      | Shortcut | Description                       |
|---------------|----------|-----------------------------------|
| `--scores`    | `-sc`    | Show today's scoreboard           |
| `--standings` | `-st`    | Show current conference standings |

Scores:
![Scores](https://github.com/ccleberg/nba/blob/main/screenshots/scores.png?raw=true)

Standings:
![Standings](https://github.com/ccleberg/nba/blob/main/screenshots/standings.png?raw=true)

# Contributing

[Back to top](#table-of-contents)

Any and all contributions are welcome. Feel free to fork the project,
add features, and submit a pull request.
