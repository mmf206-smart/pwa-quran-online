import { useEffect } from 'react';

/**
 * فرمول اختصاصی: S_target = Y_card - (H_view - H_card) / 2
 */
export function useAutoScroll(containerRef, activeCardRef, isPlaying) {
  useEffect(() => {
    if (!isPlaying || !containerRef.current || !activeCardRef.current) return;

    const container = containerRef.current;
    const card = activeCardRef.current;

    const H_view = container.clientHeight;
    const H_card = card.offsetHeight;
    const Y_card = card.offsetTop;

    const S_target = Y_card - (H_view - H_card) / 2;

    container.scrollTo({
      top: Math.max(0, S_target),
      behavior: 'smooth'
    });
  }, [isPlaying, containerRef, activeCardRef]);
}