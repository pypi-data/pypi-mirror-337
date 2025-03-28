# BigModel Hub CLI

BigModel Hub CLI Toolkit

**Usage**:

```console
$ bmhub [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `list`: List downloaded models.
* `download`: Download a model from the model hub.
* `update`: Update downloaded models.
* `remove`: Remove downloaded models.

## `bmhub list`

List downloaded models.

**Usage**:

```console
$ bmhub list [OPTIONS] BACKEND:{hf|ms}
```

**Arguments**:

* `BACKEND:{hf|ms}`: Model hub backend  [required]

**Options**:

* `-p, --pattern TEXT`: Glob pattern to match model IDs
* `--local-dir DIRECTORY`: The local model directory
* `--help`: Show this message and exit.

## `bmhub download`

Download a model from the model hub.

**Usage**:

```console
$ bmhub download [OPTIONS] BACKEND:{hf|ms} MODEL_ID
```

**Arguments**:

* `BACKEND:{hf|ms}`: Model hub backend  [required]
* `MODEL_ID`: Model ID  [required]

**Options**:

* `--local-dir DIRECTORY`: The local model directory
* `--help`: Show this message and exit.

## `bmhub update`

Update downloaded models.

**Usage**:

```console
$ bmhub update [OPTIONS] BACKEND:{hf|ms}
```

**Arguments**:

* `BACKEND:{hf|ms}`: Model hub backend  [required]

**Options**:

* `-p, --pattern TEXT`: Glob pattern to match model IDs
* `--local-dir DIRECTORY`: The local model directory
* `--help`: Show this message and exit.

## `bmhub remove`

Remove downloaded models.

**Usage**:

```console
$ bmhub remove [OPTIONS] BACKEND:{hf|ms}
```

**Arguments**:

* `BACKEND:{hf|ms}`: Model hub backend  [required]

**Options**:

* `-p, --pattern TEXT`: Glob pattern to match model IDs
* `--local-dir DIRECTORY`: The local model directory
* `--help`: Show this message and exit.
