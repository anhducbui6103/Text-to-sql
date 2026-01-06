#!/usr/bin/env python3
"""
Batch evaluation script for ViText2SQL dataset
Usage:
  python scripts/eval_vitext2sql.py --db-dir /path/to/spider/database --split test --limit 100
"""
import argparse
import json
import sys
from pathlib import Path
from dataclasses import asdict

from dotenv import load_dotenv
from tqdm import tqdm

# Add backend to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from eval.eval import ViTextEvaluator, load_vitext2sql_split


def main():
    p = argparse.ArgumentParser(description="Evaluate ViText2SQL with Gemini")
    p.add_argument("--tables-json", default="tables.json",
                   help="Path to tables.json from Spider (default: ./tables.json)")
    p.add_argument("--split", default="test", 
                   help="Dataset split: train/validation/test")
    p.add_argument("--limit", type=int, default=None,
                   help="Max samples to evaluate (default: all)")
    p.add_argument("--out", default="backend/eval/outputs/vitext2sql_eval.jsonl",
                   help="Output JSONL file path")
    p.add_argument("--model", default=None,
                   help="Gemini model name (auto-select if not specified)")
    args = p.parse_args()
    
    # Load environment
    load_dotenv()
    load_dotenv(Path(__file__).parent.parent / "backend" / ".env")
    
    # Create evaluator
    tables_json = Path(args.tables_json).resolve()
    print(f"📋 Tables schema: {tables_json}")
    print(f"🤖 Gemini model: {args.model or 'auto-select'}")
    print(f"📊 Split: {args.split}, Limit: {args.limit or 'all'}")
    print()
    
    try:
        evaluator = ViTextEvaluator(tables_json, model_name=args.model)
        print(f"✅ Using model: {evaluator.generator.model_name}\n")
    except Exception as e:
        print(f"❌ Failed to initialize evaluator: {e}")
        return 1
    
    # Load dataset
    print(f"📥 Loading ViText2SQL {args.split} split...")
    try:
        samples = load_vitext2sql_split(split=args.split, limit=args.limit)
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")
        return 1
    
    print(f"📊 Loaded {len(samples)} samples\n")
    
    # Run evaluation
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    stats = {
        "total": 0,
        "select_only": 0,
        "sql_valid": 0,
        "em_match": 0,
        "ex_match": 0,
        "errors": 0,
        "gen_time_total": 0.0,
        "samples": []
    }
    
    print(f"🔄 Running evaluation...\n")
    
    with out_path.open("w", encoding="utf-8") as f:
        for sample in tqdm(samples, desc="Evaluating"):
            db_id = sample["db_id"]
            question = sample["question"]
            gold_sql = sample["gold_sql"]
            
            if not all([db_id, question, gold_sql]):
                continue
            
            result = evaluator.eval_single(db_id, question, gold_sql)
            result_dict = asdict(result)
            
            # Update stats
            stats["total"] += 1
            if result.select_only:
                stats["select_only"] += 1
            if result.sql_valid:
                stats["sql_valid"] += 1
            if result.em_match:
                stats["em_match"] += 1
            if result.ex_match:
                stats["ex_match"] += 1
            if result.pred_error:
                stats["errors"] += 1
            
            stats["gen_time_total"] += result.gen_time
            
            # Write to JSONL
            f.write(json.dumps(result_dict, ensure_ascii=False) + "\n")
    
    # Print summary
    def pct(x):
        return 0.0 if stats["total"] == 0 else (100.0 * x / stats["total"])
    
    print("\n" + "=" * 60)
    print("📊 EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total samples: {stats['total']}")
    print(f"SELECT-only rate: {stats['select_only']}/{stats['total']} = {pct(stats['select_only']):.2f}%")
    print(f"Valid SQL rate: {stats['sql_valid']}/{stats['total']} = {pct(stats['sql_valid']):.2f}%")
    print(f"Exact Match (EM): {stats['em_match']}/{stats['total']} = {pct(stats['em_match']):.2f}%")
    print(f"Execution Accuracy (EX): {stats['ex_match']}/{stats['total']} = {pct(stats['ex_match']):.2f}%")
    print(f"Error rate: {stats['errors']}/{stats['total']} = {pct(stats['errors']):.2f}%")
    if stats["total"] > 0:
        print(f"Avg generation time: {stats['gen_time_total'] / stats['total']:.3f}s")
    print("=" * 60)
    print(f"✅ Output: {out_path}\n")
    
    # Save summary as JSON
    summary_path = out_path.parent / f"{out_path.stem}_summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump({
            "split": args.split,
            "limit": args.limit,
            "model": evaluator.generator.model_name,
            "tables_json": str(tables_json),
            "stats": {k: v for k, v in stats.items() if k != "samples"}
        }, f, indent=2, ensure_ascii=False)
    print(f"📋 Summary: {summary_path}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
