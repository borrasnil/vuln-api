function showChallenge(num) {
  document.querySelectorAll('.challenge-content').forEach(el => el.classList.add('hidden'));
  document.getElementById('challenge-' + num).classList.remove('hidden');
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('bg-red-600');
    btn.classList.add('bg-gray-700');
    if (parseInt(btn.dataset.challenge) === num) {
      btn.classList.remove('bg-gray-700');
      btn.classList.add('bg-red-600');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  showChallenge(1);
});