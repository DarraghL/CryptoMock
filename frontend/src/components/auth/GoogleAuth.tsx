// src/components/auth/GoogleAuth.tsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

declare global {
  interface Window {
    google: {
      accounts: {
        id: {
          initialize: (config: any) => void;
          renderButton: (element: HTMLElement | null, options: any) => void;
        };
      };
    };
  }
}

interface PopupPosition {
  width: number;
  height: number;
  left: number;
  top: number;
}

const GoogleAuth = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const [popupPosition, setPopupPosition] = useState<PopupPosition>(() => {
    const width = 400;
    const height = 600;
    const left = Math.round((document.documentElement.clientWidth - width) / 2);
    const top = Math.round((document.documentElement.clientHeight - height) / 2);
    return { width, height, left, top };
  });

  useEffect(() => {
    const handleResize = () => {
      setPopupPosition(prev => ({
        ...prev,
        left: Math.round((document.documentElement.clientWidth - prev.width) / 2),
        top: Math.round((document.documentElement.clientHeight - prev.height) / 2),
      }));
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    const handleCredentialResponse = async (response: any) => {
      try {
        console.log('Google response received:', response);
        await login(response.credential);
        navigate('/dashboard');
      } catch (error) {
        console.error('Login error:', error);
        setError('Authentication failed. Please try again.');
      }
    };

    const initializeGoogle = () => {
      const { width, height, left, top } = popupPosition;
      
      const config = {
        client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
        callback: handleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true,
        ux_mode: 'popup',
        position: 'center',
        popup_position: 'center',
        popup_window_features: `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes,status=1,centerscreen=yes,dialog=yes`,
        prompt_parent_centered: true,
      };

      window.google.accounts.id.initialize(config);

      window.google.accounts.id.renderButton(
        document.getElementById('googleButton'),
        { 
          type: 'standard',
          theme: 'outline',
          size: 'large',
          text: 'continue_with',
          shape: 'rectangular',
          width: 280,
          logo_alignment: 'center',
          use_fedcm_for_prompt: false,
        }
      );
    };

    const loadGoogleScript = () => {
      const script = document.createElement('script');
      script.src = "https://accounts.google.com/gsi/client";
      script.onload = initializeGoogle;
      script.async = true;
      script.defer = true;
      document.body.appendChild(script);
    };

    loadGoogleScript();

    return () => {
      const scriptElement = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
      if (scriptElement && scriptElement.parentNode) {
        scriptElement.parentNode.removeChild(scriptElement);
      }
    };
  }, [login, navigate, popupPosition]);

  return (
    <div className="flex flex-col items-center space-y-4">
      <div 
        id="googleButton" 
        className="w-full max-w-[280px] h-[40px] flex items-center justify-center"
      >
        {/* Custom button while Google button loads */}
        <div className="w-full h-full bg-white bg-opacity-10 rounded-md animate-pulse">
          <div className="w-full h-full flex items-center justify-center">
            <div className="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        </div>
      </div>
      {error && (
        <div className="text-red-400 text-sm mt-2 bg-red-900/20 px-4 py-2 rounded-md">
          {error}
        </div>
      )}
    </div>
  );
};

export default GoogleAuth;