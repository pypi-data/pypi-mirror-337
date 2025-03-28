import contextlib
import dataclasses
import functools
import io
import os
import pathlib

import duckdb
import h5py
import numpy
import typing_extensions

from ensembl_tui import _util as eti_util

ReturnType = tuple[str, tuple]  # the sql statement and corresponding values


@functools.singledispatch
def array_to_blob(data: numpy.ndarray) -> bytes:
    with io.BytesIO() as out:
        numpy.save(out, data)
        out.seek(0)
        return out.read()


@array_to_blob.register
def _(data: bytes) -> bytes:
    # already a blob
    return data


@functools.singledispatch
def blob_to_array(data: bytes) -> numpy.ndarray:
    with io.BytesIO(data) as out:
        out.seek(0)
        return numpy.load(out)


@blob_to_array.register
def _(data: numpy.ndarray) -> numpy.ndarray:
    return data


# HDF5 base class
@dataclasses.dataclass
class Hdf5Mixin(eti_util.SerialisableMixin):
    """HDF5 sequence data storage"""

    _file: h5py.File | None = None
    _is_open: bool = False
    mode: str = "r"

    def __getstate__(self) -> dict:
        if set(self.mode) & {"w", "a"}:
            raise NotImplementedError(f"pickling not supported for mode={self.mode!r}")
        return self._init_vals.copy()  # type: ignore

    def __setstate__(self, state: dict) -> None:
        obj = self.__class__(**state)
        self.__dict__.update(obj.__dict__)
        # because we have a __del__ method, and self attributes point to
        # attributes on obj, we need to modify obj state so that garbage
        # collection does not screw up self
        obj._is_open = False
        obj._file = None

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        """closes the hdf5 file"""
        # during garbage collection at shutdown, the open function is
        # not available
        try:
            open  # noqa: B018
        except NameError:
            return

        # hdf5 dumps content to stdout if resource already closed, so
        # we trap that here, and capture expected exceptions raised in the process
        with (
            open(os.devnull, "w") as devnull,
            contextlib.redirect_stderr(devnull),
            contextlib.redirect_stdout(devnull),
        ):
            with contextlib.suppress(ValueError, AttributeError):
                if self._is_open and self._file:
                    self._file.flush()

            with contextlib.suppress(AttributeError):
                if self._file:
                    self._file.close()

        self._is_open = False


class ViewMixin:
    _source: pathlib.Path  # override in subclass

    @property
    def species(self) -> str:
        return self._source.name


@dataclasses.dataclass(slots=True)
class DuckdbParquetBase:
    source: dataclasses.InitVar[pathlib.Path]
    # db is for testing purposes
    db: dataclasses.InitVar[duckdb.DuckDBPyConnection | None] = None
    _source: pathlib.Path = dataclasses.field(init=False)
    _conn: duckdb.DuckDBPyConnection = dataclasses.field(init=False, default=None)  # type: ignore
    _tables: tuple[str, ...] | tuple = ()

    def __post_init__(
        self,
        source: pathlib.Path,
        db: duckdb.DuckDBPyConnection | None,
    ) -> None:
        source = pathlib.Path(source)
        self._source = source
        if db:
            self._conn = db
            return

        self._conn = None

        if not source.exists():
            msg = f"{self._source} does not exist"
            raise FileNotFoundError(msg)
        if not source.is_dir():
            msg = f"{self._source} is not a directory"
            raise OSError(msg)

        if hasattr(self, "_post_init"):
            self._post_init()

    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        if self._conn is None:
            self._conn = duckdb.connect(":memory:")
            for table in self._tables:
                parquet_file = self._source / f"{table}.parquet"
                if not parquet_file.exists():
                    msg = f"{parquet_file} does not exist"
                    raise FileNotFoundError(msg)

                sql = f"CREATE TABLE {table} AS SELECT * FROM read_parquet('{parquet_file}')"
                self._conn.sql(sql)

        return self._conn

    def __len__(self) -> int:
        return self.num_records()

    def __eq__(self, other: typing_extensions.Self) -> bool:
        return other.conn is self.conn

    @property
    def source(self) -> pathlib.Path:
        return self._source

    def close(self) -> None:
        self.conn.close()

    def num_records(self) -> int:  # pragma: no cover
        # override in subclass
        raise NotImplementedError
