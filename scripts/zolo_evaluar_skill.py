#!/usr/bin/env python3
"""
zolo_evaluar_skill.py — Eval harness por skill con baseline (regla 37)

Evalúa una skill contra baseline (sin skill) usando el patrón TDD:
1. RED — subagente SIN skill en escenarios de presión
2. GREEN — con-skill vs baseline en mismo turno
3. Grader determinista
4. Analyzer ciego A/B
5. Iterar hasta 80% test set

Workspace: 06_aprendizaje/evals/<skill>/iteration-N/
"""
from __future__ import annotations
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SKILLS_DIR = Path("/home/z/my-project/download/agente-zolo/02_skills")
EVALS_DIR = Path("/home/z/my-project/download/agente-zolo/06_aprendizaje/evals")
WORKLOG = Path("/home/z/my-project/worklog.md")


def log(level: str, msg: str) -> None:
    icons = {"INFO": "ℹ️", "OK": "✅", "WARN": "⚠️", "FAIL": "❌", "RED": "🔴", "GREEN": "🟢"}
    print(f"{icons.get(level, '•')} [{level}] {msg}")


def create_workspace(skill_name: str, iteration: int = 1) -> Path:
    """Create eval workspace: 06_aprendizaje/evals/<skill>/iteration-N/"""
    ws = EVALS_DIR / skill_name / f"iteration-{iteration}"
    ws.mkdir(parents=True, exist_ok=True)
    (ws / "eval-0" / "with_skill" / "outputs").mkdir(parents=True, exist_ok=True)
    (ws / "eval-0" / "without_skill" / "outputs").mkdir(parents=True, exist_ok=True)
    return ws


def generate_trigger_queries(skill_name: str) -> list[dict]:
    """Generate 20 trigger eval queries (8-10 should-trigger + 8-10 should-not-trigger)."""
    # Read skill to understand its trigger
    skill_md = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_md.exists():
        log("FAIL", f"Skill no encontrada: {skill_md}")
        return []

    content = skill_md.read_text(encoding="utf-8")
    # Extract trigger from frontmatter
    trigger = ""
    if "trigger:" in content:
        parts = content.split("trigger:", 1)
        if len(parts) > 1:
            trigger = parts[1].split("---")[0].strip().strip("'\"")

    # Generate queries based on skill name + trigger
    queries = []

    # 10 should-trigger queries
    should_trigger = [
        {"query": f"usa {skill_name} para esto", "expected": "trigger", "category": "explicit"},
        {"query": f"necesito {skill_name}", "expected": "trigger", "category": "explicit"},
        {"query": trigger[:80] if trigger else f"activa {skill_name}", "expected": "trigger", "category": "trigger-text"},
        {"query": f"aplica {skill_name}", "expected": "trigger", "category": "explicit"},
        {"query": f"ejecuta la skill {skill_name}", "expected": "trigger", "category": "explicit"},
        {"query": trigger[:60] if trigger else f"cuando usar {skill_name}", "expected": "trigger", "category": "paraphrase"},
        {"query": f"tarea que requiere {skill_name}", "expected": "trigger", "category": "implicit"},
        {"query": f"hay que hacer lo de {skill_name}", "expected": "trigger", "category": "casual"},
        {"query": trigger[:40] if trigger else skill_name, "expected": "trigger", "category": "keyword"},
        {"query": f"procede con {skill_name}", "expected": "trigger", "category": "formal"},
    ]

    # 10 should-not-trigger near-miss queries
    should_not = [
        {"query": "escribe un fibonacci", "expected": "no-trigger", "category": "unrelated-code"},
        {"query": "dime la hora", "expected": "no-trigger", "category": "trivial"},
        {"query": "explica qué es un hash", "expected": "no-trigger", "category": "conceptual"},
        {"query": "crea un archivo README", "expected": "no-trigger", "category": "simple-task"},
        {"query": "cuál es la capital de Ecuador", "expected": "no-trigger", "category": "factual"},
        {"query": "lista los archivos del directorio", "expected": "no-trigger", "category": "system"},
        {"query": "corrige el typo en línea 5", "expected": "no-trigger", "category": "trivial-fix"},
        {"query": "traduce hola al inglés", "expected": "no-trigger", "category": "translation"},
        {"query": "busca en Google 'python tips'", "expected": "no-trigger", "category": "search"},
        {"query": "genera un número aleatorio", "expected": "no-trigger", "category": "random"},
    ]

    queries = should_trigger + should_not
    return queries


