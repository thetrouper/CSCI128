r"""
      /\        ╔═━─
     /  \       ║ C. Vicente
    /\   \      ╠══━─
   /      \     ║ Section A
  /   ,,   \    ║ Final Project
 /   |  |  -\   ║ "Labmda-1LP"
/_-''    ''-_\  ╚═══━─
"""

import os
import ast
import sys


roundabout_try = lambda primary, exceptional, exc_types: (
    lambda ns: (
        exec("try:\n    res = primary()\nexcept exc_types as err:\n    res = exceptional(err)", globals(), ns),
        ns.get('res')
    )[1]
)({'primary': primary, 'exceptional': exceptional, 'exc_types': tuple(exc_types)})

welcome = lambda: print("\n      ---[ Lambda 1LP ]---\ntype \"exit\" to quit at any stage\n\n")
main = lambda: (
    welcome(),
    -1 if (in_file := verify_infile()) is None
    else -1 if (out_file := verify_outfile()) is None
    else (collapse_file(in_file, out_file), in_file.close(), out_file.close(), 0)[-1]
)[-1]



attempt_comprehend = lambda file: (
    (tree:=ast.parse(file.read())),
    (forbidden:=(
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.ClassDef,
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.With,
        ast.AsyncWith,
        ast.Try,
        ast.TryStar,
        ast.Match
    )),
    (errors:=sum(1 for node in ast.walk(tree) if isinstance(node,forbidden) for _ in [print(f"Line {getattr(node, 'lineno', 'unknown')}: Illegal compound statement '{type(node).__name__}' found.")])),
    (errors==0)
)[-1]

comprehend_file = lambda file: roundabout_try(
    primary=lambda: attempt_comprehend(file),
    exceptional=lambda err: (print(f"Syntax error in target file: {err}"),False)[-1],
    exc_types=[SyntaxError]
)

verify_infile = lambda: (
    (filename:=input("Enter path to lambda-only python file: ").strip()),
    None if filename.lower() == "exit" else (
        roundabout_try(
            primary= lambda: open(filename,"r"),
            exceptional= lambda e: (print(f"Caught error opening {filename}: {e}."),None)[-1],
            exc_types=[IOError]
        )
        if os.path.exists(filename) and filename.lower().endswith(".py")
        else (print(f"Only valid python (.py) files are accepted. {filename} is not accepted. (Check Permissions?)"),None)[-1]
    )
    if not (
    (file:=roundabout_try(
        primary= lambda: open(filename,"r"),
        exceptional= lambda e: (print(f"Caught error opening {filename}: {e}."),None)[-1],
        exc_types=[IOError]
    )) is None or not comprehend_file(file)
    )
    else None
)[-1]

verify_outfile = lambda: ( (
    filename:=input("Enter path to output file: ").strip()
) , (
    None if filename.lower() == "exit" else (
        roundabout_try(
            primary=lambda: (
                (
                    None if (
                        os.path.exists(filename)
                        and os.path.getsize(filename) > 0
                        and (input(f"'{filename}' already contains data. Overwrite? [y/N]: ").strip().lower()) != "y"
                        and not print("Operation cancelled.")
                    ) else (
                        None if (
                            not os.path.exists(filename)
                            and (file_dir:=os.path.dirname(filename))
                            and not os.path.exists(file_dir)
                            and (input(f"Directory '{file_dir}' does not exist. Create it? [y/N]: ").strip().lower()) != "y"
                            and not print("Operation cancelled.")
                        ) else (
                            os.mkdirs(
                                (file_dir:=os.path.dirname(filename)),
                                exists_ok=True
                            ) or print(f"Created Directory '{file_dir}'.") or open(filename,"w") if (
                                not os.path.exists(filename)
                                and (file_dir:=os.path.dirname(filename))
                                and not os.path.exists(file_dir)
                            ) else open(filename,"w")
                        )
                    )
                )
            ),
            exceptional=lambda e: (
                print(f"Permission denied for '{filename}'.") or None
                if isinstance(e,PermissionError)
                else print(f"AN error occured while processing '{filename}': {e}") or None
            ),
            exc_types=[PermissionError,OSError,IOError]
        )
    )
))[-1]

unparse_stmt = lambda node: ast.unparse(node) if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr, ast.Delete, ast.Assert, ast.Raise, ast.Return, ast.Pass, ast.Break, ast.Continue, ast.Global, ast.Nonlocal, ast.Import, ast.ImportFrom, ast.TypeAlias)) else None

collapse_file = lambda in_file, out_file: (
    (
        in_file.seek(0)
    ),
    (
        module:=next(node for node in ast.walk(ast.parse(in_file.read())) if isinstance(node,ast.Module))
    ),
    (
        out_file.write(";".join([part for stmt in module.body if (part:=unparse_stmt(stmt)) is not None]))
    )
)


exec("""
if __name__ == '__main__':
    sys.exit(main())
""")

