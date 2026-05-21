'use client';

import { RefreshCw } from 'lucide-react';

export default function MobileReloadButton() {
  const reloadPage = () => {
    window.location.reload();
  };

  return (
    <button
      onClick={reloadPage}
      className="
        fixed
        bottom-4
        right-4
        z-[9999]
        flex
        items-center
        justify-center
        w-12
        h-12
        rounded-full
        bg-neutral-900/90
        text-white
        shadow-lg
        border
        border-neutral-700
        active:scale-95
        transition
        md:hidden
      "
    >
      <RefreshCw size={20} />
    </button>
  );
}