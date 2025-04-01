import matplotlib.pyplot as plt
import numpy as np

def Practical_10():
    print("\n" + "="*50)
    print("AI ETHICS CASE STUDY: FACIAL RECOGNITION & PRIVACY")
    print("="*50 + "\n")
    
    # Case Study Overview
    print("CASE STUDY: CLEARVIEW AI FACIAL RECOGNITION")
    print("Background:")
    print("- Scraped billions of images from social media without consent")
    print("- Built facial recognition database sold to law enforcement")
    print("- Operated with minimal transparency or oversight\n")
    
    # Ethical Issues Visualization
    issues = ['Privacy Violation', 'Lack of Consent', 'Surveillance Risks', 
              'Bias in Accuracy', 'Accountability Gaps']
    severity = [9, 8, 8, 7, 6]
    
    plt.figure(figsize=(10, 6))
    plt.barh(issues, severity, color=['#ff6b6b', '#ffa502', '#ff793f', '#ff5252', '#ff7f50'])
    plt.title('Key Ethical Concerns in Facial Recognition AI', pad=20)
    plt.xlim(0, 10)
    plt.grid(axis='x', alpha=0.3)
    plt.xlabel('Severity (1-10)')
    plt.tight_layout()
    plt.show()
    
    # Bias Analysis
    print("\nBIAS IN FACIAL RECOGNITION SYSTEMS:")
    groups = ['White Males', 'Women of Color', 'Dark-Skinned Women', 'Asian Females']
    accuracy = [98, 65, 79, 82]
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(groups, accuracy, color=['#3498db', '#e74c3c', '#e74c3c', '#f39c12'])
    plt.title('Facial Recognition Accuracy by Demographic Group')
    plt.ylabel('Accuracy (%)')
    plt.ylim(0, 100)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%', ha='center', va='bottom')
    plt.show()
    
    # Ethical Framework
    print("\nETHICAL FRAMEWORK FOR RESPONSIBLE AI:")
    principles = ['Privacy Protection', 'Informed Consent', 'Bias Mitigation', 
                 'Transparency', 'Accountability']
    implementation = [
        "Data minimization & encryption",
        "Opt-in systems with clear explanations",
        "Diverse datasets & fairness testing",
        "Explainable AI & open documentation",
        "Audit trails & redress mechanisms"
    ]
    
    print("\n".join([f"{p+':':<20} {i}" for p, i in zip(principles, implementation)]))
    
    # Regulatory Landscape
    print("\nGLOBAL REGULATORY APPROACHES:")
    regulations = {
        'EU AI Act': "Banned real-time facial recognition in public spaces",
        'US State Laws': "Patchwork of local restrictions (e.g., Illinois BIPA)",
        'China': "Extensive use with social credit system integration",
        'Canada': "Ruled Clearview violated privacy laws"
    }
    
    for k, v in regulations.items():
        print(f"- {k:<15}: {v}")
    
    # Actionable Solutions
    print("\nACTIONABLE SOLUTIONS:")
    solutions = [
        ("Technical", "Develop bias-detection tools & federated learning"),
        ("Legal", "Implement strict data protection laws (GDPR++)"),
        ("Organizational", "Create ethics review boards for AI projects"),
        ("Social", "Public awareness campaigns about facial recognition")
    ]
    
    for category, solution in solutions:
        print(f"{category+':':<15} {solution}")
    
    # Return ethical framework
    return {
        'issues': issues,
        'principles': principles,
        'case_study': "Clearview AI Facial Recognition"
    }

# Call the function with:
# ethics_report = Practical_10()