import { NavLink, useLocation } from 'react-router-dom';
import { useEffect, useRef } from 'react';

const personas = [
  { id: 'customer', label: 'Customer', to: '/customer/invite' },
  { id: 'colourist', label: 'Colourist', to: '/colourist' },
  { id: 'salon', label: 'Salon', to: '/salon' },
  { id: 'ceo', label: 'CEO', to: '/ceo' },
];

export function personaFromPath(path: string) {
  return personas.find((p) => path.startsWith('/' + p.id))?.id ?? 'customer';
}

export function PersonaSwitcher() {
  const { pathname } = useLocation();
  // Coming back to "Customer" returns to the last customer screen, not always S1.
  const lastCustomer = useRef('/customer/invite');
  useEffect(() => { if (pathname.startsWith('/customer')) lastCustomer.current = pathname; }, [pathname]);
  const current = personaFromPath(pathname);

  return (
    <nav aria-label="Switch persona" className="grid grid-cols-4 border-b border-hairline bg-paper">
      {personas.map((p) => (
        <NavLink key={p.id} to={p.id === 'customer' ? lastCustomer.current : p.to}
          aria-current={current === p.id ? 'page' : undefined}
          className={`t-label flex min-h-11 items-center justify-center border-b-2 ${current === p.id ? 'border-ink text-ink' : 'border-transparent text-muted hover:text-ink'}`}>
          {p.label}
        </NavLink>
      ))}
    </nav>
  );
}
