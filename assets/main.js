(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // 대장 카드는 뒤에 오는 장이 앞 장을 덮도록 쌓는다.
  var cards = document.querySelectorAll('.stack .card');
  for (var i = 0; i < cards.length; i++) cards[i].style.zIndex = String(i + 1);

  if (reduce) return;

  // 첫 화면 제목을 글자 단위로 쪼개 한 글자씩 올라오게 한다.
  var title = document.querySelector('.hero-title');
  var lines = document.querySelectorAll('.hero-line');
  var delay = 0.05;
  if (title) title.setAttribute('aria-label', title.textContent.replace(/\s+/g, ' ').trim());
  for (var l = 0; l < lines.length; l++) {
    var line = lines[l];
    var text = line.textContent;
    line.textContent = '';
    for (var c = 0; c < text.length; c++) {
      var span = document.createElement('span');
      span.className = 'hero-char';
      span.setAttribute('aria-hidden', 'true');
      span.textContent = text[c];
      span.style.animationDelay = delay.toFixed(3) + 's';
      line.appendChild(span);
      delay += 0.035;
    }
    delay += 0.2;
  }

  // 스크롤에 따라 제목 두 줄은 좌우로, 사진은 위아래로 조금씩 흐른다.
  var drifters = document.querySelectorAll('[data-drift]');
  var photo = document.querySelector('[data-drift-y]');
  var ticking = false;
  function update() {
    ticking = false;
    var y = Math.min(window.scrollY, 900);
    for (var d = 0; d < drifters.length; d++) {
      var dir = Number(drifters[d].getAttribute('data-drift'));
      drifters[d].style.transform = 'translateX(' + (dir * y * 0.08).toFixed(1) + 'px)';
    }
    if (photo) photo.style.transform = 'translateY(' + (y * -0.06).toFixed(1) + 'px)';
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
})();
