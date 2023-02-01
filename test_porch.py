from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")
model = AutoModelForQuestionAnswering.from_pretrained("bert-large-uncased-whole-word-masking-finetuned-squad")

text = r"""
"Miro Careers | Open Positions at MiroCareersOur storyPeopleHow we hireOpen positions→Our storyPeopleHow we hireOpen positions→Open positionsRyanAre you ready for a career without edges? At Miro, we are a global team of nearly 1,800 dreamers, thinkers, builders, storytellers, engineers and designers. We dream big, aim high, and let our failures inform our future successes.MarvinThierryOpen positionsFor example: software engineerproduct managerAll departmentsAll departmentsBusiness TechnologyCustomer ExperienceData & AnalyticsDesignEngineeringFinanceLegalMarketingOperationsPeopleProductAll locationsAll locationsAmsterdam, NLAmsterdam, NetherlandsAustin, USBerlin, DEMunich, DENew York, USRemote, EMEARemote, USYerevan, ArmeniaEMEA Sales Strategy and Operations ManagerOperationsAmsterdam, Netherlands Employee Relations Manager, NL & UK PeopleAmsterdam, Netherlands Engineering ManagerEngineeringBerlin, DEEngineering Manager Backend (Core Product, Board Server)EngineeringYerevan, ArmeniaEngineering Manager Backend (Core Product, Business Logic)EngineeringYerevan, ArmeniaEngineering Manager Backend (Core Product, CanvasLogic)EngineeringYerevan, ArmeniaEngineering Manager (Database Engineering)EngineeringAmsterdam, NetherlandsEngineering Manager Frontend (Core Product, Canvas Engine)EngineeringYerevan, Armenia12...9Prepare yourself to go beyondHere are some helpful tips to ensure you have all the correct information throughout our hiring process.How we hire→Miro Together: Hybrid strategyJoining Miro is one of the best career moves you’ll ever make.Our best work happens when we build strong working relationships with each other. We believe that a flexible mix of in-person and remote co-creation works best for everyone. For this reason, we remain committed to a hub-centric, hybrid working model. We call it Miro Together.How we hire→Team daysLearn from each other, share insights and build skills.Culture daysBuild connections and foster culture through shared experiences.Still have questions?Can I apply in another language other than English?Our business language is English, and while we are an international company with many languages spoken, we encourage you to apply in English.I know someone working at Miro. Can they refer me?Absolutely! Please reach out to your contact and ask them to submit your candidacy as a referral (we have a very well-regulated referral program). Or, if you decide to apply directly, please go ahead, and our respective recruiting specialist will contact you.How do I apply for a traineeship/internship role?Miro is piloting APM (Associate Product Management) Program this year. The application period is closed now. Make sure you check back for future intakes.Will the interview happen face-to-face?Face-to-face interviews are an option alongside a virtual interview. It will depend on the role's location and other details. Your respective recruiting partner will walk you through the process and align on the best possible set-up.What are the benefits?You can learn more about the benefits you receive at Miro at the end of each job description.What are the equity offerings and potential value? RSUs? How does that factor into the total comp package?Our Head of Talent has written a blog post on this topic on our Miro Blog page. You can read the post here.What is the leveling structure internally?At Miro, we have a global Career Map - a framework which we use to explain, design and develop our organization as well as to define, facilitate and track the career growth of Mironeers. In alignment with this Map, we have a title structure that includes public roles and private levels and titles.How is performance measured?For individual performance measurement, we’re conducting a bi-annual review of each Mironeer’s performance through peer and manager feedback. The process involves all Mironeers who have been in the company for longer than 4 months. A significant part of this performance review is a strengths-based feedback and development areas discussion, together with feedback against our behavior rubric (4 stages rubric highlighting expected behavior based on company culture values).\nThe expected outcome of every performance review is actionable feedback that can lead to a growth plan and personal OKRs.How do your values influence the culture?Visit our people page to learn more about our values.Ready to go beyond?For example: software engineerproduct managerAll departmentsAll departmentsBusiness TechnologyCustomer ExperienceData & AnalyticsDesignEngineeringFinanceLegalMarketingOperationsPeopleProductAll locationsAll locationsAmsterdam, NLAmsterdam, NetherlandsAustin, USBerlin, DEMunich, DENew York, USRemote, EMEARemote, USYerevan, ArmeniaSearchCareersHomeOur StoryPeopleHow we hireCompanyAbout MiroMiro in the NewsCustomer storiesCompany Events© 2022 MiroTerms of ServicePrivacy PolicyManage Cookies"
"""

questions = [
    "How many jobs are open?"
]

for question in questions:
    inputs = tokenizer(question, text, add_special_tokens=True, return_tensors="pt")
    input_ids = inputs["input_ids"].tolist()[0]

    outputs = model(**inputs)
    answer_start_scores = outputs.start_logits
    answer_end_scores = outputs.end_logits

    # Get the most likely beginning of answer with the argmax of the score
    answer_start = torch.argmax(answer_start_scores)
    # Get the most likely end of answer with the argmax of the score
    answer_end = torch.argmax(answer_end_scores) + 1

    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[answer_start:answer_end])
    )

    print(f"Question: {question}")
    print(f"Answer: {answer}")