"use client";

import { ClerkProvider } from "@clerk/nextjs";
import { useEffect, useState, type ReactNode } from "react";

import { isLikelyValidClerkPublishableKey } from "@/auth/clerkKey";
import {
  clearLocalAuthToken,
  getLocalAuthToken,
  isLocalAuthMode,
} from "@/auth/localAuth";
import { LocalAuthLogin } from "@/components/organisms/LocalAuthLogin";

export function AuthProvider({ children }: { children: ReactNode }) {
  const localMode = isLocalAuthMode();
  const [isHydrated, setIsHydrated] = useState(!localMode);
  const [hasLocalToken, setHasLocalToken] = useState(false);

  useEffect(() => {
    if (!localMode) {
      clearLocalAuthToken();
      setHasLocalToken(false);
      setIsHydrated(true);
      return;
    }

    setHasLocalToken(Boolean(getLocalAuthToken()));
    setIsHydrated(true);
  }, [localMode]);

  if (localMode) {
    if (!isHydrated) {
      return null;
    }

    if (!hasLocalToken) {
      return <LocalAuthLogin />;
    }

    return <>{children}</>;
  }

  const publishableKey = process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY;
  const afterSignOutUrl =
    process.env.NEXT_PUBLIC_CLERK_AFTER_SIGN_OUT_URL ?? "/";

  if (!isLikelyValidClerkPublishableKey(publishableKey)) {
    return <>{children}</>;
  }

  return (
    <ClerkProvider
      publishableKey={publishableKey}
      afterSignOutUrl={afterSignOutUrl}
    >
      {children}
    </ClerkProvider>
  );
}
