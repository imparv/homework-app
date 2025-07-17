document.addEventListener('DOMContentLoaded', () => {
  const homeworkList = document.getElementById('homework-list');
  const downloadsList = document.getElementById('downloads-list');

  // Example static data (replace with Firebase later)
  const homework = [
    "Math - Solve exercise 6.2",
    "Science - Read chapter 4 and write notes",
    "English - Write an essay on 'My Hobby'"
  ];

  const notes = [
    { name: "Math Notes (PDF)", link: "#" },
    { name: "Science Diagrams", link: "#" },
    { name: "English Grammar Sheet", link: "#" }
  ];

  // Populate homework
  homeworkList.innerHTML = "";
  homework.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    homeworkList.appendChild(li);
  });

  // Populate downloads
  downloadsList.innerHTML = "";
  notes.forEach(note => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = note.link;
    a.textContent = note.name;
    a.target = "_blank";
    li.appendChild(a);
    downloadsList.appendChild(li);
  });
});
