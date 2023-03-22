## Deploying to production

Now that we have everything, the last step is to make our app ready for production.

In 2023, wherever you deploy, production usually means one or more docker image,
and either a docker-compose, a Helm Chart or some other packaging.

I won't go into details here, but have a look at [fastapi-notebook-runner](
https://github.com/derlin/fastapi-notebook-runner) for an example of:

* a [Dockerfile](https://github.com/derlin/fastapi-notebook-runner/blob/main/Dockerfile)
* a [docker-compose](https://github.com/derlin/fastapi-notebook-runner/blob/main/docker-compose.yaml)
* a Helm Chart (Kubernetes).


The full app uses two Docker images even though it needs 3 processes:

1. the app Docker image, which can launch either celery or fastapi depending on the command argument, and
2. the official redis image.

Again, have a look at [fastapi-notebook-runner](https://github.com/derlin/fastapi-notebook-runner)
for more details.

## Tips

* [conventional commits](conventionalcommits.org/en/v1.0.0/)
* [black](https://github.com/psf/black), [ruff](https://github.com/charliermarsh/ruff)
  and [pytest](https://pytest.org)
* [GitHub Actions](https://docs.github.com/en/actions)
* [MkDocs Material](https://squidfunk.github.io/mkdocs-material)

## One more thing

I really enjoyed putting this site together. If you found it useful, please leave a :star:
on the [GitHub repo](https://github.com/derlin/introduction-to-fastapi-and-celery)!