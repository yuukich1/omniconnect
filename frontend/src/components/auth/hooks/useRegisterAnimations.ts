import { useEffect, useRef } from 'react';
import gsap from 'gsap';

export type Step = 'name' | 'email' | 'password' | 'summary' | 'welcome';

export function useRegisterAnimations(
  step: Step,
  currentInputValue: string,
  onWelcomeComplete: () => void
) {
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const nextBtnRef = useRef<HTMLButtonElement>(null);
  const prevBtnRef = useRef<HTMLButtonElement>(null);
  const summaryRef = useRef<HTMLDivElement>(null);
  const hintRef = useRef<HTMLParagraphElement>(null);
  const welcomeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (step !== 'summary' && step !== 'welcome') {
      inputRef.current?.focus();
    }
  }, [step]);

  useEffect(() => {
    if (hintRef.current && step !== 'welcome') {
      gsap.fromTo(hintRef.current, 
        { opacity: 0, y: -5 },
        { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }
      );
    }
  }, [step]);

  useEffect(() => {
    if (step === 'summary' || step === 'welcome') return;
    
    if (currentInputValue.trim().length > 0) {
      gsap.to(nextBtnRef.current, { opacity: 1, x: 0, pointerEvents: 'auto', duration: 0.2, ease: 'power2.out' });
    } else {
      gsap.to(nextBtnRef.current, { opacity: 0, x: -8, pointerEvents: 'none', duration: 0.15 });
    }
  }, [currentInputValue, step]);

  useEffect(() => {
    if (step !== 'name' && step !== 'summary' && step !== 'welcome') {
      gsap.to(prevBtnRef.current, { opacity: 1, x: 0, pointerEvents: 'auto', duration: 0.2 });
    } else {
      gsap.to(prevBtnRef.current, { opacity: 0, x: 8, pointerEvents: 'none', duration: 0.15 });
    }
  }, [step]);

  useEffect(() => {
    if (step === 'summary' && summaryRef.current) {
      gsap.fromTo(summaryRef.current.querySelectorAll('.summary-item'),
        { opacity: 0, y: 15, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.4, stagger: 0.06, ease: 'power4.out' }
      );
    }
  }, [step]);

  useEffect(() => {
    if (step === 'welcome' && welcomeRef.current) {
      gsap.fromTo(welcomeRef.current.querySelectorAll('.welcome-item'),
        { opacity: 0, y: 25, scale: 0.96 },
        { 
          opacity: 1, y: 0, scale: 1, duration: 0.6, stagger: 0.15, ease: 'power4.out',
          onComplete: () => {
            gsap.to(containerRef.current, {
              opacity: 0, scale: 0.98, duration: 0.4, delay: 2, ease: 'power3.inOut',
              onComplete: onWelcomeComplete
            });
          }
        }
      );
    }
  }, [step, onWelcomeComplete]);

  const shake = () => {
    if (!containerRef.current) return;
    gsap.to(containerRef.current, {
      x: 6, duration: 0.05, yoyo: true, repeat: 4,
      onComplete: () => gsap.set(containerRef.current, { x: 0 })
    });
  };

  const transitionInput = (nextStep: Step, onComplete: () => void) => {
    if (!inputRef.current || nextStep === 'summary' || nextStep === 'welcome') {
      onComplete();
      return;
    }

    const isForward = nextStep === 'password' || (step === 'name' && nextStep === 'email');
    const xOffset = isForward ? -10 : 10;

    gsap.to(inputRef.current, {
      opacity: 0, x: xOffset, duration: 0.15,
      onComplete: () => {
        onComplete();
        gsap.fromTo(inputRef.current, 
          { opacity: 0, x: -xOffset }, 
          { opacity: 1, x: 0, duration: 0.2 }
        );
      }
    });
  };

  return { containerRef, inputRef, nextBtnRef, prevBtnRef, summaryRef, hintRef, welcomeRef, shake, transitionInput };
}