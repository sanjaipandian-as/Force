import re

file_path = r'd:\Zippy\FORCE\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Re-apply WebP image compressions & basic optimizations
# We'll just replace known image names with their .webp counterparts
webp_replacements = {
    'Hereup.png': 'Hereup.webp',
    'samara.jpg': 'samara.webp',
    'University%20of%20Georgia.jpg': 'University%20of%20Georgia.webp',
    'tashkent.jpg': 'tashkent.webp',
    'fergama.jpg': 'fergama.webp',
    'can%20tho.jpg': 'can%20tho.webp',
    'kazan%20state.jpg': 'kazan%20state.webp',
    'Andijan.jpg': 'Andijan.webp',
    'BAU%20International%20University.jpg': 'BAU%20International%20University.webp',
    'crimae.jpg': 'crimae.webp',
    'dai%20num.jpg': 'dai%20num.webp',
    'phan%20chaue.jpg': 'phan%20chaue.webp',
    'Mardovia.jpg': 'Mardovia.webp',
    'Buon%20ma.jpg': 'Buon%20ma.webp',
    'Kyrgyz-Uzbek%20University%20Medical%20Faculty.jpg': 'Kyrgyz-Uzbek%20University%20Medical%20Faculty.webp'
}
for old, new in webp_replacements.items():
    content = content.replace(old, new)

# Also preload Hereup.webp instead of hero_university_bg.webp
content = re.sub(r'<link rel="preload" href="assets/hero_university_bg\.webp".*?>', 
                 r'<link rel="preload" href="assets/Hereup.webp" as="image" fetchpriority="high">', content)
# And add <picture> fallback for Hereup
content = content.replace(
    '<img src="assets/Hereup.webp" alt="MBBS Abroad Seminar"\n      style="width: 100%; height: auto; display: block;" />',
    '<picture><source srcset="assets/Hereup.webp" type="image/webp"><img src="assets/Hereup.png" alt="MBBS Abroad Seminar" width="1920" height="auto" fetchpriority="high" decoding="sync" style="width: 100%; height: auto; display: block;" /></picture>'
)

# Fix fonts: remove Syne, simplify Inter
content = re.sub(r'family=Syne.*?&', '', content)
content = content.replace("font-family: 'Syne', sans-serif;", "font-family: 'Inter', sans-serif;")

# 2. Remove .univ-logo-avatar tags
content = re.sub(r'\s*<div class=\"univ-logo-avatar[^\>]+>.*?<\/div>', '', content)

# 3. Reorder Sections
# Find indices
idx_russia = content.find('<!-- Russia Section -->')
idx_vietnam = content.find('<!-- Vietnam Section -->')
idx_uzbek = content.find('<!-- Uzbekistan Section -->')
idx_georgia = content.find('<!-- Georgia Section -->')
idx_kyrgyz = content.find('<!-- Kyrgyzstan Section -->')
idx_end = content.find('<!-- Trusted Partners Section -->')

if all(idx != -1 for idx in [idx_russia, idx_vietnam, idx_uzbek, idx_georgia, idx_kyrgyz, idx_end]):
    russia_sec = content[idx_russia:idx_vietnam]
    vietnam_sec = content[idx_vietnam:idx_uzbek]
    uzbek_sec = content[idx_uzbek:idx_georgia]
    georgia_sec = content[idx_georgia:idx_kyrgyz]
    kyrgyz_sec = content[idx_kyrgyz:idx_end]
    
    # New order: Russia, Georgia, Uzbekistan, Kyrgyzstan, Vietnam
    new_sections = russia_sec + georgia_sec + uzbek_sec + kyrgyz_sec + vietnam_sec
    content = content[:idx_russia] + new_sections + content[idx_end:]

# 4 & 5. Past Events text and professional badge
past_events_pattern = r'<div\s*style="background:\s*rgba\(0,\s*187,\s*35,\s*0\.1\);[^>]+>.*?Completed Successfully\s*</div>\s*</div>\s*<h3[^>]+>2\)\s*May 10 –\s*Chennai</h3>'
new_past_events = '''<div style="font-size: 13px; font-weight: 700; color: #00bb23; text-transform: uppercase; letter-spacing: 0.08em; display: block;">
          Previous seminars
        </div>
      </div>
      <h3 style="font-size: 28px; font-weight: 800; color: #0f1419; margin: 0 0 8px 0; line-height: 1.2;">May 10 –
        Chennai</h3>'''
