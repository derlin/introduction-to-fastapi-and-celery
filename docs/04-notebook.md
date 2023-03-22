The last piece of the puzzle is to design a task that can execute a Jupyter Notebook.


## A simple notebook

The most basic notebook of all would look like this:
```json
--8<-- "notebook.ipynb"
```

It doesn't require any specific dependencies to run except, of course, Jupyter.

## The fast and ugly way

Since the notebook is not meant to change once the app is started,
an easy (but ugly) way is to convert it to a simple Python script (e.g. in CI),
and run it using `execfile`.

To convert a Jupyter Notebook provided `notebook` (or juypter lab) is installed
is as easy as calling `nbconvert`:
```bash
jupyter nbconvert --to python notebook.ipynb
```

Then, the task would look like this:
```python
@app.task("execute_notebook")
def execute_notebook():
    execfile('notebook.py')
```

But we could do better, right?

## Using NbConvert API

If developers use Jupyter Notebook for developing, chances are all the dependencies
are already in the Poetry file. But if we only want to convert a simple notebook,
the only thing we need is `nbconvert` and Python's IpyKernel support:

```bash
poetry add nbconvert ipykernel
```

Now that we have this, we can read the notebook directly from the task and execute it:

```python
import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

processor = ExecutePreprocessor(timeout=600, kernel_name="python")

# read the notebook once, as it will never change
with open(os.environ.get("SCRIPT_PATH", "notebook.ipynb")) as f:
    notebook = nbformat.read(f, as_version=4)


def execute_notebook() -> str:
    processor.preprocess(notebook)
    # the following will raise an CellExecutionError in case of error
    return nbformat.writes(notebook)
```

To convert this into a Celery task, just add the annotation and you are good to go!

Why is it better you ask?
Well, for one thing, we can now have access to nbconvert's output,
including the stacktrace if something goes wrong! Furthermore, any error will raise an
exception of type `CellExecutionError` that will automatically mark Celery's task as a failure.

We could even imagine storing the notebook's output itself in the result in case of success.
But beware! Depending on the verbosity of the notebook, it may burden the results backend. Up to you! 