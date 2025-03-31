import ast
from pathlib import Path
from typing import List, Dict, Set


def index_local_modules(root: Path) -> Dict[str, Path]:
    mod_map = {}
    for file in root.rglob("*.py"):
        if "__pycache__" in file.parts:
            continue
        rel = file.relative_to(root).with_suffix("")
        modname = ".".join(rel.parts)
        mod_map[modname] = file.resolve()
    return mod_map


def extract_imports(path: Path) -> Set[str]:
    with open(path, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=str(path))
        except SyntaxError:
            return set()

    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    return imports


def resolve_local_dependencies(entry: Path, mod_map: Dict[str, Path]) -> Set[Path]:
    visited = set()
    to_visit = [entry.resolve()]
    result = set()

    while to_visit:
        path = to_visit.pop()
        if path in visited:
            continue
        visited.add(path)
        result.add(path)

        imports = extract_imports(path)
        for imp in imports:
            # Try to resolve the longest prefix match (for e.g. `foo.bar.baz`)
            while imp:
                if imp in mod_map:
                    imp_path = mod_map[imp]
                    to_visit.append(imp_path)
                    break
                else:
                    imp = ".".join(imp.split(".")[:-1])

    return result


def collect_module_data(project_root: Path, entry_point: Path) -> List[Dict]:
    mod_map = index_local_modules(project_root)
    used_files = resolve_local_dependencies(entry_point, mod_map)

    reverse_map = {v: k for k, v in mod_map.items()}

    result = []
    for path in sorted(used_files):
        module_name = reverse_map.get(path, path.stem)
        file_contents = path.read_text(encoding="utf-8")
        result.append(
            {
                "module_name": module_name,
                "file_name": str(path),
                "file_contents": file_contents,
            }
        )

    return result