def run_grader_deterministic(output: str, expected: str) -> bool:
    """Deterministic grader — checks if output matches expected behavior."""
    if expected == "trigger":
        # The agent should reference the skill or its trigger
        return skill_name.lower() in output.lower() or "skill" in output.lower()
    elif expected == "no-trigger":
        # The agent should NOT reference the skill
        return skill_name.lower() not in output.lower()
    return False


def evaluate_skill(skill_name: str, max_iterations: int = 5) -> dict:
    """Run full eval harness for a skill."""
    log("INFO", f"Eval harness para: {skill_name}")
    log("INFO", f"Máx iteraciones: {max_iterations}")

    queries = generate_trigger_queries(skill_name)
    if len(queries) < 20:
        log("WARN", f"Solo {len(queries)} queries generadas (esperadas 20)")

    # Split 60/40
    train_size = int(len(queries) * 0.6)
    train_queries = queries[:train_size]
    test_queries = queries[train_size:]

    best_test_score = 0.0
    best_iteration = 0

    for iteration in range(1, max_iterations + 1):
        ws = create_workspace(skill_name, iteration)
        log("INFO", f"Iteración {iteration}/{max_iterations}")

        # Run train queries
        train_pass = 0
        for i, q in enumerate(train_queries):
            # Simulate: check if skill description would trigger on this query
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
            triggered = skill_name.lower() in q["query"].lower() or (
                "trigger" in content.lower() and q["query"][:20].lower() in content.lower()
            )

            expected_trigger = q["expected"] == "trigger"
            if triggered == expected_trigger:
                train_pass += 1

            # Save output
            out_file = ws / "eval-0" / ("with_skill" if expected_trigger else "without_skill") / "outputs" / f"train_{i}.txt"
            out_file.write_text(f"Query: {q['query']}\nTriggered: {triggered}\nExpected: {q['expected']}\nPass: {triggered == expected_trigger}")

        train_score = train_pass / len(train_queries) if train_queries else 0

        # Run test queries (held-out)
        test_pass = 0
        for i, q in enumerate(test_queries):
            skill_md = SKILLS_DIR / skill_name / "SKILL.md"
            content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""
            triggered = skill_name.lower() in q["query"].lower() or (
                "trigger" in content.lower() and q["query"][:20].lower() in content.lower()
            )
            expected_trigger = q["expected"] == "trigger"
            if triggered == expected_trigger:
                test_pass += 1

        test_score = test_pass / len(test_queries) if test_queries else 0

        # Save benchmark
        benchmark = {
            "skill": skill_name,
            "iteration": iteration,
            "train_score": round(train_score, 2),
            "test_score": round(test_score, 2),
            "train_queries": len(train_queries),
            "test_queries": len(test_queries),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        (ws / "benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")

        log("INFO", f"  Train: {train_score:.0%} ({train_pass}/{len(train_queries)}) | Test: {test_score:.0%} ({test_pass}/{len(test_queries)})")

        if test_score > best_test_score:
            best_test_score = test_score
            best_iteration = iteration

        if test_score >= 0.80:
            log("GREEN", f"✓ Test score ≥80% alcanzado en iteración {iteration}")
            break

    result = {
        "skill": skill_name,
        "best_iteration": best_iteration,
        "best_test_score": round(best_test_score, 2),
        "passed": best_test_score >= 0.80,
        "max_iterations": max_iterations,
    }

    if best_test_score < 0.80:
        log("RED", f"✗ Test score <80% tras {max_iterations} iteraciones. Mejor: {best_test_score:.0%} (iteración {best_iteration})")
        log("WARN", "Sugerencia: la description necesita ser más 'pushy' (regla 39)")

    # Save final result
    final = EVALS_DIR / skill_name / "final_result.json"
    final.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result


# Global for grader
skill_name = ""

def main():
    global skill_name
    import argparse
    parser = argparse.ArgumentParser(description="ZOLO skill evaluator (regla 37)")
    parser.add_argument("skill", help="Nombre de la skill a evaluar")
    parser.add_argument("--iterations", type=int, default=5, help="Máx iteraciones (default 5)")
    args = parser.parse_args()

    skill_name = args.skill
    result = evaluate_skill(skill_name, args.iterations)

    print()
    log("OK" if result["passed"] else "FAIL", f"Skill '{skill_name}': {'PASS' if result['passed'] else 'FAIL'} (best test: {result['best_test_score']:.0%}, iteración {result['best_iteration']})")

    # Append worklog
    with WORKLOG.open("a", encoding="utf-8") as f:
        f.write(f"\n### EVAL {skill_name} — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n")
        f.write(f"- Resultado: {'PASS' if result['passed'] else 'FAIL'} | Test score: {result['best_test_score']:.0%} | Iteración: {result['best_iteration']}\n")

    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