content = re.sub(past_events_pattern, new_past_events, content, flags=re.DOTALL)

# 6. Location icon in city-strip
city_strip_css_pattern = r'(\.city-strip-inner span\s*\{[^}]+)(margin-right:\s*48px;\s*\})'
new_city_strip_css = r'''\1\2
    .city-strip-inner span { display: inline-flex; align-items: center; gap: 6px; }
    .city-strip-inner span::before { content: ''; display: inline-block; width: 14px; height: 14px; background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'%3E%3C/path%3E%3Ccircle cx='12' cy='10' r='3'%3E%3C/circle%3E%3C/svg%3E"); background-size: contain; background-repeat: no-repeat; background-position: center; }'''
content = re.sub(city_strip_css_pattern, new_city_strip_css, content)

# 7. Add Checkbox to form
form_pattern = r'(<option>Other City</option>\s*</select>\s*</div>)(\s*<button type="submit" class="btn-reserve">)'
form_addition = r'''\1
      <div class="form-row" style="margin-top: 4px;">
        <label>Study abroad preference</label>
        <div style="display: flex; gap: 16px; margin-top: 8px;">
          <label style="display: flex; align-items: center; gap: 6px; font-weight: 500; cursor: pointer; text-transform: none; color: #1f2937;">
            <input type="radio" name="study_interest" value="Interested" checked style="width: auto; height: auto;">
            Interested
          </label>
          <label style="display: flex; align-items: center; gap: 6px; font-weight: 500; cursor: pointer; text-transform: none; color: #1f2937;">
            <input type="radio" name="study_interest" value="Not Interested" style="width: auto; height: auto;">
            Not interested
          </label>
        </div>
      </div>\2'''
content = re.sub(form_pattern, form_addition, content)

# 8. Add 4-image grid to Past Events
# Look for Students Attended</div></div>
grid_pattern = r'(Students Attended</div>\s*</div>)(\s*</div>\s*</section>)'
grid_addition = r'''\1
  <!-- Past Seminar Images -->
  <div style="max-width: 900px; margin: 40px auto 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px;">
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/partner_1.webp" alt="Seminar Setup" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/partner_2.webp" alt="Seminar Audience" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/hero_medical_bg.webp" alt="Doctor Mentorship" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
    <div style="border-radius: 16px; overflow: hidden; aspect-ratio: 4/3; box-shadow: 0 8px 24px rgba(0,0,0,0.06); border: 2px solid #fff;"><img src="assets/hero_university_bg.webp" alt="University Discussion" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'" loading="lazy" decoding="async"></div>
  </div>\2'''
content = re.sub(grid_pattern, grid_addition, content)

# 9. Footer background
footer_css_pattern = r'(footer\s*\{\s*background:\s*#FFFFFF;\s*background-image:\s*)radial-gradient\([^\)]+\)(;)'
new_footer_css = r'\1linear-gradient(rgba(0, 0, 0, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 0, 0, 0.03) 1px, transparent 1px)\2'
content = re.sub(footer_css_pattern, new_footer_css, content)
content = re.sub(r'(background-size:\s*)20px 20px(;)', r'\1 30px 30px\2', content)

# 10. Defer instagram iframes (lazy load trick)
content = content.replace('src="https://www.instagram.com', 'data-src="https://www.instagram.com')

# Make sure playMockVideo correctly lazy-loads
lazy_video_js = r'''  function playMockVideo() {
    const videoModal = document.getElementById('video-modal');
    const videoElement = document.getElementById('modal-video-element');
    if (videoModal && videoElement) {
      const source = videoElement.querySelector('source[data-src]');
      if (source && !source.src) { source.src = source.getAttribute('data-src'); videoElement.load(); }
      videoModal.classList.add('active');
      document.body.style.overflow = 'hidden';
      videoElement.currentTime = 0;
      videoElement.play().catch(err => { console.log('Autoplay prevented'); });
    }
  }'''
content = re.sub(r'function playMockVideo\(\)\s*\{.*?\}', lazy_video_js, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied full robust update!")
