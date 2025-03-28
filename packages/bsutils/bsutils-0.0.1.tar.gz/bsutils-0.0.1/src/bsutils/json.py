import pyjson5
from typing import Generator


def check_json_file_type(filename: str) -> str:
    ext = filename.split(".")[-1]
    if ext not in {"json", "jsonl"}:
        raise ValueError(f"Unknown file type .{ext}: {filename}")
    else:
        return ext


def iter_json_file(filename: str, ignore_exception: bool = True) -> Generator[dict, None, None]:
    def _iter_jsonl(f, ignore_exception: bool):
        for line in f:
            try:
                item = pyjson5.loads(line)
            except Exception as e:
                if ignore_exception:
                    print(f"Error: {e}\ncontent: {line}")
                else:
                    raise e
            else:
                yield item

    ext = check_json_file_type(filename)
    with open(filename, "r", encoding="utf8") as f:
        if ext == ".json":
            try:
                content = pyjson5.load(f)  # type: ignore
            except Exception:
                f.seek(0)
                _iter_jsonl(f, ignore_exception)
            else:
                if isinstance(content, list):
                    for item in content:
                        yield item
                elif not ignore_exception:
                    raise Exception  # TODO 修改为完善的错误类型
        else:  # .jsonl
            _iter_jsonl(f, ignore_exception)


def get_item_num(filename: str, ignore_exception: bool = True) -> int:
    def __jsonl_num(f, ignore_exception: bool):
        try:
            num = sum(1 for line in f)
        except Exception as e:
            if ignore_exception:
                print(f"File: {filename}\nError: {e}")
                num = 0
            else:
                raise e
        return num

    ext = check_json_file_type(filename)
    with open(filename) as f:
        if ext == ".json":
            try:
                dataset = pyjson5.load(f)  # type: ignore
            except Exception:
                num = __jsonl_num(f, ignore_exception)
            else:
                num = len(dataset)
        else:  # .jsonl
            num = __jsonl_num(f, ignore_exception)

    return num
