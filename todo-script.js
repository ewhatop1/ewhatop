// 1. 날짜 표시 (DOM 완성 후 실행)
document.addEventListener("DOMContentLoaded", function () {
  const dateDiv = document.querySelector(".date");
  const today = new Date().toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    weekday: "long"
  });
  if(dateDiv) dateDiv.textContent = today;
});

// 2. 체크박스 클릭 시 DB에 완료 상태 반영
function markDone(todoId, checked) {
  fetch('/todo/done', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({todo_id: todoId, done: checked})
  })
  .then(response => response.json())
  .then(data => {
    if(data.result !== 'success') {
      alert('DB 갱신 실패!');
    }
  });
}
