"use client";

import { AuthMode } from "@/auth/mode";

let localToken: string | null = null;
const STORAGE_KEY = "mc_local_auth_token";

export function isLocalAuthMode(): boolean {
  return process.env.NEXT_PUBLIC_AUTH_MODE === AuthMode.Local;
}

function readStoredToken(storage: Storage): string | null {
  try {
    return storage.getItem(STORAGE_KEY);
  } catch {
    return null;
  }
}

function writeStoredToken(storage: Storage, token: string): void {
  try {
    storage.setItem(STORAGE_KEY, token);
  } catch {
    // Ignore storage failures (private mode / policy).
  }
}

function clearStoredToken(storage: Storage): void {
  try {
    storage.removeItem(STORAGE_KEY);
  } catch {
    // Ignore storage failures (private mode / policy).
  }
}

export function setLocalAuthToken(token: string): void {
  localToken = token;
  if (typeof window === "undefined") return;
  writeStoredToken(window.sessionStorage, token);
  writeStoredToken(window.localStorage, token);
}

export function getLocalAuthToken(): string | null {
  if (localToken) return localToken;
  if (typeof window === "undefined") return null;

  const sessionToken = readStoredToken(window.sessionStorage);
  if (sessionToken) {
    localToken = sessionToken;
    return sessionToken;
  }

  const persistedToken = readStoredToken(window.localStorage);
  if (persistedToken) {
    localToken = persistedToken;
    writeStoredToken(window.sessionStorage, persistedToken);
    return persistedToken;
  }

  return null;
}

export function clearLocalAuthToken(): void {
  localToken = null;
  if (typeof window === "undefined") return;
  clearStoredToken(window.sessionStorage);
  clearStoredToken(window.localStorage);
}
