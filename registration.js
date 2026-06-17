// API endpoint
const API_URL = 'https://api.krmconsultantsmbbs.in/api/register';

// Handle form submission
async function submitRegistration() {
  const name = document.getElementById('modal-name').value.trim();
  const phone = document.getElementById('modal-phone').value.trim();
  const seminarCity = document.getElementById('modal-select-city').value;
  const userCity = document.getElementById('modal-user-city').value;
  const studyInterestRadio = document.querySelector('input[name="study_interest"]:checked');
  const studyInterest = studyInterestRadio ? studyInterestRadio.value : 'Interested';

  // Validate required fields
  if (!name || !phone || !seminarCity || !userCity) {
    alert('❌ Please fill all fields');
    return false;
  }

  // Show loading state
  const submitBtn = document.querySelector('.btn-reserve');
  const originalText = submitBtn.textContent;
  submitBtn.disabled = true;
  submitBtn.textContent = '⏳ Submitting...';

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        phone: phone,
        seminarCity: seminarCity,
        userCity: userCity,
        studyInterest: studyInterest
      })
    });

    const data = await response.json();

    if (response.ok && data.success) {
      alert('✅ Registration submitted successfully! We\'ll WhatsApp you shortly.');
      
      // Clear form
      document.getElementById('modal-name').value = '';
      document.getElementById('modal-phone').value = '';
      document.getElementById('modal-select-city').value = '';
      document.getElementById('modal-user-city').value = '';
      
      closeModal();
    } else {
      alert('❌ Error: ' + (data.error || 'Failed to submit registration'));
    }
  } catch (error) {
    console.error('Error:', error);
    alert('❌ Network error. Please check if the server is running.\n\nMake sure to run: npm install && npm start');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = originalText;
  }
}
