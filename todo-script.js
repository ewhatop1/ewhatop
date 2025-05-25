<script>
  document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.querySelector(".add-todo");
    const inputBox = document.querySelector(".add-task-box");
    const todoList = document.querySelector(".todo-list");
    const dateDiv = document.querySelector(".date");

    // 오늘 날짜 한국어로 표시
    const today = new Date().toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "long",
      day: "numeric",
      weekday: "long"
    });
    dateDiv.textContent = today;

    // 할 일 추가 버튼 클릭 이벤트
    addButton.addEventListener("click", function () {
      const task = inputBox.value.trim();

      // 입력창이 보이지 않으면 보여주기
      if (inputBox.offsetParent === null) {
        inputBox.style.display = "inline-block";
        inputBox.focus();
        return;
      }

      // 입력값이 있을 경우, 새로운 할 일 추가
      if (task !== "") {
        const newTodo = document.createElement("li");
        const newId = "todo" + Date.now();

        newTodo.innerHTML = `
          <input type="checkbox" id="${newId}">
          <label for="${newId}">${task}</label>
        `;
        todoList.appendChild(newTodo);

        // 입력창 초기화 및 숨기기
        inputBox.value = "";
        inputBox.style.display = "none";
      }
    });
  });
</script>
