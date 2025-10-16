# promisces.hhra

Human Health Risk Assessment (HHRA) for Project PROMISCES

## Installation

### dependencies

create a venv

```bash
python -m venv venv
```

source it (Mac/Linux)

```bash
source venv/bin/activate
```
or on windows

```bash
source venv/Scripts/activate
```

then, install the requirements with 

```bash
pip install -r requirements.txt
```

if you intend to work with the notebooks, you need to install `jupyter` too with
```bash
pip install jupyter
```

### literature data

for `promisces` to work correctly, you'll need to put all the `.csv` of the literature data in a directory named `data/` at the top-level of the project's directory.
Then, `promisces/` should look like this:
```bash
promisces/
  data/
    matrix_unique.csv
    process_removal_lit.csv
    reference_lit.csv
    starting_concentration.csv
    substance_unique.csv
    treatment_unique.csv
  promisces/
    models/
      ...
    simulate_removals.py
    ...
  demo.ipynb
  ...
```

> Note: the required data is not part of the git repository and must be requested by {{{?}}}  

## Usage

