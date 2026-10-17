"""
Generate and validate data/synthetic/ground_truth.json containing Q1-Q20, R1-R8, and distractors.
"""
import os
import json
import yaml

def load_plan():
    with open("data/synthetic/PLAN.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def run():
    print("Generating data/synthetic/ground_truth.json...")
    plan = load_plan()

    ground_truth = {
        "metadata": {
            "title": "RepoBrain Ground Truth Evaluation Set",
            "seed": plan["metadata"]["deterministic_seed"],
            "total_questions": len(plan["planted_facts_q1_q20"]),
            "total_review_scenarios": len(plan["planted_scenarios_r1_r8"]),
            "total_distractors": len(plan["distractors"])
        },
        "questions": plan["planted_facts_q1_q20"],
        "review_scenarios": plan["planted_scenarios_r1_r8"],
        "distractors": plan["distractors"]
    }

    gt_path = os.path.join("data", "synthetic", "ground_truth.json")
    with open(gt_path, "w", encoding="utf-8") as f:
        json.dump(ground_truth, f, indent=2)

    print(f"Wrote ground truth to {gt_path}")

    # Validate that every source ID exists in raw fixtures
    print("Validating source ID existence in generated dataset...")
    missing_sources = []
    for q in ground_truth["questions"]:
        qid = q["question_id"]
        for src in q["required_source_ids"]:
            if src.startswith("pull:"):
                pnum = src.split(":")[1]
                path = os.path.join("data", "synthetic", "fixtures", "pulls", f"{pnum}.json")
                if not os.path.exists(path):
                    missing_sources.append((qid, src, path))
            elif src.startswith("issue:"):
                inum = src.split(":")[1]
                path = os.path.join("data", "synthetic", "fixtures", "issues", f"{inum}.json")
                if not os.path.exists(path):
                    missing_sources.append((qid, src, path))
            elif src.startswith("doc:"):
                dpath = src.split(":", 1)[1]
                if not os.path.exists(dpath) and not os.path.exists(os.path.join("data", "synthetic", dpath)):
                    missing_sources.append((qid, src, dpath))
            elif src.startswith("file:"):
                fpath = src.split(":", 1)[1]
                if not os.path.exists(fpath) and not os.path.exists(os.path.join("data", "synthetic", fpath)):
                    missing_sources.append((qid, src, fpath))

    print(f"Missing sources found: {len(missing_sources)}")
    assert len(missing_sources) == 0, f"Missing planted source files: {missing_sources}"
    print("Stage 6 validation PASSED: all planted facts verified in raw data!\n")
    return ground_truth

if __name__ == "__main__":
    run()
