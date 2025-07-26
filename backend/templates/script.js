// Import Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-app.js";
import { getFirestore, collection, getDocs, query, orderBy } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBRXOSaE7kD73aElC_4EcjswfyCBjQseNI",
  authDomain: "homework-app-9b95f.firebaseapp.com",
  projectId: "homework-app-9b95f",
  storageBucket: "homework-app-9b95f.appspot.com",  // fixed typo
  messagingSenderId: "145897834934",
  appId: "1:145897834934:web:2eba3483c605a6b538d917",
  measurementId: "G-VTXM1E72LF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// Load homework from Firestore
async function loadHomework() {
  const list = document.getElementById('all-homework-list');  // fixed ID
  if (!list) return;

  list.innerHTML = '<li class="list-group-item">Loading homework...</li>';

  try {
    const homeworkRef = collection(db, 'homeworks');
    const q = query(homeworkRef, orderBy("date", "desc"));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      list.innerHTML = '<li class="list-group-item">No homework found.</li>';
      return;
    }

    list.innerHTML = '';

    snapshot.forEach(doc => {
      const data = doc.data();
      const subject = data.subject || 'No subject';
      const details = data.details || 'No details provided';

      const li = document.createElement('li');
      li.className = 'list-group-item';
      li.textContent = `${subject}: ${details}`;
      list.appendChild(li);
    });

  } catch (error) {
    list.innerHTML = `<li class="list-group-item text-danger">Error loading homework: ${error.message}</li>`;
  }
}

// Run when DOM is ready
window.addEventListener('DOMContentLoaded', loadHomework);

