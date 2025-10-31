"""
Test script for enhanced AI chat features
Tests special handlers: greetings, developer, location, thank you
"""

from ai_training_data import get_ai_response
import json

def test_ai():
    """Run tests and save results to avoid console encoding issues"""
    
    tests = [
        ("Greeting", "Hello"),
        ("Developer", "Who developed this?"),
        ("Location", "Where is your main branch?"),
        ("Thanks", "Thank you!"),
        ("GPU Question", "Best GPU for 1440p?"),
        ("Tagalog", "Anong oras kayo open?"),
        ("Store Hours", "What are your store hours?"),
        ("Compatibility", "Is my PC compatible?"),
        ("Future Proof", "How to future-proof my build?"),
        ("RAM Mix", "Can I mix different RAM brands?"),
    ]
    
    results = []
    print("Running AI Enhancement Tests...")
    print("=" * 60)
    
    for test_name, question in tests:
        try:
            response = get_ai_response(question)
            status = "PASS" if len(response) > 50 else "FAIL"
            
            # Store result
            results.append({
                "test": test_name,
                "question": question,
                "status": status,
                "response_length": len(response),
                "response_preview": response[:100] if len(response) > 100 else response
            })
            
            print(f"{status}: {test_name} - {len(response)} chars")
            
        except Exception as e:
            results.append({
                "test": test_name,
                "question": question,
                "status": "ERROR",
                "error": str(e)
            })
            print(f"ERROR: {test_name} - {str(e)}")
    
    # Save results to file
    with open("ai_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {sum(1 for r in results if r.get('status') == 'PASS')}")
    print(f"Failed: {sum(1 for r in results if r.get('status') != 'PASS')}")
    print("\nResults saved to: ai_test_results.json")
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_ai()
