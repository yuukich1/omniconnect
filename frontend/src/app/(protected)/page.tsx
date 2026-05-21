export default function HomePage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold tracking-tight">Лента</h1>
      <p className="text-neutral-500 dark:text-neutral-400">
        Здесь будет лента из тгк и нашего приложения
      </p>
      <div className="h-32 w-full rounded-2xl bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 p-4 animate-pulse" />
    </div>
  );
}