'use client';

import { useAuthStore } from '@/store/useAuthStore';
import { useRegister } from './hooks/useRegister';
import { useRegisterAnimations } from './hooks/useRegisterAnimations';

interface RegisterFormProps {
  onSuccess: () => void;
  onSwitchMode: () => void;
}

export default function RegisterForm({ onSuccess, onSwitchMode }: RegisterFormProps) {
  const loginGlobal = useAuthStore((state) => state.login);

  const {
    step, setStep,
    username, setUsername,
    email, setEmail,
    password, setPassword,
    error, setError,
    isLoading,
    goNext,
    handleSubmit,
    completeWelcome
  } = useRegister(
    () => shake(), 
    (validUsername, token) => {
      loginGlobal({ id: 'current_user', username: validUsername }, token);
      onSuccess();
    }
  );

  const currentInputValue = step === 'name' ? username : step === 'email' ? email : password;
  const { 
    containerRef, inputRef, nextBtnRef, prevBtnRef, 
    summaryRef, hintRef, welcomeRef, 
    shake, transitionInput 
  } = useRegisterAnimations(step, currentInputValue, completeWelcome);

  const handleNextClick = () => {
    const nextStep = goNext();
    if (nextStep) {
      transitionInput(nextStep, () => setStep(nextStep));
    }
  };

  const handleChangeStep = (targetStep: typeof step) => {
    setError(null);
    transitionInput(targetStep, () => setStep(targetStep));
  };

  return (
    <div ref={containerRef} className="fixed inset-0 flex flex-col items-center justify-center bg-white dark:bg-black px-6 z-50 select-none overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] bg-neutral-200 dark:bg-neutral-800/40 rounded-full blur-[120px] pointer-events-none" />

      {step !== 'summary' && step !== 'welcome' && (
        <div className="w-full max-w-sm mb-4 text-center px-12 sm:px-0">
          <p ref={hintRef} className="text-xs tracking-wide text-neutral-400 dark:text-neutral-500 font-light transition-all">
            {step === 'name' && `Имя пользователя (максимум 20 символов: ${username.length}/20)`}
            {step === 'email' && 'Введите действующий почтовый адрес'}
            {step === 'password' && 'От 8 символов, включая 1 цифру и 1 заглавную букву'}
          </p>
        </div>
      )}

      {step !== 'summary' && step !== 'welcome' && (
        <div className="relative w-full max-w-sm flex items-center justify-center z-10 px-14 sm:px-0">
          <button
            ref={prevBtnRef}
            type="button"
            onClick={() => handleChangeStep(step === 'password' ? 'email' : 'name')}
            className="absolute left-0 sm:-left-16 h-12 w-12 flex items-center justify-center rounded-xl bg-neutral-50 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 active:scale-95 transition-all"
          >
            <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 12L6 8l4-4"/></svg>
          </button>

          <div className="w-full h-14 relative flex items-center">
            {step === 'name' && (
              <input
                ref={inputRef}
                type="text"
                value={username}
                maxLength={25} 
                placeholder="Как к вам обращаться?"
                onChange={(e) => setUsername(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && username.trim() && handleNextClick()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}

            {step === 'email' && (
              <input
                ref={inputRef}
                type="email"
                value={email}
                placeholder="Укажите ваш Email"
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && email.trim() && handleNextClick()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}

            {step === 'password' && (
              <input
                ref={inputRef}
                type="password"
                value={password}
                placeholder="Придумайте пароль"
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && password.trim() && handleNextClick()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}
          </div>

          <button
            ref={nextBtnRef}
            type="button"
            onClick={handleNextClick}
            className="absolute right-0 sm:-right-16 h-12 w-12 flex items-center justify-center rounded-xl bg-neutral-950 dark:bg-white text-white dark:text-black font-semibold active:scale-95 transition-all"
          >
            <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 4l4 4-4 4"/></svg>
          </button>
        </div>
      )}

      {step === 'summary' && (
        <div ref={summaryRef} className="w-full max-w-sm space-y-6 z-10 px-4 sm:px-0">
          <div className="space-y-1 text-center summary-item opacity-0">
            <h2 className="text-3xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">Проверьте данные</h2>
            <p className="text-xs tracking-wide uppercase text-neutral-400 dark:text-neutral-500 font-medium">Всё верно?</p>
          </div>

          <div className="border-t border-b border-neutral-100 dark:border-neutral-900 py-2 space-y-1">
            <div onClick={() => handleChangeStep('name')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Никнейм</span>
              <span className="text-base text-neutral-900 dark:text-neutral-100 font-light group-hover:underline underline-offset-4 decoration-neutral-400">{username}</span>
            </div>

            <div onClick={() => handleChangeStep('email')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Email</span>
              <span className="text-base text-neutral-900 dark:text-neutral-100 font-light max-w-[180px] sm:max-w-[200px] truncate group-hover:underline underline-offset-4 decoration-neutral-400">{email}</span>
            </div>

            <div onClick={() => handleChangeStep('password')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Пароль</span>
              <span className="text-base text-neutral-400 dark:text-neutral-600 tracking-widest text-xs">••••••••</span>
            </div>
          </div>

          <div className="summary-item opacity-0">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isLoading}
              className="w-full h-12 rounded-full bg-neutral-950 dark:bg-white text-white dark:text-black font-medium text-sm transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-40 flex items-center justify-center tracking-wide"
            >
              {isLoading ? <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" /> : 'Создать аккаунт'}
            </button>
          </div>
        </div>
      )}

      {step === 'welcome' && (
        <div ref={welcomeRef} className="text-center space-y-2 z-10">
          <h1 className="welcome-item opacity-0 text-4xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">
            Добро пожаловать!
          </h1>
          <p className="welcome-item opacity-0 text-sm tracking-wide text-neutral-400 dark:text-neutral-500 font-medium uppercase">
            {username}
          </p>
        </div>
      )}

      {error && step !== 'welcome' && (
        <p className="text-xs text-red-500 font-medium mt-4 absolute transform translate-y-52 sm:translate-y-52 z-20 px-1 text-center">{error}</p>
      )}

      {step !== 'welcome' && (
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 text-center z-10 w-full">
          <button
            type="button"
            onClick={onSwitchMode}
            className="text-xs tracking-wide text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-200 transition-colors underline underline-offset-4 decoration-neutral-200 dark:decoration-neutral-800"
          >
            Уже есть аккаунт. <span className="underline underline-offset-4 decoration-neutral-300 dark:decoration-neutral-700">Войти</span>
          </button>
        </div>
      )}
    </div>
  );
}