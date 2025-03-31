# 🪄 bluer-ai

🪄 `bluer-ai` is an implementation of 🔻 [giza](https://github.com/kamangir/giza) and a language [to speak AI](https://github.com/kamangir/kamangir).

![image](https://github.com/kamangir/assets/blob/main/awesome-bash-cli/marquee-2024-10-26.jpg?raw=true)

# release install

not recommended.

```bash
pip install bluer_ai
```

# dev install

on macOS:

```bash
# change shell to bash
chsh -s /bin/bash

mkdir git
cd git
git clone git@github.com:kamangir/bluer-ai.git

nano ~/.bash_profile
# add "source $HOME/git/bluer-ai/bluer_ai/.abcli/bluer_ai.sh"
# restart the terminal

cd ~/Downloads
curl -o Miniconda3-latest-MacOSX-x86_64.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash ./Miniconda3-latest-MacOSX-x86_64.sh

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install awscli

aws configure

git config --global user.name kamangir
git config --global user.email arash@kamangir.net
```

on other environments:

- [Amazon EC2 instances](https://github.com/kamangir/awesome-bash-cli/wiki/ec2)
- [Amazon SageMaker](https://github.com/kamangir/awesome-bash-cli/wiki/SageMaker)
- [Jetson Nano](https://github.com/kamangir/awesome-bash-cli/wiki/Jetson-Nano)
- [Raspberry Pi](https://github.com/kamangir/awesome-bash-cli/wiki/Raspberry-Pi)

# configuration

create a copy of [`sample.env`](./bluer_ai/sample.env) as `.env` and fill in the secrets.

---

> 🪄 [`abcli`](https://github.com/kamangir/awesome-bash-cli) for the [Global South](https://github.com/kamangir/blue-south).

---


[![pylint](https://github.com/kamangir/bluer-ai/actions/workflows/pylint.yml/badge.svg)](https://github.com/kamangir/bluer-ai/actions/workflows/pylint.yml) [![pytest](https://github.com/kamangir/bluer-ai/actions/workflows/pytest.yml/badge.svg)](https://github.com/kamangir/bluer-ai/actions/workflows/pytest.yml) [![bashtest](https://github.com/kamangir/bluer-ai/actions/workflows/bashtest.yml/badge.svg)](https://github.com/kamangir/bluer-ai/actions/workflows/bashtest.yml) [![PyPI version](https://img.shields.io/pypi/v/bluer_ai.svg)](https://pypi.org/project/bluer_ai/) [![PyPI - Downloads](https://img.shields.io/pypi/dd/bluer_ai)](https://pypistats.org/packages/bluer_ai)

built by 🌀 [`bluer_options-5.5.1`](https://github.com/kamangir/awesome-bash-cli), based on 🪄 [`bluer_ai-12.3.1`](https://github.com/kamangir/bluer-ai).
