// Interactive background floating icons follow mouse movement
(() => {
  const bgIcons = document.querySelectorAll('.bg-icon');

  window.addEventListener('mousemove', (e) => {
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;

    bgIcons.forEach((icon, index) => {
      const intensity = (index + 1) * 5; // Different for each icon
      const moveX = (e.clientX - centerX) / intensity;
      const moveY = (e.clientY - centerY) / intensity;
      icon.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });
  });
})();

// Placeholder: Load homework dynamically (replace with your actual code)
function loadHomework() {
  const homeworkList = document.getElementById('homework-list');
  if (!homeworkList) return;

  // Example static homework data
  const homeworkItems = [
    'Math: Complete exercise 5.3 (Q1–Q5) from NCERT book.',
    'English: Write a summary of Chapter 4.',
    'Science: Draw and label plant cell parts.',
  ];

  homeworkList.innerHTML = ''; // Clear loading message

  homeworkItems.forEach((item) => {
    const li = document.createElement('li');
    li.className = 'list-group-item';
    li.textContent = item;
    homeworkList.appendChild(li);
  });
}

// Call loadHomework when page loads
window.addEventListener('DOMContentLoaded', loadHomework);
