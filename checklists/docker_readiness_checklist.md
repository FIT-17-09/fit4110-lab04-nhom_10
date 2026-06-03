# Docker Readiness Checklist

## Dockerfile

- [x] Uses a reasonable base image.
- [x] Defines `WORKDIR`.
- [x] Copies dependency files before source files to improve build cache usage.
- [x] Defines `EXPOSE`.
- [x] Defines `CMD` or `ENTRYPOINT`.
- [x] Defines `HEALTHCHECK`.
- [x] Runs with a non-root user.
- [x] Does not include real secrets.

## Runtime

- [x] Container starts successfully.
- [x] Port mapping is correct.
- [x] `/health` returns `200`.
- [x] Startup logs are clear.
- [x] Runtime configuration is provided through environment variables.

## Testing

- [x] Re-runs the Lab 03 Postman Collection.
- [x] Newman reports are generated in `reports/`.
- [x] Functional tests pass.
- [x] Auth tests pass on local/container.
- [x] Negative tests pass on local/container.
- [x] Boundary tests pass.

## Evidence

- [x] Docker build log is available.
- [x] Docker run log is available.
- [x] `curl /health` log is available.
- [x] Newman HTML/XML reports are available.
- [x] Image tag follows the lab convention.
