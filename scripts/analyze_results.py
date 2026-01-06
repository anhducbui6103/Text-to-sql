#!/usr/bin/env python3
"""
Analysis script for evaluation results
"""
import json
import sys
from pathlib import Path
from collections import defaultdict

import pandas as pd


def analyze_results(jsonl_path: str):
    """Analyze JSONL evaluation results"""
    p = Path(jsonl_path)
    if not p.exists():
        print(f"❌ File not found: {jsonl_path}")
        return
    
    # Load JSONL
    records = []
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    if not records:
        print("No records found")
        return
    
    df = pd.DataFrame(records)
    
    # Basic stats
    print("\n" + "=" * 70)
    print("📊 OVERALL STATISTICS")
    print("=" * 70)
    print(f"Total samples: {len(df)}")
    print(f"SELECT-only: {df['select_only'].sum()} ({df['select_only'].mean()*100:.2f}%)")
    print(f"Valid SQL: {df['sql_valid'].sum()} ({df['sql_valid'].mean()*100:.2f}%)")
    print(f"Exact Match (EM): {df['em_match'].sum()} ({df['em_match'].mean()*100:.2f}%)")
    print(f"Execution Accuracy (EX): {df['ex_match'].sum()} ({df['ex_match'].mean()*100:.2f}%)")
    
    avg_time = df['gen_time'].mean()
    print(f"Avg generation time: {avg_time:.3f}s")
    
    # Error analysis
    print("\n" + "=" * 70)
    print("❌ ERROR ANALYSIS")
    print("=" * 70)
    errors = df[df['pred_error'].notna()]
    if len(errors) > 0:
        print(f"Total errors: {len(errors)}")
        error_types = errors['pred_error'].value_counts().head(10)
        for err, count in error_types.items():
            print(f"  - {err}: {count}")
    
    # Per-database stats
    if 'db_id' in df.columns:
        print("\n" + "=" * 70)
        print("📈 PER-DATABASE STATISTICS")
        print("=" * 70)
        db_stats = df.groupby('db_id').agg({
            'ex_match': ['sum', 'count', 'mean'],
            'sql_valid': 'mean',
            'gen_time': 'mean'
        }).round(3)
        
        db_stats.columns = ['EX_count', 'total', 'EX_rate', 'valid_rate', 'avg_time']
        db_stats = db_stats.sort_values('EX_rate', ascending=False)
        
        print(db_stats.head(15))
    
    # Sample errors
    print("\n" + "=" * 70)
    print("🔍 SAMPLE FAILURES (First 5)")
    print("=" * 70)
    failures = df[df['ex_match'] == False].head(5)
    for idx, row in failures.iterrows():
        print(f"\nDB: {row['db_id']}")
        print(f"Q: {row['question'][:80]}...")
        print(f"Gold SQL: {row['gold_sql'][:60]}...")
        print(f"Pred SQL: {row['pred_sql'][:60]}...")
        if row['pred_error']:
            print(f"Error: {row['pred_error'][:60]}...")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_results.py <path_to_eval.jsonl>")
        sys.exit(1)
    
    analyze_results(sys.argv[1])
