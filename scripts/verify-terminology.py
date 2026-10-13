#!/usr/bin/env python3
"""
Custom verification script to ensure 100% terminology compliance and zero regressions.
Runs inside Docker container (python:3.12-slim).
"""

import os
import re
import sys
from pathlib import Path

def find_sc_knowledge_dir() -> Path:
    candidates = [
        Path("/sc-knowledge"),
        Path("/home/cosmo_chang/Projects/star-citizen-knowledge-mcp"),
    ]
    for c in candidates:
        if (c / "glossaries").exists() and (c / "mcp_servers" / "shared" / "resolver.py").exists():
            return c
    raise FileNotFoundError(f"Could not locate star-citizen-knowledge-mcp in {candidates}")

def test_term_resolver(sc_dir: Path):
    print(f"--- 1. Testing TermResolver integration from {sc_dir} ---")
    sys.path.insert(0, str(sc_dir))
    from mcp_servers.shared.resolver import TermResolver
    
    resolver = TermResolver(str(sc_dir / "glossaries"))
    
    test_cases = [
        ("Drake Interplanetary", "德雷克星際"),
        ("Roberts Space Industries", "羅伯茲太空工業"),
        ("Stanton", "斯坦頓"),
        ("Klescher Rehabilitation Facility", "克萊舍爾勞教所"),
        ("Vulture", "禿鷲"),
        ("Aaron Halo", "亞倫環"),
        ("United Wayfarers Club", "旅者聯合俱樂部"),
        ("Covalex Shipping", "科瓦萊什貨運"),
        ("Coramor", "科拉情人節"),
        ("Standard Control Mode", "SCM 戰鬥操控模式"),
        ("Navigation Mode", "NAV 巡航導航模式"),
    ]
    
    all_passed = True
    for en, expected_zh in test_cases:
        actual_zh = resolver.resolve_to_zh(en)
        if actual_zh != expected_zh:
            print(f"  [FAIL] {en} -> {actual_zh} (expected: {expected_zh})")
            all_passed = False
        else:
            print(f"  ✓ {en} -> {actual_zh}")
            
    if not all_passed:
        raise ValueError("TermResolver resolution validation failed.")
    print("✓ TermResolver loaded and passed all benchmark resolution checks.\n")

