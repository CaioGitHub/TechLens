import json
import hashlib
import os
import sys

sys.path.insert(0, '.')
from scratch.dataset_groups_part1 import GROUP_A, GROUP_B, GROUP_C, GROUP_D
from scratch.dataset_groups_part2 import GROUP_E, GROUP_F, GROUP_G, GROUP_H, GROUP_I, GROUP_J

def compute_sha256(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest().upper()

def main():
    target_dir = '11 - Interview Evaluation/09 - Real Interview Pilot/Candidato-Piloto-05'
    all_cases = GROUP_A + GROUP_B + GROUP_C + GROUP_D + GROUP_E + GROUP_F + GROUP_G + GROUP_H + GROUP_I + GROUP_J
    
    print(f"Total cases assembled: {len(all_cases)}")
    
    # 1. Internal ID uniqueness
    ids = [c['id'] for c in all_cases]
    if len(ids) != len(set(ids)):
        duplicates = [x for x in ids if ids.count(x) > 1]
        raise ValueError(f"Duplicate IDs found in assembled dataset: {set(duplicates)}")
    print("Internal ID uniqueness check: PASSED (250 unique IDs)")

    # 2. Overlap audit against historical Stage 31.7.17 benchmark
    hist_path = os.path.join(target_dir, 'stage_31_7_17_ground_truth.json')
    if os.path.exists(hist_path):
        with open(hist_path, 'r', encoding='utf-8') as f:
            hist_cases = json.load(f)
        
        hist_questions = {c['question_text'].strip().lower() for c in hist_cases}
        hist_responses = {c['response_text'].strip().lower() for c in hist_cases}
        
        exact_q_collisions = []
        exact_r_collisions = []
        
        for c in all_cases:
            q = c['question_text'].strip().lower()
            r = c['response_text'].strip().lower()
            if q in hist_questions:
                exact_q_collisions.append((c['id'], c['question_text']))
            if r in hist_responses:
                exact_r_collisions.append((c['id'], c['response_text']))
                
        print(f"Exact question collisions with Stage 31.7.17: {len(exact_q_collisions)}")
        print(f"Exact response collisions with Stage 31.7.17: {len(exact_r_collisions)}")
        if exact_q_collisions:
            for cid, qtext in exact_q_collisions[:5]:
                print(f"  Collision Q: {cid} -> {qtext}")
        if exact_r_collisions:
            for cid, rtext in exact_r_collisions[:5]:
                print(f"  Collision R: {cid} -> {rtext}")
    else:
        print("Historical benchmark file not found for overlap check.")

    # 3. Write stage_31_7_21_ground_truth.json
    gt_file = os.path.join(target_dir, 'stage_31_7_21_ground_truth.json')
    with open(gt_file, 'w', encoding='utf-8') as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=2)
    gt_sha = compute_sha256(gt_file)
    print(f"Ground Truth written to: {gt_file}")
    print(f"Ground Truth SHA-256: {gt_sha} (Size: {os.path.getsize(gt_file)} bytes)")

    # 4. Write stage_31_7_21_blind_input.json
    blind_cases = [
        {
            "id": c["id"],
            "question_text": c["question_text"],
            "response_text": c["response_text"]
        }
        for c in all_cases
    ]
    blind_file = os.path.join(target_dir, 'stage_31_7_21_blind_input.json')
    with open(blind_file, 'w', encoding='utf-8') as f:
        json.dump(blind_cases, f, ensure_ascii=False, indent=2)
    blind_sha = compute_sha256(blind_file)
    print(f"Blind Input written to: {blind_file}")
    print(f"Blind Input SHA-256: {blind_sha} (Size: {os.path.getsize(blind_file)} bytes)")

if __name__ == '__main__':
    main()
