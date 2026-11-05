import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { Banner } from './components/Banner';
import { Footer } from './components/Footer';
import { PhoneFrame } from './components/PhoneFrame';
import { Placeholder } from './components/Placeholder';
import { SidePanel } from './components/SidePanel';
import { customerScreens, findScreen, otherScreens } from './screens/registry';

export default function App() {
  const { pathname } = useLocation();
  return (
    <PhoneFrame side={<SidePanel screen={findScreen(pathname)} />}>
      <Banner />
      <main className="flex flex-1 flex-col overflow-y-auto">
        <Routes>
          {customerScreens.map((s, i) => (
            <Route key={s.id} path={s.path} element={<Placeholder screen={s} next={customerScreens[i + 1]} />} />
          ))}
          {otherScreens.map((s) => (
            <Route key={s.id} path={s.path} element={<Placeholder screen={s} />} />
          ))}
          <Route path="/customer" element={<Navigate to="/customer/invite" replace />} />
          <Route path="*" element={<Navigate to="/customer/invite" replace />} />
        </Routes>
        <Footer />
      </main>
    </PhoneFrame>
  );
}
