import { useEffect, useRef } from 'react';
import { Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { Banner } from './components/Banner';
import { Footer } from './components/Footer';
import { PhoneFrame } from './components/PhoneFrame';
import { SidePanel } from './components/SidePanel';
import { findScreen } from './screens/registry';
import ColouristHome from './screens/ColouristHome';
import SalonHome from './screens/SalonHome';
import CeoScoreboard from './screens/CeoScoreboard';
import { StoreProvider } from './state/store';
import { TourBar, TourProvider } from './tour/Tour';
import S9Account from './screens/S9Account';
import S1Invite from './screens/S1Invite';
import S2Scan from './screens/S2Scan';
import S3Result from './screens/S3Result';
import S4Plan from './screens/S4Plan';
import S5Slot from './screens/S5Slot';
import S6Visit from './screens/S6Visit';
import S7After from './screens/S7After';
import S8Adjust from './screens/S8Adjust';

export default function App() {
  const { pathname } = useLocation();
  const mainRef = useRef<HTMLElement>(null);
  // New screen: scroll to top, in the phone frame and on a real phone.
  useEffect(() => { mainRef.current?.scrollTo(0, 0); window.scrollTo(0, 0); }, [pathname]);

  return (
    <StoreProvider>
      <TourProvider>
      <PhoneFrame side={<SidePanel screen={findScreen(pathname)} />}>
        <Banner />
        <main ref={mainRef} className="flex flex-1 flex-col overflow-y-auto">
          <Routes>
            <Route path="/customer/invite" element={<S1Invite />} />
            <Route path="/customer/scan" element={<S2Scan />} />
            <Route path="/customer/result" element={<S3Result />} />
            <Route path="/customer/plan" element={<S4Plan />} />
            <Route path="/customer/slot" element={<S5Slot />} />
            <Route path="/customer/visit" element={<S6Visit />} />
            <Route path="/customer/after" element={<S7After />} />
            <Route path="/customer/adjust" element={<S8Adjust />} />
            <Route path="/customer/account" element={<S9Account />} />
            <Route path="/colourist" element={<ColouristHome />} />
            <Route path="/salon" element={<SalonHome />} />
            <Route path="/ceo" element={<CeoScoreboard />} />
            <Route path="/customer" element={<Navigate to="/customer/invite" replace />} />
            <Route path="*" element={<Navigate to="/customer/invite" replace />} />
          </Routes>
          <Footer />
        </main>
        <TourBar />
      </PhoneFrame>
      </TourProvider>
    </StoreProvider>
  );
}
