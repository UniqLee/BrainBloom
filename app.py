from google import genai

client = genai.Client(api_key="AIzaSyAP05RYwa__zILpmycarX_UlM_HlA25gYQ")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain what programming is "
)
print(response.text)
