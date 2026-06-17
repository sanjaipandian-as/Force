import re

file_path = r'd:\Zippy\FORCE\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove univ-logo-avatar divs
content = re.sub(r'\s*<div class=\"univ-logo-avatar[^\>]+>.*?<\/div>', '', content)

# Extract sections
def extract_section(country_name):
    pattern = rf'(<!-- {country_name} Section -->.*?</div>\s*</div>)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1), match.span()
    return None, None

russia, r_span = extract_section('Russia')
vietnam, v_span = extract_section('Vietnam')
uzbekistan, u_span = extract_section('Uzbekistan')
georgia, g_span = extract_section('Georgia')
kyrgyzstan, k_span = extract_section('Kyrgyzstan')

# Desired order: Russia, Georgia, Uzbekistan, Kyrgyzstan, Vietnam
if all([russia, georgia, uzbekistan, kyrgyzstan, vietnam]):
    new_order = russia + '\n\n' + georgia + '\n\n' + uzbekistan + '\n\n' + kyrgyzstan + '\n\n' + vietnam
    
    start_idx = min(r_span[0], v_span[0], u_span[0], g_span[0], k_span[0])
    end_idx = max(r_span[1], v_span[1], u_span[1], g_span[1], k_span[1])
    
    content = content[:start_idx] + new_order + content[end_idx:]

# Update footer style (squares pattern)
footer_css_pattern = r'(footer\s*\{\s*background:\s*#FFFFFF;\s*background-image:\s*)radial-gradient\([^\)]+\)(;)'
new_footer_css = r'\1linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px)\2'
content = re.sub(footer_css_pattern, new_footer_css, content)

# Add square background-size
content = re.sub(r'(background-size:\s*)20px 20px(;)', r'\1 30px 30px\2', content)

# Update Past Events Section
past_events_pattern = r'(<!-- Past Events \/ Completed Seminars -->\s*<section class=\"past-events-section\"[^>]+>.*?<div style=\"font-size: 42px; font-weight: 800; color: #00bb23; line-height: 1; margin-bottom: 6px;\">263</div>.*?</div>\s*</div>)'
past_events_addition = r'''\1
  <!-- Past Seminar Images -->
  <div style="max-width: 900px; margin: 40px auto 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/partner_1.webp" alt="Seminar Setup" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/partner_2.webp" alt="Seminar Audience" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/hero_medical_bg.webp" alt="Doctor Mentorship" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/hero_university_bg.webp" alt="University Discussion" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
  </div>'''

content = re.sub(past_events_pattern, past_events_addition, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated index.html successfully.')
