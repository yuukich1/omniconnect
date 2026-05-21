import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export function useLoginAnimations() {
  const containerRef = useRef<HTMLDivElement>(null);
  const elementsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!elementsRef.current) return;

    const items = elementsRef.current.querySelectorAll('.animate-item');

    gsap.set(items, { 
      opacity: 0, 
      y: 20, 
      scale: 0.98 
    });

    const timer = setTimeout(() => {
      gsap.to(items, { 
        opacity: 1, 
        y: 0, 
        scale: 1,
        duration: 0.5, 
        stagger: 0.07, 
        ease: 'power4.out',
        force3D: true 
      });
    }, 50);

    return () => clearTimeout(timer);
  }, []);

  const shakeValidationError = () => {
    if (!elementsRef.current) return;
    gsap.to(elementsRef.current, { 
      x: 6, 
      duration: 0.05, 
      yoyo: true, 
      repeat: 4, 
      onComplete: () => gsap.set(elementsRef.current, { x: 0 }) 
    });
  };

  const shakeApiError = () => {
    if (!elementsRef.current) return;
    gsap.fromTo(elementsRef.current, { x: -6 }, { 
      x: 0, 
      duration: 0.4, 
      ease: 'elastic.out(1, 0.4)' 
    });
  };

  const animateSuccess = (onComplete: () => void) => {
    if (!containerRef.current) return;
    gsap.to(containerRef.current, {
      opacity: 0,
      scale: 0.98,
      duration: 0.25,
      ease: 'power3.in',
      onComplete,
    });
  };

  return { containerRef, elementsRef, shakeValidationError, shakeApiError, animateSuccess };
}