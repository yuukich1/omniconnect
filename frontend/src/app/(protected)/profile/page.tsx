export default function ProfilePage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold tracking-tight">Профиль</h1>
      <div className="flex items-center gap-4 border-b border-neutral-200 dark:border-neutral-800 pb-4">
        <div className="h-16 w-16 rounded-full bg-neutral-200 dark:bg-neutral-800 animate-fade-in" />
        <div>
          <h2 className="font-semibold text-lg">Fullstack Developer</h2>
          <p className="text-sm text-neutral-400">Настройки подключений</p>
        </div>
      </div>
    </div>
  );
}