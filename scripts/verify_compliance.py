#!/usr/bin/env python3
"""
IRH v21.4 Compliance Verification Script

Verifies that code adheres to the Theoretical Correspondence Mandate
and other compliance requirements defined in copilot-instructions.md.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Any


class ComplianceViolation:
    """Represents a compliance violation."""
    
    def __init__(self, category: str, message: str, file: str = None, line: int = None, severity: str = "error"):
        self.category = category
        self.message = message
        self.file = file
        self.line = line
        self.severity = severity
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "message": self.message,
            "file": self.file,
            "line": self.line,
            "severity": self.severity
        }


class ComplianceChecker:
    """Checks code for compliance with IRH v21.4 standards."""
    
    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.violations = []
        self.warnings = []
        self.passes_count = 0
    
    def log(self, message: str):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def add_violation(self, violation: ComplianceViolation):
        """Add a compliance violation."""
        if violation.severity == "error":
            self.violations.append(violation)
        else:
            self.warnings.append(violation)
        if self.verbose:
            symbol = "❌" if violation.severity == "error" else "⚠️"
            print(f"{symbol} {violation.category}: {violation.message}")
            if violation.file:
                print(f"   in {violation.file}:{violation.line or '?'}")
    
    def add_pass(self, message: str):
        """Record a passing check."""
        self.passes_count += 1
        if self.verbose:
            print(f"✅ {message}")
    
    def check_theoretical_references(self):
        """Check that functions have proper theoretical references."""
        self.log("Checking theoretical references in Python files...")
        
        python_files = list(self.repo_root.glob("python/src/**/*.py"))
        
        for py_file in python_files:
            if "__pycache__" in str(py_file) or "test_" in py_file.name:
                continue
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for functions that compute observables
                compute_functions = re.finditer(
                    r'def (compute_\w+|calculate_\w+)\s*\([^)]*\)\s*(?:->.*?)?:',
                    content
                )
                
                for match in compute_functions:
                    func_name = match.group(1)
                    func_start = match.start()
                    
                    # Look for docstring with theoretical reference
                    docstring_pattern = r'"""(.*?)"""'
                    docstring_match = re.search(docstring_pattern, content[func_start:func_start+2000], re.DOTALL)
                    
                    if docstring_match:
                        docstring = docstring_match.group(1)
                        # Check for theoretical references (IRH v21.4, Eq., §)
                        has_reference = bool(
                            re.search(r'IRH\s+v2[12]\.\d+', docstring, re.IGNORECASE) or
                            re.search(r'Eq\.\s*\d+', docstring) or
                            re.search(r'§\s*\d+', docstring) or
                            re.search(r'Appendix\s+[A-Z]', docstring)
                        )
                        
                        if has_reference:
                            self.add_pass(f"Function {func_name} has theoretical reference")
                        else:
                            line_num = content[:func_start].count('\n') + 1
                            self.add_violation(ComplianceViolation(
                                category="Missing Theoretical Reference",
                                message=f"Function '{func_name}' lacks theoretical reference (IRH v21.4, Eq., §, or Appendix)",
                                file=str(py_file.relative_to(self.repo_root)),
                                line=line_num,
                                severity="warning"
                            ))
                    else:
                        line_num = content[:func_start].count('\n') + 1
                        self.add_violation(ComplianceViolation(
                            category="Missing Docstring",
                            message=f"Function '{func_name}' lacks docstring",
                            file=str(py_file.relative_to(self.repo_root)),
                            line=line_num,
                            severity="warning"
                        ))
            
            except Exception as e:
                self.log(f"Error checking {py_file}: {e}")
    
    def check_critical_files(self):
        """Check that critical documentation files exist."""
        self.log("Checking critical files...")
        
        critical_files = [
            ".github/copilot-instructions.md",
            ".github/pull_request_template.md",
        ]
        
        for file_path in critical_files:
            full_path = self.repo_root / file_path
            if full_path.exists():
                self.add_pass(f"Critical file exists: {file_path}")
            else:
                self.add_violation(ComplianceViolation(
                    category="Missing Critical File",
                    message=f"Critical file missing: {file_path}",
                    file=file_path,
                    severity="error"
                ))
    
    def check_manuscript_references(self):
        """Check that manuscripts are properly referenced."""
        self.log("Checking manuscript references...")
        
        manuscripts = [
            "Intrinsic-Resonance-Holography-21.4-Part1.md",
            "Intrinsic-Resonance-Holography-21.4-Part2.md"
        ]
        
        for manuscript in manuscripts:
            full_path = self.repo_root / manuscript
            if full_path.exists():
                self.add_pass(f"Manuscript exists: {manuscript}")
            else:
                self.add_violation(ComplianceViolation(
                    category="Missing Manuscript",
                    message=f"Manuscript not found: {manuscript}",
                    file=manuscript,
                    severity="warning"
                ))
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate compliance report."""
        return {
            "compliant": len(self.violations) == 0,
            "violations": [v.to_dict() for v in self.violations],
            "warnings": [w.to_dict() for w in self.warnings],
            "passes_count": self.passes_count,
            "summary": {
                "total_violations": len(self.violations),
                "total_warnings": len(self.warnings),
                "total_passes": self.passes_count
            }
        }
    
    def run_all_checks(self):
        """Run all compliance checks."""
        self.check_critical_files()
        self.check_manuscript_references()
        self.check_theoretical_references()


def main():
    parser = argparse.ArgumentParser(
        description="Verify IRH v21.4 compliance"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--report",
        type=str,
        help="Path to save JSON report"
    )
    
    args = parser.parse_args()
    
    repo_root = Path(__file__).parent.parent
    checker = ComplianceChecker(repo_root, verbose=args.verbose)
    
    print("Running IRH v21.4 Compliance Checks...")
    checker.run_all_checks()
    
    report = checker.generate_report()
    
    if args.report:
        with open(args.report, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {args.report}")
    
    print("\n" + "="*60)
    print(f"Compliance Check Results:")
    print(f"  ✅ Passes: {report['passes_count']}")
    print(f"  ⚠️  Warnings: {len(report['warnings'])}")
    print(f"  ❌ Violations: {len(report['violations'])}")
    print("="*60)
    
    if report['compliant']:
        print("\n✅ Code is compliant with IRH v21.4 standards")
        return 0
    else:
        print("\n❌ Compliance check failed - see violations above")
        return 1


if __name__ == "__main__":
    sys.exit(main())
