# projectdoctor/detectors/circular_import.py
import os
import ast
from collections import defaultdict

# Helper functions remain the same
def _get_module_name(file_path, project_path):
    rel_path = os.path.relpath(file_path, project_path).replace("\\", "/")
    if rel_path.startswith('../'): # Handle cases outside main project path
        return None
    module_path = os.path.splitext(rel_path)[0]
    return module_path.replace('/', '.')

def _resolve_import(module_name, current_module_path):
    if not module_name.startswith('.'): return module_name
    level = 0
    while module_name.startswith('.'):
        level += 1
        module_name = module_name[1:]
    parts = current_module_path.split('.')
    base = parts[:len(parts) - level]
    return '.'.join(base + ([module_name] if module_name else []))

class ImportVisitor(ast.NodeVisitor):
    def __init__(self, current_module_path):
        self.current_module_path = current_module_path
        self.imports = set()
    def visit_Import(self, node):
        for alias in node.names: self.imports.add(alias.name)
        self.generic_visit(node)
    def visit_ImportFrom(self, node):
        if node.module: self.imports.add(_resolve_import(node.module, self.current_module_path))
        self.generic_visit(node)

def _find_cycles(graph):
    path, visited, cycles, seen_cycles = [], set(), [], set()
    def dfs(node):
        path.append(node)
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in path:
                cycle = path[path.index(neighbor):] + [neighbor]
                sorted_tuple = tuple(sorted(cycle))
                if sorted_tuple not in seen_cycles:
                    cycles.append(cycle)
                    seen_cycles.add(sorted_tuple)
            elif neighbor not in visited: dfs(neighbor)
        path.pop()
    for node in list(graph.keys()):
        if node not in visited: dfs(node)
    return cycles

def analyze(project_path, thresholds, python_files):
    """
    ADVANCED DETECTOR: circular_import
    Purpose: Detects circular dependencies between modules.
    Improvement: This graph-based AST analysis is already the gold standard.
    """
    dependency_graph, module_map = defaultdict(set), {}
    for path in python_files:
        name = _get_module_name(path, project_path)
        if name: module_map[name] = path
    
    all_project_modules = set(module_map.keys())

    for module_name, file_path in module_map.items():
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                tree = ast.parse(f.read(), filename=file_path)
                visitor = ImportVisitor(module_name)
                visitor.visit(tree)
                for imp in visitor.imports:
                    if imp in all_project_modules: dependency_graph[module_name].add(imp)
        except Exception: continue
            
    cycles, issues = _find_cycles(dependency_graph), []
    for cycle in cycles:
        cycle_path = " -> ".join(cycle)
        issues.append({'file': module_map.get(cycle[0], cycle[0]), 'severity': 'HIGH', 'message': f"Circular import detected: {cycle_path}"})
    return issues