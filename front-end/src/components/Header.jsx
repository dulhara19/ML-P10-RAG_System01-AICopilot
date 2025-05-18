import { useEffect, useState } from "react";
import { GraduationCap, WifiOff, Wifi } from "lucide-react";

function Header() {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);
    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);
    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, []);

  return (
    <header className="w-full bg-indigo-600 text-white p-4 shadow-md flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <GraduationCap className="w-7 h-7" />
        <h1 className="text-xl font-semibold tracking-wide">University Copilot</h1>
      </div>

      <div className="flex items-center space-x-3">
        <div className="flex items-center gap-1">
          {isOnline ? (
            <>
              <Wifi className="w-5 h-5 text-green-300" />
              <span className="text-sm">Online</span>
            </>
          ) : (
            <>
              <WifiOff className="w-5 h-5 text-yellow-300" />
              <span className="text-sm">Offline</span>
            </>
          )}
        </div>
        {/* Optional: Future dark mode toggle
        <button className="p-2 bg-white text-indigo-600 rounded-full">🌓</button>
        */}
      </div>
    </header>
  );
}

export default Header;
