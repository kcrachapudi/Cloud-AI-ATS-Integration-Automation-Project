🚀 AI-Powered Resume Processing & ATS Automation Pipeline (AWS)
📌 Overview

This project is a serverless, AI-powered resume processing pipeline built on AWS. It automates the ingestion, analysis, and scoring of resumes using cloud-native services and AI, enabling an ATS-style evaluation system.

The system leverages event-driven architecture to process resumes in real time as soon as they are uploaded.

🧠 Key Features
⚡ Event-Driven Automation
Automatically triggers processing when a resume is uploaded
🤖 AI-Powered Resume Evaluation
Uses AWS AI services to extract insights and evaluate candidate profiles
📄 Document Processing
Parses and extracts structured data from .docx resumes
📊 ATS-Style Scoring System
Assigns scores to resumes based on predefined criteria
☁️ Serverless Architecture
Fully managed, scalable, and cost-efficient
🔐 Secure Cloud Integration
IAM roles and policies ensure secure service communication
🏗️ Architecture
          +-------------------+
          |   Amazon S3       |
          | (Resume Upload)   |
          +---------+---------+
                    |
                    | Event Trigger
                    ↓
          +-------------------+
          |   AWS Lambda      |
          | (Processing Logic)|
          +---------+---------+
                    |
                    ↓
          +-------------------+
          |   AWS AI Services |
          | (Analysis/Scoring)|
          +---------+---------+
                    |
                    ↓
          +-------------------+
          |   DynamoDB        |
          | (Store Results)   |
          +-------------------+
⚙️ Tech Stack
Cloud: AWS (S3, Lambda, DynamoDB, IAM, CloudWatch)
Language: Python
AI Services: AWS AI (NLP / Document Analysis)
Data Processing: python-docx
Infrastructure: Serverless
🔄 Workflow
Upload a resume (.docx) to S3
S3 triggers a Lambda function
Lambda:
Retrieves the file
Extracts text and structured data
Sends data to AWS AI services
Generates evaluation score
Results are stored in DynamoDB
Logs and errors are tracked via CloudWatch
📊 Sample Output (DynamoDB)
{
  "resume_id": "resume_2",
  "score": 0.87,
  "skills": ["Python", "AWS", "Machine Learning"],
  "experience": "3 years",
  "summary": "Strong backend and cloud experience"
}
🔐 Security
IAM roles configured for:
S3 access
DynamoDB write operations
AI service integration
Least privilege access enforced
🧪 Challenges Solved

This project addresses real-world AWS challenges:

❌ S3 object key mismatches → ✅ Correct key handling
❌ Region mismatches → ✅ Unified configuration
❌ IAM permission errors → ✅ Role-based access control
❌ Data type issues (float vs Decimal) → ✅ DynamoDB-compatible data handling
📈 Future Enhancements
🔍 Resume search and filtering API
🌐 FastAPI backend for querying results
🤖 Advanced AI scoring using LLMs
📊 Dashboard for visualization
📥 Bulk resume processing
💡 Use Cases
Applicant Tracking Systems (ATS)
HR automation platforms
AI document processing pipelines
Resume screening tools
🧑‍💻 Author

Kalyan Rachapudi
Software Engineer | Cloud | AI Automation

⭐ Why This Project Matters

This project demonstrates:

Real-world cloud integration (S3 → Lambda → DynamoDB)
AI-powered automation in production-like workflows
Hands-on experience with serverless architecture
Ability to debug and solve complex AWS issues
📬 Feedback

Feel free to open issues or suggestions to improve the project!

Next Iteration:

Add a FastAPI layer 
🔥 Pro Tip (Do This Next)

Add these to your repo to make it elite-level:

Screenshots of AWS Console (S3, Lambda, DynamoDB)
Sample logs from CloudWatch
2–3 sample resumes for testing
Short demo video (HUGE impact)

