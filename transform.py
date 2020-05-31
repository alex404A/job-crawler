import json

forbidden_companies = []
forbidden_keywords = []
available_urls = []

def is_job_ok(candidate):
    if not candidate['is_friendly']:
        return False
    if candidate['company'].strip().lower() in forbidden_companies:
        return False
    name = candidate['name'].strip().lower()
    if any(x.lower().strip() in name for x in forbidden_keywords):
        return False
    return True

with open('./filter_condition/forbidden_companies.txt','r') as f:
  forbidden_companies = [x.strip().lower() for x in f.read().split('\n') if x.strip() != '']

with open('./filter_condition/forbidden_keywords.txt','r') as f:
  forbidden_keywords = [x.strip().lower() for x in f.read().split('\n') if x.strip() != '']

with open('jd.jl','r') as f:
  candidates = [json.loads(x) for x in f.read().split('\n') if x.strip() != '']
  for candidate in candidates:
      if is_job_ok(candidate):
        available_urls.append(candidate['url'])

with open('available.txt', 'w') as the_file:
    the_file.write('\n'.join(available_urls))
