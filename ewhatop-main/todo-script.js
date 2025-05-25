<script>
  document.addEventListener("DOMContentLoaded", function () {
    const dateDiv = document.querySelector(".date");
    // 오늘 날짜 한국어로 표시
    const today = new Date().toLocaleDateString("ko-KR", {
      year: "numeric",
      month: "long",
      day: "numeric",
      weekday: "long"
    });
    dateDiv.textContent = today;
  });
</script>
