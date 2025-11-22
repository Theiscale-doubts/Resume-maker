import json
import os
from dotenv import load_dotenv
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

load_dotenv()

# Configure Gemini API
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)

@csrf_exempt
@require_http_methods(["POST"])
def generate_summary(request):
    try:
        data = json.loads(request.body)
        job_title = data.get('jobTitle')
        skills = data.get('skills')
        current_summary = data.get('currentSummary', '')

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
          You are an expert career coach. Write a professional, compelling, and ATS-friendly resume summary (approx 3-4 sentences) for a {job_title}. 
          Key skills: {skills}.
          {f'Current draft to improve: "{current_summary}"' if current_summary else ''}
          
          Focus on professional achievements and value proposition. Do not use "I" excessively. Keep it concise.
        """

        response = model.generate_content(prompt)
        return JsonResponse({'summary': response.text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def enhance_description(request):
    try:
        data = json.loads(request.body)
        description = data.get('description')
        role = data.get('role')

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
          You are an expert resume editor. Rewrite the following job description bullet points for a {role} role to be more impactful, action-oriented, and ATS-friendly.
          
          Original text:
          "{description}"
          
          Rules:
          1. Use strong action verbs (Led, Developed, Engineered).
          2. Quantify results where possible (e.g., "improved by 20%").
          3. Keep formatting as a bulleted list (using • or -).
          4. Fix any grammar or spelling errors.
          5. Return ONLY the rewritten text.
        """

        response = model.generate_content(prompt)
        return JsonResponse({'enhancedDescription': response.text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def analyze_resume(request):
    try:
        data = json.loads(request.body)
        resume_data = data.get('resumeData')

        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""
          Act as an ATS (Applicant Tracking System) scanner. Analyze the following resume JSON data.
          
          Resume Data: {json.dumps(resume_data)}

          Provide the output in the following JSON format ONLY (no markdown):
          {{
            "score": number (0-100),
            "feedback": [string array of 3-5 concise tips to improve the resume or missing keywords based on the job title]
          }}
        """

        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        result = json.loads(response.text)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
