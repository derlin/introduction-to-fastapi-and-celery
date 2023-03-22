# FastAPI + Celery = ♥

*Interested in Python FastAPI? Wondering how to execute long-running tasks in the background
in Python? You came to the right place!*

This little website will go through the basics of Poetry, FastAPI and Celery, with some detours
here and there. I created it to back up my talk at GDG Fribourg on **March 22, 2023**.

Read on ⮕ ✨✨ https://derlin.github.io/introduction-to-fastapi-and-celery ✨✨

The full implementation of the use case can be found at: 
https://github.com/derlin/fastapi-notebook-runner.

**IMPORTANT** At the time of writing, the versions used are:

* poetry `1.3.0`
* FastAPI `0.95.0`
* Celery `5.2.7`

If you like it, please leave a :star:

---

To edit/run the website locally:

```bash
docker run --rm -it -p 8888:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```