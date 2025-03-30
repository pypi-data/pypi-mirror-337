import ast
import csv
from io import StringIO
from types import FunctionType
from himena.plugins import register_function
from himena.types import Parametric, WidgetDataModel
from himena.standards.model_meta import TextMeta, FunctionMeta
from himena.consts import StandardType, MenuId


@register_function(
    types=StandardType.TEXT,
    menus=[MenuId.TOOLS_TEXT],
    keybindings="Ctrl+F5",
    command_id="builtins:run-script",
)
def run_script(model: WidgetDataModel[str]):
    """Run a Python script."""
    script = model.value
    if isinstance(model.metadata, TextMeta):
        if model.metadata.language.lower() == "python":
            exec(script)
        else:
            raise ValueError(f"Cannot run {model.metadata.language}.")
    else:
        raise ValueError("Unknown language.")
    return None


@register_function(
    types=StandardType.TEXT,
    menus=[MenuId.TOOLS_TEXT],
    command_id="builtins:text:change-separator",
)
def change_separator(model: WidgetDataModel[str]) -> Parametric:
    """Change the separator (in the sense of CSV or TSV) of a text."""

    def change_separator_data(old: str = ",", new: str = r"\t") -> WidgetDataModel[str]:
        if old == "" or new == "":
            raise ValueError("Old and new separators must not be empty.")
        # decode unicode escape. e.g., "\\t" -> "\t"
        old = old.encode().decode("unicode_escape")
        new = new.encode().decode("unicode_escape")
        buf = StringIO(model.value)
        reader = csv.reader(buf, delimiter=old)
        new_text = "\n".join(new.join(row) for row in reader)
        return WidgetDataModel(
            value=new_text,
            type=model.type,
            extensions=model.extensions,
            metadata=model.metadata,
        ).with_title_numbering()

    return change_separator_data


@register_function(
    types=StandardType.TEXT,
    menus=[MenuId.TOOLS_TEXT],
    command_id="builtins:text:change-encoding",
)
def change_encoding(model: WidgetDataModel[str]) -> Parametric:
    """Change the encoding of a text."""

    def change_encoding_data(encoding: str = "utf-8") -> WidgetDataModel[str]:
        new_text = model.value.encode(encoding).decode(encoding)
        out = model.with_value(new_text)
        if isinstance(meta := model.metadata, TextMeta):
            meta.encoding = encoding
        return out

    return change_encoding_data


@register_function(
    title="Compile as a function",
    types=StandardType.TEXT,
    menus=[MenuId.TOOLS_TEXT],
    command_id="builtins:compile-as-function",
)
def compile_as_function(model: WidgetDataModel[str]) -> WidgetDataModel:
    code = model.value
    mod = ast.parse(code)
    global_vars = {}
    local_vars = {}
    out = None
    nblock = len(mod.body)
    filename = "<QFunctionEdit>"
    if nblock == 0:
        raise ValueError("Code is empty.")
    last = mod.body[-1]
    if isinstance(last, ast.Expr):
        if len(mod.body) > 1:
            block_pre = ast.Module(body=mod.body[:-1], type_ignores=[])
            exec(compile(block_pre, filename, "exec"), global_vars, local_vars)
        if isinstance(last.value, ast.Name):
            out = local_vars[last.value.id]
        else:
            out = eval(compile(last.value, filename, "eval"), global_vars, local_vars)
    elif isinstance(last, ast.FunctionDef):
        exec(compile(mod, filename, "exec"), global_vars, local_vars)
        out = local_vars[last.name]
        assert isinstance(out, FunctionType)
        out.__globals__.update(local_vars)
    else:
        raise ValueError("Code must ends with an expression or a function definition.")

    if not callable(out):
        raise ValueError("Code does not define a callable object.")

    return WidgetDataModel(
        value=out,
        type=StandardType.FUNCTION,
        metadata=FunctionMeta(source_code=code),
    )
