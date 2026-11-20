(function initializeGalleries() {
  const slideInterval = 5000;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  function initializeSlider(slider) {
    const track = slider.querySelector('.graduation-track');
    const slides = Array.from(track.children);
    let activeIndex = 0;
    let isHovered = false;
    let isFocused = false;
    let isTouching = false;
    let timer;
    let scrollFrame;

    function showSlide(index) {
      const nextIndex = (index + slides.length) % slides.length;
      track.scrollTo({
        left: nextIndex * track.clientWidth,
        behavior: reducedMotion.matches ? 'instant' : 'smooth'
      });
    }

    function updatePlayback() {
      clearInterval(timer);

      const shouldPause = reducedMotion.matches || isHovered ||
        isFocused || isTouching || document.hidden;

      if (!shouldPause) {
        timer = setInterval(function advanceSlide() {
          showSlide(activeIndex + 1);
        }, slideInterval);
      }
    }

    slider.addEventListener('mouseenter', function pauseOnHover() {
      isHovered = true;
      updatePlayback();
    });

    slider.addEventListener('mouseleave', function resumeAfterHover() {
      isHovered = false;
      updatePlayback();
    });

    slider.addEventListener('focusin', function pauseOnFocus() {
      isFocused = true;
      updatePlayback();
    });

    slider.addEventListener('focusout', function resumeAfterFocus(event) {
      isFocused = slider.contains(event.relatedTarget);
      updatePlayback();
    });

    track.addEventListener('touchstart', function pauseOnTouch() {
      isTouching = true;
      updatePlayback();
    }, { passive: true });

    function resumeAfterTouch() {
      isTouching = false;
      updatePlayback();
    }

    track.addEventListener('touchend', resumeAfterTouch, { passive: true });
    track.addEventListener('touchcancel', resumeAfterTouch, { passive: true });

    track.addEventListener('keydown', function navigateWithKeyboard(event) {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault();
        const direction = event.key === 'ArrowLeft' ? -1 : 1;
        showSlide(activeIndex + direction);
        updatePlayback();
      }
    });

    track.addEventListener('scroll', function recordVisibleSlide() {
      cancelAnimationFrame(scrollFrame);
      scrollFrame = requestAnimationFrame(function updateActiveIndex() {
        activeIndex = Math.round(track.scrollLeft / track.clientWidth);
      });
    }, { passive: true });

    const resizeObserver = new ResizeObserver(function preserveVisibleSlide() {
      track.scrollTo({
        left: activeIndex * track.clientWidth,
        behavior: 'instant'
      });
    });

    resizeObserver.observe(track);
    document.addEventListener('visibilitychange', updatePlayback);
    reducedMotion.addEventListener('change', updatePlayback);

    // Stop timers when leaving and restart when restored from the browser's cache.
    window.addEventListener('pagehide', function stopPlayback() {
      clearInterval(timer);
      cancelAnimationFrame(scrollFrame);
    });
    window.addEventListener('pageshow', updatePlayback);

    updatePlayback();
  }

  document.querySelectorAll('.graduation-slider').forEach(initializeSlider);
})();
