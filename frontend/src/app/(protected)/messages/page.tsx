export default function MessagesPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold tracking-tight">Сообщения</h1>
      <input 
        type="text" 
        placeholder="Поиск по всем каналам..." 
        className="w-full h-12 px-4 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 outline-none focus:ring-2 focus:ring-neutral-400 dark:focus:ring-neutral-700 transition-all"
      />
    </div>
  );
}