def test_markdown_compliance(repo_root: Path):
    print("--- 2. Validating Repository Markdown Files ---")
    md_files = [p for p in repo_root.glob("**/*.md") if ".git" not in p.parts]
    print(f"Found {len(md_files)} Markdown files.")
    
    errors = []
    total_hints = 0
    
    deprecated_rules = [
        ("德拉克工業", r"德拉克工業", "德雷克星際"),
        ("毀滅空間站", r"毀滅空間站", "廢墟太空站"),
        ("星辰建築師", r"星際?建築師", "星際建築系統"),
        ("阿隆光環", r"阿隆光環", "亞倫環"),
        ("克萊雪", r"克萊雪", "克萊舍爾"),
        ("史丹頓", r"史丹頓", "斯坦頓"),
        ("德拉克(非德拉克沃斯)", r"德拉克(?![沃斯])", "德雷克星際"),
        ("基礎節 (Foundation Festival)", r"基礎節\s*\(Foundation Festival\)", "奠基節"),
        ("寇拉莫 (Coramor)", r"寇拉莫\s*\(Coramor\)", "科拉情人節"),
        ("生命維持系統", r"生命維持系統", "維生系統"),
        ("醫療生物凝膠", r"醫療生物凝膠", "醫療凝膠"),
        ("互安防務", r"互安防務", "互安防衛"),
        ("北岩服務集團", r"北境?岩服務集團", "北境之巖服務團隊"),
        ("埃克哈特保安", r"埃克哈特保安", "埃克哈特保全"),
        ("科瓦萊什物流", r"科瓦萊什物流", "科瓦萊什貨運"),
        ("QV 拆解站", r"QV\s*拆解站", "QV 碎岩站"),
        ("SCM (戰鬥機動)", r"SCM\s*\(戰鬥機動\)", "SCM (戰鬥操控模式)"),
        ("NAV (極速導航)", r"NAV\s*\(極速導航\)", "NAV (巡航導航模式)"),
    ]
    
    for p in sorted(md_files):
        rel = p.relative_to(repo_root)
        content = p.read_text(encoding="utf-8")
        
        # Check hint tag balance
        hint_count = content.count("{% hint")
        endhint_count = content.count("{% endhint %}")
        total_hints += hint_count
        if hint_count != endhint_count:
            errors.append(f"Unbalanced hints in {rel}: {hint_count} {{% hint %}} vs {endhint_count} {{% endhint %}}")
            
        # Check for lingering alert blockquotes
        for idx, line in enumerate(content.splitlines()):
            if re.search(r"^\s*>\s*\\?\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]", line, re.IGNORECASE):
                errors.append(f"Legacy alert blockquote in {rel}:{idx+1}: {line.strip()}")
                
        # Check for deprecated terms outside HTML comments
        clean_content = re.sub(r"<!--[\s\S]*?-->", "", content)
        for term_name, pat, replacement in deprecated_rules:
            matches = re.findall(pat, clean_content)
            if matches:
                errors.append(f"Deprecated term '{term_name}' found in {rel}: replace with '{replacement}'")

    print(f"✓ Total GitBook hint blocks verified: {total_hints}")
    
    if errors:
        print(f"\n[ERROR] Found {len(errors)} issues:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
        
    print("✓ 0 syntax errors, 0 deprecated terms, 100% compliant with sc-knowledge.")

def test_mirror_consistency(repo_root: Path):
    print("\n--- 3. Checking Mirroring Consistency between Root and docs/ ---")
    mappings = [
        ("introduction", "docs/gai-lan-yu-xin-shou-qi-bu/introduction"),
        ("getting-started", "docs/gai-lan-yu-xin-shou-qi-bu/getting-started"),
        ("first-steps", "docs/he-xin-cao-zuo-yu-sheng-cun-fa-ze/first-steps"),
        ("survival-guide", "docs/he-xin-cao-zuo-yu-sheng-cun-fa-ze/survival-guide"),
        ("professions", "docs/yu-zhou-zhi-ye-yu-jing-ji-ti-xi/professions"),
        ("special-events", "docs/te-shu-huo-dong-zhi-nan/special-events"),
        ("future", "docs/wei-lai-yuan-jing-yu-xing-chen-yin-qing/future"),
        ("appendix", "docs/fu-lu-yu-li-shi-zi-liao-ku/appendix"),
    ]
    
    terms_to_check = [
        "德雷克星際",
        "羅伯茲太空工業",
        "星際引擎",
        "星際建築系統",
        "廢墟太空站",
        "亞倫環",
        "旅者聯合俱樂部",
        "克萊舍爾勞教所",
        "斯坦頓",
        "禿鷲",
        "坎比奧 打撈修復工具",
        "瑞倫",
        "指揮模組",
        "醫療凝膠",
        "維生系統",
        "奠基節",
        "科拉情人節",
        "光燈節",
        "互安防衛",
        "北境之巖服務團隊",
        "埃克哈特保全",
        "聯科發",
        "科瓦萊什貨運",
        "基格小行星帶",
        "QV 碎岩站",
        "SCM (戰鬥操控模式)",
        "NAV (巡航導航模式)",
        "異種威脅 (XenoThreat)",
    ]
    
    discrepancies = []
    for src_dir, dst_dir in mappings:
        src_path = repo_root / src_dir
        dst_path = repo_root / dst_dir
        for p in src_path.glob("**/*.md"):
            rel = p.relative_to(src_path)
            mirror_p = dst_path / rel
            if not mirror_p.exists():
                discrepancies.append(f"Missing mirror for {p}: expected {mirror_p}")
                continue
            src_txt = p.read_text(encoding="utf-8")
            dst_txt = mirror_p.read_text(encoding="utf-8")
            
            # Check hint count equality
            if src_txt.count("{% hint") != dst_txt.count("{% hint"):
                discrepancies.append(f"Hint count mismatch between {rel} ({src_txt.count('{% hint')}) and mirror ({dst_txt.count('{% hint')})")
                
            # Check terminology consistency
            for t in terms_to_check:
                if (t in src_txt) != (t in dst_txt):
                    discrepancies.append(f"Terminology presence mismatch for '{t}' in {rel} (src: {t in src_txt}, mirror: {t in dst_txt})")
                    
    if discrepancies:
        print(f"[FAIL] Found {len(discrepancies)} mirror discrepancies:")
        for d in discrepancies[:10]:
            print(f"  - {d}")
        sys.exit(1)
        
    print(f"✓ All mapped directories verified for hint and terminology parity across root and docs/.")

def main():
    repo_root = Path(__file__).resolve().parent.parent
    sc_dir = find_sc_knowledge_dir()
    test_term_resolver(sc_dir)
    test_markdown_compliance(repo_root)
    test_mirror_consistency(repo_root)
    print("\n🎉 ALL TERMINOLOGY & HINT VERIFICATIONS PASSED IN DOCKER!")

if __name__ == "__main__":
    main()
