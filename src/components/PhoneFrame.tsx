import type { ReactNode } from 'react';

// On phones the app fills the screen. From 1024 px up it sits in a 390 x 844 phone frame.
// The rounded device bezel is hardware chrome, not a UI element, so it keeps its curve;
// everything inside the screen follows the kit (square, no shadows).
export function PhoneFrame({ children, side }: { children: ReactNode; side: ReactNode }) {
  return (
    <div className="min-h-full lg:flex lg:items-center lg:justify-center lg:gap-12 lg:p-8">
      <div className="mx-auto flex min-h-dvh w-full max-w-[430px] flex-col bg-paper
        lg:mx-0 lg:h-[844px] lg:min-h-0 lg:w-[390px] lg:overflow-hidden lg:rounded-[44px] lg:border-[10px] lg:border-ink">
        {children}
      </div>
      <div className="hidden lg:block">{side}</div>
    </div>
  );
}
